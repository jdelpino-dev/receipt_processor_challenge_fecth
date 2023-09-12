import json
from receipts import Receipt
from app import receipt_pool


def test_process_valid_receipts(app, sample_receipt_data):
    """Test processing a valid receipt."""
    for data in sample_receipt_data:
        response = app.post('/receipts/process', json=data)
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert "id" in response_data


def test_process_invalid_receipts(app, invalid_receipt_data):
    """Test processing invalid receipts."""
    for data in invalid_receipt_data:
        response = app.post('/receipts/process', json=data)
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert "error" in response_data


def test_get_receipts_invalid_id(app, invalid_receipt_ids):
    """Test getting receipts with invalid ids."""
    for invalid_id in invalid_receipt_ids:
        response = app.get(f'/receipts/{invalid_id}')
        assert response.status_code == 404


def test_get_receipts_valid_id(
        app,
        sample_receipt_data,
        dict_of_ids_and_points):
    """Test getting receipts with valid ids."""
    # Add receipts to the pool that the endpoint can retrieve later
    # receipt_pool = app.receipt_pool

    # Create receipts from valid sample data, add them to the pool, and
    # store separately their ids and points in a list.
    for receipt_data in sample_receipt_data:
        receipt = Receipt(receipt_data)
        dict_of_ids_and_points[receipt.id] = str(receipt.points)
        receipt_pool.add_receipt(receipt)

    # Test retrieval of receipts
    for id, points in dict_of_ids_and_points.items():
        response = app.get(f'/receipts/{id}/points')
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data["points"] == points
