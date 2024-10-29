# CSVExportService

"http://reservation_service:5003/api/v1/reservations" 

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

```bash
docker build -t csv_export_service .
```

```bash
docker run -d \        
  -p 5005:5005 \
  -e RESERVATION_SERVICE_URL=http://reservation_service:5003 \
  --name csv_export_service \
  --network microservice-network \
  csv_export_service
```