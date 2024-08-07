from app.schemas.receipt import Receipt
from datetime import datetime
import math

# In-memory storage for receipts and their points
receipts_store = {}

def process_receipt(receipt: Receipt, receipt_id: str) -> None:
    points = calculate_points(receipt)
    receipts_store[receipt_id] = points

def get_receipt_points(receipt_id: str) -> int:
    return receipts_store.get(receipt_id)

def calculate_points(receipt: Receipt) -> int:
    points = 0
    
    # Rule 1: One point for every alphanumeric character in the retailer name
    points += sum(c.isalnum() for c in receipt.retailer)
    
    # Rule 2: 50 points if the total is a round dollar amount with no cents
    if receipt.total.endswith('.00'):
        points += 50
    
    # Rule 3: 25 points if the total is a multiple of 0.25
    if float(receipt.total) % 0.25 == 0:
        points += 25
    
    # Rule 4: 5 points for every two items on the receipt
    points += (len(receipt.items) // 2) * 5
    
    # Rule 5: If the trimmed length of the item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer
    for item in receipt.items:
        if len(item.shortDescription.strip()) % 3 == 0:
            points += math.ceil(float(item.price) * 0.2)
    
    # Rule 6: 6 points if the day in the purchase date is odd
    purchase_date = datetime.strptime(receipt.purchaseDate, "%Y-%m-%d")
    if purchase_date.day % 2 != 0:
        points += 6
    
    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = datetime.strptime(receipt.purchaseTime, "%H:%M")
    if datetime.strptime("14:00", "%H:%M") < purchase_time < datetime.strptime("16:00", "%H:%M"):
        points += 10
    
    return points
