"""
Transaction categorization module for GPay AI Insights Engine.

This module will provide functions to categorize transactions
(e.g., groceries, utilities, rent, etc.) based on merchant, amount, or description.
"""

def categorize_transaction(transaction, ml_model=None):
    """
    Categorize a single transaction using either:
    - ML/NLP model (if provided)
    - Fallback: merchant/description keyword rules
    """
    merchant = (transaction.get("merchant") or "").lower()
    raw = (transaction.get("raw") or "").lower()
    text = merchant + " " + raw

    # If ML model is provided, use it
    if ml_model is not None:
        return ml_model.predict([text])[0]

    # Fallback: Simple keyword-based rules
    categories = [
        ("groceries", ["bigbasket", "grofers", "more", "dmart", "spencer", "reliance fresh", "nature's basket"]),
        ("fuel", ["indian oil", "bharat petroleum", "hpcl", "fuel", "petrol", "shell"]),
        ("travel", ["uber", "ola", "irctc", "makemytrip", "goibibo", "yatra", "air india", "indigo", "spicejet", "flight", "train", "bus"]),
        ("food delivery", ["zomato", "swiggy", "domino", "pizza hut", "mcdonald", "kfc", "foodpanda"]),
        ("shopping", ["amazon", "flipkart", "myntra", "ajio", "snapdeal", "tatacliq"]),
        ("utilities", ["electricity", "power", "water", "gas", "broadband", "internet", "tata power", "bills", "apcpdcl", "tsspdcl"]),
        ("mobile recharge", ["airtel", "jio", "vi", "vodafone", "idea", "bsnl", "recharge"]),
        ("entertainment", ["netflix", "hotstar", "prime video", "bookmyshow", "spotify", "gaana", "wynk"]),
        ("health", ["apollo", "pharmacy", "medplus", "practo", "hospital", "clinic", "diagnostics"]),
        ("education", ["byju", "unacademy", "udemy", "coursera", "edx", "school", "college", "university"]),
        ("rent", ["rent", "no broker", "housing.com", "nestaway"]),
        ("others", []),
    ]

    for cat, keywords in categories:
        for kw in keywords:
            if kw in merchant or kw in raw:
                return cat
    return "others"

def train_ml_categorizer(X, y):
    """
    Train a simple ML/NLP model for transaction categorization.
    X: list of merchant/description strings
    y: list of category labels
    Returns a scikit-learn pipeline.
    """
    from sklearn.pipeline import Pipeline
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2))),
        ("clf", LogisticRegression(max_iter=1000))
    ])
    pipeline.fit(X, y)
    return pipeline
