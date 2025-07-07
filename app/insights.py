"""
Insights module for GPay AI Insights Engine.
"""

import os
import re
import pandas as pd

def parse_gpay_html(html_input, ml_model=None):
    """
    Accepts a file path (str) or a file-like object (e.g., from Streamlit).
    Optionally uses an ML model for categorization.
    Returns: (DataFrame, categorization_method)
    """
    from bs4 import BeautifulSoup
    from app import categorizer

    if hasattr(html_input, "read"):
        # file-like object (e.g., Streamlit UploadedFile)
        content = html_input.read()
        if isinstance(content, bytes):
            content = content.decode("utf-8")
        soup = BeautifulSoup(content, "html.parser")
    else:
        with open(html_input, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

    transactions = []
    for cell in soup.find_all("div", class_="outer-cell"):
        main_info = cell.find("div", class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1")
        if not main_info:
            continue
        main_text = main_info.get_text(separator=" ", strip=True)
        amount_match = re.search(r"₹[\d,]+(?:\.\d+)?", main_text)
        amount = amount_match.group(0).replace("₹", "").replace(",", "") if amount_match else None
        type_match = re.match(r"(Sent|Paid|Received|Used)", main_text)
        tx_type = type_match.group(1) if type_match else None
        account_match = re.search(r"Account\s+([A-Z0-9X]+)", main_text)
        account = account_match.group(1) if account_match else None
        merchant = None
        merchant_match = re.search(r"to\s+(.+?)\s+using", main_text)
        if merchant_match:
            merchant = merchant_match.group(1)
        else:
            merchant_match2 = re.match(r"(Paid|Received)\s+₹[\d,\.]+\s+to\s+(.+?)\s+using", main_text)
            if merchant_match2:
                merchant = merchant_match2.group(2)
        date_match = re.search(r"\d{1,2} \w+ \d{4}, [\d:]+ GMT[+\-]\d{2}:\d{2}", main_text)
        date = date_match.group(0) if date_match else None
        caption = cell.find("div", class_="content-cell mdl-cell mdl-cell--12-col mdl-typography--caption")
        status = None
        if caption:
            status_match = re.search(r"(Completed|Failed|Cancelled|Pending)", caption.get_text())
            if status_match:
                status = status_match.group(1)
        transactions.append({
            "type": tx_type,
            "amount": float(amount) if amount else None,
            "account": account,
            "merchant": merchant,
            "date": date,
            "status": status,
            "raw": main_text
        })

    df = pd.DataFrame(transactions)
    if not df.empty:
        if ml_model is not None:
            df["category"] = df.apply(lambda row: categorizer.categorize_transaction(row, ml_model=ml_model), axis=1)
            categorization_method = "AI/ML model"
        else:
            df["category"] = df.apply(lambda row: categorizer.categorize_transaction(row), axis=1)
            categorization_method = "rule-based"
    else:
        categorization_method = "N/A"
    return df, categorization_method

def generate_smart_insights(df, period_unit="M"):
    """
    Generate human-readable insights from the transactions DataFrame.
    period_unit: "M" (monthly), "W" (weekly), "Y" (yearly), etc.
    Returns a list of strings.
    """
    import numpy as np

    insights = []
    if df.empty:
        return ["No transactions to analyze."]

    # Ensure date is parsed
    df = df.copy()
    df["date_parsed"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date_parsed"])

    # Periodic spend by category
    df["period"] = df["date_parsed"].dt.to_period(period_unit)
    current_period = df["period"].max()
    prev_period = current_period - 1 if current_period else None

    # 1. Spend change for each category
    if prev_period:
        for cat in df["category"].unique():
            this_period = df[(df["period"] == current_period) & (df["category"] == cat) & (df["type"].isin(["Sent", "Paid"]))]
            last_period = df[(df["period"] == prev_period) & (df["category"] == cat) & (df["type"].isin(["Sent", "Paid"]))]
            this_total = this_period["amount"].sum()
            last_total = last_period["amount"].sum()
            if last_total > 0:
                pct = ((this_total - last_total) / last_total) * 100
                if abs(pct) > 10 and this_total > 0:
                    direction = "increased" if pct > 0 else "decreased"
                    insights.append(f"Your {cat} expenses {direction} by {abs(pct):.0f}% this {df['period'].dtype.name.lower()}.")
    # 2. Top merchants this period
    top_merchants = (
        df[(df["period"] == current_period) & (df["type"].isin(["Sent", "Paid"]))]
        .groupby("merchant")["amount"].sum()
        .sort_values(ascending=False)
        .head(3)
    )
    if not top_merchants.empty:
        top_list = ", ".join(top_merchants.index)
        insights.append(f"Top 3 merchants this {df['period'].dtype.name.lower()}: {top_list}")
        insights.append(f"You spent most on {top_merchants.index[0]} this {df['period'].dtype.name.lower()}.")

    return insights

def load_and_analyze(input_path, period_unit="M"):
    import joblib

    ml_model = None
    categorization_method = "rule-based"
    model_path = os.path.join("model", "categorizer.pkl")
    if os.path.exists(model_path):
        try:
            ml_model = joblib.load(model_path)
            categorization_method = "AI/ML model"
        except Exception as e:
            print(f"Warning: Failed to load ML model ({model_path}): {e}")
            ml_model = None
            categorization_method = "rule-based"

    ext = os.path.splitext(input_path)[-1].lower()
    if ext == ".html":
        print(f"Parsing HTML: {input_path}")
        df, method = parse_gpay_html(input_path, ml_model=ml_model)
        categorization_method = method
        out_csv = os.path.join(os.path.dirname(input_path), "parsed_transactions.csv")
        df.to_csv(out_csv, index=False)
        print(f"Extracted {len(df)} transactions to {out_csv}")
    else:
        print(f"Loading CSV: {input_path}")
        df = pd.read_csv(input_path)

    print(f"\nCategorization method used: {categorization_method}")

    # Basic insights
    print("\n--- Basic Insights ---")
    print(f"Total transactions: {len(df)}")
    print(f"Total spent: ₹{df[df['type'].isin(['Sent', 'Paid'])]['amount'].sum():,.2f}")
    print(f"Total received: ₹{df[df['type'] == 'Received']['amount'].sum():,.2f}")
    print("\nTop merchants/recipients:")
    print(df['merchant'].value_counts().head(10))
    print("\nStatus breakdown:")
    print(df['status'].value_counts())

    # Smart, human-readable insights
    print("\n--- Smart Insights ---")
    for insight in generate_smart_insights(df, period_unit=period_unit):
        print(f"- {insight}")
