from fastapi.testclient import TestClient
from app.main import app
from app.schemas.receipt import Receipt, Item

client = TestClient(app)

def test_process_receipt_endpoint():
    receipt_data = Receipt(
        retailer="Target",
        purchaseDate="2022-01-01",
        purchaseTime="13:01",
        items=[
            Item(shortDescription="Mountain Dew 12PK", price="6.49"),
            Item(shortDescription="Emils Cheese Pizza", price="12.25"),
            Item(shortDescription="Knorr Creamy Chicken", price="1.26"),
            Item(shortDescription="Doritos Nacho Cheese", price="3.35"),
            Item(shortDescription="   Klarbrunn 12-PK 12 FL OZ  ", price="12.00")
        ],
        total="35.35"
    )
    response = client.post("/api/v1/receipts/process", json=receipt_data.model_dump())

    assert response.status_code == 201
    assert "id" in response.json()

def test_get_points_endpoint():
    # process a receipt to generate a valid receipt ID
    receipt_data = Receipt(
        retailer="Target",
        purchaseDate="2022-01-01",
        purchaseTime="13:01",
        items=[
            Item(shortDescription="Mountain Dew 12PK", price="6.49"),
            Item(shortDescription="Emils Cheese Pizza", price="12.25"),
            Item(shortDescription="Knorr Creamy Chicken", price="1.26"),
            Item(shortDescription="Doritos Nacho Cheese", price="3.35"),
            Item(shortDescription="   Klarbrunn 12-PK 12 FL OZ  ", price="12.00")
        ],
        total="35.35"
    )
    process_response = client.post("/api/v1/receipts/process", json=receipt_data.model_dump())
    receipt_id = process_response.json()["id"]

    # test the get_points_endpoint with the valid receipt ID
    response = client.get(f"/api/v1/receipts/{receipt_id}/points")
    assert response.status_code == 200
    assert "points" in response.json()
    assert response.json()["points"] > 0  # Points should be greater than 0

def test_process_receipt_invalid_date_format():
    receipt_data = {
        "retailer": "Best Buy",
        "purchaseDate": "07/20/2024",  # Invalid date format
        "purchaseTime": "14:15",
        "items": [{"shortDescription": "Gadget", "price": "50.00"}],
        "total": "50.00"
    }
    response = client.post("/api/v1/receipts/process", json=receipt_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid date or time format"}

def test_process_receipt_total_mismatch():
    receipt_data = {
        "retailer": "Walmart",
        "purchaseDate": "2024-07-20",
        "purchaseTime": "12:30",
        "items": [
            {"shortDescription": "Item 1", "price": "10.00"},
            {"shortDescription": "Item 2", "price": "5.00"}
        ],
        "total": "20.00"  # Incorrect total
    }
    response = client.post("/api/v1/receipts/process", json=receipt_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Total does not match sum of item prices"}

def test_get_points_endpoint_not_found():
    response = client.get("/api/v1/receipts/1234/points")
    assert response.status_code == 404
    assert response.json() == {"detail": "Receipt not found"}

def test_validation_exception_handler_price():
    invalid_data = {
        "retailer": "StoreName",
        "purchaseDate": "2024-07-20",
        "purchaseTime": "14:15",
        "items": [{"shortDescription": "Item", "price": "invalid_price"}],  # Invalid price
        "total": "20.00"
    }
    response = client.post("/api/v1/receipts/process", json=invalid_data)
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "price: String should match pattern" in response.json()["detail"][0]

def test_validation_exception_handler_total_price():
    invalid_data = {
        "retailer": "StoreName",
        "purchaseDate": "2024-07-20",
        "purchaseTime": "14:15",
        "items": [{"shortDescription": "Item", "price": "1.35"}],  
        "total": "20.005" # Invalid Total price
    }
    response = client.post("/api/v1/receipts/process", json=invalid_data)
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "total: String should match pattern" in response.json()["detail"][0]

def test_validation_exception_handler_retailer():
    invalid_data = {
        "retailer": "StoreName@123", # Invalid retailer name
        "purchaseDate": "2024-07-20",
        "purchaseTime": "14:15",
        "items": [{"shortDescription": "Item", "price": "1.35"}],  
        "total": "1.35" 
    }
    response = client.post("/api/v1/receipts/process", json=invalid_data)
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "retailer: String should match pattern" in response.json()["detail"][0]


def test_validation_exception_handler_empty():
    invalid_data = {
        "purchaseDate": "2024-07-20",
        "purchaseTime": "23:15",
        "items": [{"shortDescription": "Item", "price": "1.35"}],  
        "total": "1.35" 
    }
    response = client.post("/api/v1/receipts/process", json=invalid_data)
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "retailer: Field required" in response.json()["detail"][0]