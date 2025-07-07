import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd

st.title("GPay AI Insights Engine")

uploaded_file = st.file_uploader("Upload Google Pay My Activity HTML or CSV", type=["html", "csv"])
if uploaded_file:
    import joblib
    from app import insights
    ml_model = None
    categorization_method = "rule-based"
    model_path = os.path.join("model", "categorizer.pkl")
    if os.path.exists(model_path):
        try:
            ml_model = joblib.load(model_path)
            categorization_method = "AI/ML model"
        except Exception as e:
            st.warning(f"Failed to load ML model: {e}")
            ml_model = None
            categorization_method = "rule-based"

    # User can select period, default is Monthly
    period_display = st.selectbox(
        "Select time period for insights",
        ["Monthly", "Weekly", "Yearly"],
        index=0  # Monthly is default
    )
    period_map = {"Monthly": "M", "Weekly": "W", "Yearly": "Y"}
    period_unit = period_map[period_display]

    ext = os.path.splitext(uploaded_file.name)[-1].lower()
    if ext == ".csv":
        df = pd.read_csv(uploaded_file)
    else:
        df, categorization_method = insights.parse_gpay_html(uploaded_file, ml_model=ml_model)

    # Year selection logic
    import pandas as pd
    df["date_parsed"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date_parsed"])
    if period_unit == "Y":
        df["year"] = df["date_parsed"].dt.year
        years = sorted(df["year"].dropna().unique())
        current_year = max(years)
        selected_year = st.selectbox(
            "Select year to analyze",
            years,
            index=years.index(current_year)
        )
        df = df[df["year"] == selected_year]

    st.info(f"Categorization method used: **{categorization_method}**")
    st.write("### Transactions", df)
    st.write("**Total transactions:**", len(df))
    st.write("**Total spent:** ₹{:,.2f}".format(df[df['type'].isin(['Sent', 'Paid'])]['amount'].sum()))
    st.write("**Total received:** ₹{:,.2f}".format(df[df['type'] == 'Received']['amount'].sum()))
    st.write("**Top merchants/recipients:**")
    st.write(df['merchant'].value_counts().head(10))
    st.write("**Status breakdown:**")
    st.write(df['status'].value_counts())

    st.write("### Smart Insights")
    for insight in insights.generate_smart_insights(df, period_unit=period_unit):
        st.write(f"- {insight}")
else:
    st.info("Upload a file to get started.")
