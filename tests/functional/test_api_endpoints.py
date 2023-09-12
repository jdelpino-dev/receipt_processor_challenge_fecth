import json


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
