import pytest
from app import app as flask_app
from receipts import Receipt, Receipt_Pool


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a test client using the Flask application
    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def sample_receipt_data():
    """Provide a sample valid receipt data."""
    return {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [{"price": "6.49", "shortDescription": "Mountain Dew 12PK"}],
        "total": "6.49"
    }


@pytest.fixture
def receipt():
    """Create a Receipt instance from sample data."""
    data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [{"price": "6.49", "shortDescription": "Mountain Dew 12PK"}],
        "total": "6.49"
    }
    return Receipt(data)


@pytest.fixture
def receipt_pool():
    """Create a Receipt_Pool instance."""
    return Receipt_Pool()
