import json
import csv
import os, requests

from flask import Flask, send_file, jsonify

app = Flask(__name__)

RESERVATION_SERVICE_URL = os.getenv("RESERVATION_SERVICE_URL")
#DRINK_SALES_SERVICE_URL = os.getenv("DRINK_SALES_SERVICE_URL")

@app.route('/api/v1/reservation/data/csv', methods=['GET'])
def get_reservation_data():
    try:
        # Get data from reservation service
        response = requests.get(RESERVATION_SERVICE_URL)
        reservation_data = response.json()

        # Make csv scheme
        data_scheme = {
            "first_name": reservation_data["guest"]["first_name"],
            "last_name": reservation_data["guest"]["last_name"],
            "country": reservation_data["guest"]["country"],
            "room_type": reservation_data["room"]["room_type"],
            "days_rented": reservation_data["reservation_details"]["days_rented"],
            "price": reservation_data["reservation_details"]["price"]
        }
        # Write data to CSV
        csv_filename = 'reservation_data.csv'
        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data_scheme.keys())
            writer.writeheader()
            writer.writerow(data_scheme)
        
        print("CSV file created successfully.")

        # Send the CSV file as a response to the client
        return send_file(
            csv_filename,
            mimetype='text/csv',
            download_name='reservation_data.csv',
            as_attachment=True,
        ), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)




   
