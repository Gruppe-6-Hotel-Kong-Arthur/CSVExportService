# CSV Export Service
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

## Overview
The CSV Export Service is a component of the Hotel Kong Arthur management system, responsible for exporting data from other microservices into CSV format. Built with Flask, this microservice provides a RESTful API for generating and downloading CSV reports of reservation and drink sales data.

Key Features:
- Export reservation data to CSV format
- Export combined drinks and drink sales data to CSV format
- Automatic cleanup of temporary files
- Comprehensive error handling
- Docker containerization
- Integration with multiple microservices

## Project Structure
```bash
CSVExportService/
├── app.py                           # Main application entry point
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation
```

## API Documentation
| Method | Endpoint | Description | Request Body | Response (200) | Error Responses |
|--------|----------|-------------|--------------|----------------|-----------------|
| GET | /api/v1/reservation/data/csv | Export reservation data to CSV | N/A | CSV file download | 500: {"error": "Error message"} |
| GET | /api/v1/drinks/data/csv | Export drinks and sales data to CSV | N/A | CSV file download | 500: {"error": "Error message"} |

### CSV File Formats

#### Reservation Data CSV
```csv
first_name,last_name,country,room_type,days_rented,season,price
```

#### Drinks Data CSV
```csv
drink_id,drink_name,category,price_dkk,units_sold
```

## Installation & Setup
### Local Development
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 app.py
```

### Docker Setup
1. Create Docker network (if not exists):
```bash
docker network create microservice-network
```

2. Build and run the service:
```bash
# Build image
docker build -t csv_export_service . && docker image prune -f

# Run container
docker run -d \
  -p 5005:5005 \
  --name csv_export_service \
  --network microservice-network \
  -e RESERVATION_SERVICE_URL=http://reservation_service:5001 \
  -e DRINK_SERVICE_URL=http://drink_service:5004 \
  -e DRINKS_SALES_SERVICE_URL=http://drink_sales_service:5006 \
  csv_export_service
```

## Testing
### Prerequisites
- Docker Desktop installed and running
- Python 3.x (for local development)
- Postman or similar API testing tool
- Running instances of Reservation Service, Drink Service, and Drink Sales Service

### Example API Calls
1. Export reservation data
   - Method: GET
   - Request: http://127.0.0.1:5005/api/v1/reservation/data/csv
   - Response: Downloads a CSV file containing reservation data

2. Export drinks and sales data
   - Method: GET
   - Request: http://127.0.0.1:5005/api/v1/drinks/data/csv
   - Response: Downloads a CSV file containing combined drinks and sales data

---
#### Created by Hotel Kong Arthur Team
