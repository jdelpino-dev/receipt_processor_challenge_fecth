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
    """Provide a list of sample valid receipt data."""
    return [
        {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {"price": "6.49", "shortDescription": "Mountain Dew 12PK"}
            ],
            "total": "6.49"
        },
        {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"}
            ],
            "total": "9.00"
        },
        {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                {
                    "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                    "price": "12.00"
                }
            ],
            "total": "35.35"
        }
    ]


@pytest.fixture
def filled_receipt_pool(sample_receipt_data):
    """
    Create a Receipt_Pool instance and populate it with
    valid sample receipt data."""
    pool = Receipt_Pool()
    for data in sample_receipt_data:
        receipt = Receipt(data)
        pool.add_receipt(receipt)
    return pool


@pytest.fixture
def invalid_receipt_data():
    """Provide a collection of invalid receipt data."""
    return [
        {
            # Missing retailer
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {"price": "6.49", "shortDescription": "Mountain Dew 12PK"}
            ],
            "total": "6.49"
        },
        {
            # Invalid date
            "retailer": "Target",
            "purchaseDate": "Invalid-Date",
            "purchaseTime": "13:01",
            "items": [
                {"price": "6.49", "shortDescription": "Mountain Dew 12PK"}
            ],
            "total": "6.49"
        },
        {
            # Invalid time
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "Invalid-Time",  # Invalid time
            "items": [
                {"price": "6.49", "shortDescription": "Mountain Dew 12PK"}
            ],
            "total": "6.49"
        },
        {
            # Missing items
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [],
            "total": "6.49"
        },
        {
            # Invalid item price
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [],
            "total": "6"
        }
    ]


@pytest.fixture
def receipt_pool(scope="module"):
    """Create an empty Receipt_Pool instance available to all tests
    in a module."""
    return Receipt_Pool()


@pytest.fixture
def list_of_receipt_ids(scope="module"):
    """Provide an empy list of receipt ids available to all tests
    in a module."""
    return list()
