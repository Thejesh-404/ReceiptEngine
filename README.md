# Receipt Engine

A receipt processing service built with FastAPI.

## Setup and Run using Docker

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Thejesh-404/ReceiptEngine
```

```bash
cd ReceiptEngine
```

### Step 2: Build the Docker Image

```bash
docker build -t receipt-processor:1.0 .
```

### Step 3: Run the Docker Container

```bash
docker run -d -p 8000:8000 receipt-processor
```

### Step 4: API Endpoints

Access the Application

```bash
http://localhost:8000
```


#### Process Receipt

Endpoint: POST /api/v1/receipts/process

Description: Submits a receipt for processing. The receipt data is validated and, if valid, processed to generate an ID that uniquely identifies the receipt.

Request Payload:

retailer (string, required): The name of the retailer or store where the purchase was made. It should match the regex pattern `^[\w\s\-&]+$`(alphanumeric, spaces, hyphens, and ampersands).

purchaseDate (string, required): The date of the purchase in YYYY-MM-DD format. It must be a valid date.

purchaseTime (string, required): The time of the purchase in HH:MM 24-hour format. It must be a valid time.

total (string, required): The total amount paid for the receipt. It should match the regex pattern `^\d+\.\d{2}$` (e.g., "1.25" or "100.00").

items (array of objects, required): A list of items on the receipt. Each item has the following structure:

shortDescription (string, required): A brief description of the item, matching the regex pattern `^[\w\s\-]+$` (alphanumeric, spaces, hyphens).
price (string, required): The price of the item, matching the regex pattern `^\d+\.\d{2}$` (e.g., "1.25" or "100.00")

```bash
{
    "retailer": "Target",
    "purchaseDate": "2024-06-02",
    "purchaseTime": "23:13",
    "total": "1.25",
    "items": [
        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
    ]
}
```


Using curl:

```bash
curl -X POST "http://0.0.0.0:8000/api/v1/receipts/process" \
-H "Content-Type: application/json" \
-d '{
    "retailer": "Target",
    "purchaseDate": "2024-06-02",
    "purchaseTime": "23:13",
    "total": "1.25",
    "items": [
        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
    ]
}'
```


Sample Response:

Status Code: 201 Created

Response Body:
```bash
{
    "id": "11bac2b8-dabf-47be-be91-000baa39f061"
}
```

#### Retrieving Points


Endpoint: GET /api/v1/receipts/{id}/points

Description: Retrieves the number of points awarded for a receipt based on its ID.

Path Parameter:

id (string, required): The unique ID of the receipt.


Using curl:

```bash
curl -X GET "http://0.0.0.0:8000/api/v1/receipts/{id}/points"
```

Sample Response:

Status Code: 200 OK

Response Body:

```bash
{
    "points": 31
}
```

## API Documentation
FastAPI automatically generates interactive API documentation. You can access it at:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
