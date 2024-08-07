from app.schemas.receipt import Receipt, Item
from app.services.receipt_service import calculate_points

def test_calculate_points():
    #1
    receipt_1 = Receipt(
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
    points_1 = calculate_points(receipt_1)
    assert points_1 == 28, f"Expected 28, but got {points_1}"

    #2
    receipt_2 = Receipt(
        retailer="M&M Corner Market",
        purchaseDate="2022-03-20",
        purchaseTime="14:33",
        items=[
            Item(shortDescription="Gatorade", price="2.25"),
            Item(shortDescription="Gatorade", price="2.25"),
            Item(shortDescription="Gatorade", price="2.25"),
            Item(shortDescription="Gatorade", price="2.25")
        ],
        total="9.00"
    )
    points_2 = calculate_points(receipt_2)
    assert points_2 == 109, f"Expected 109, but got {points_2}"

    #3
    receipt_3 = Receipt(
        retailer="Walgreens",
        purchaseDate="2022-01-02",
        purchaseTime="08:13",
        items=[
            Item(shortDescription="Pepsi - 12-oz", price="1.25"),
            Item(shortDescription="Dasani", price="1.40")
        ],
        total="2.65"
    )
    points_3 = calculate_points(receipt_3)
    assert points_3 == 15, f"Expected 15, but got {points_3}"

    #4
    receipt_4 = Receipt(
        retailer="Target",
        purchaseDate="2022-01-02",
        purchaseTime="13:13",
        items=[
            Item(shortDescription="Pepsi - 12-oz", price="1.25")
        ],
        total="1.25"
    )
    points_4 = calculate_points(receipt_4)
    assert points_4 == 31, f"Expected 31, but got {points_4}"
