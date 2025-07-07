import pytest
from app.categorizer import categorize_transaction

def test_categorize_transaction_default():
    tx = {"merchant": "Unknown"}
    assert categorize_transaction(tx) == "uncategorized"

# Add more tests as categorization logic evolves
