import json
import csv
import os, requests

from flask import Flask, send_file, jsonify

app = Flask(__name__)

RESERVATION_SERVICE_URL = os.getenv("RESERVATION_SERVICE_URL")
DRINKS_SERVICE_URL = os.getenv("DRINKS_SERVICE_URL")
DRINKS_SAVER_SERVICE_URL = os.getenv("DRINKS_SAVER_SERVICE_URL")


@app.route('/api/v1/reservation/data/csv', methods=['GET'])
def get_reservation_data():
    try:
        # Get data from reservation service
        response = requests.get(f'{RESERVATION_SERVICE_URL}/api/v1/reservations')
        reservation_data = response.json()

        # Write data to CSV
        csv_filename = 'reservation_data.csv'

        # Define the field names for our CSV
        fieldnames = ['first_name', 'last_name', 'country', 'room_type', 'days_rented', 'price']

        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            # Process each reservation
            for reservation in reservation_data:
                data_row = {
                    "first_name": reservation.get("guest", {}).get("first_name"),
                    "last_name": reservation.get("guest", {}).get("last_name"),
                    "country": reservation.get("guest", {}).get("country"),
                    "room_type": reservation.get("room", {}).get("room_type"),
                    "days_rented": reservation.get("reservation_details", {}).get("days_rented"),
                    "price": reservation.get("reservation_details", {}).get("price")
                }
                writer.writerow(data_row)
        
        app.logger.info(f"CSV file created successfully")

        # Send the CSV file as a response to the client
        return send_file(
            csv_filename,
            mimetype='text/csv',
            download_name='reservation_data.csv',
            as_attachment=True,
        ), 200, app.logger.info(f"CSV file sent successfully")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up the temporary file if it exists
        if csv_filename in locals():
            try:
                os.remove(csv_filename)
            except:
                pass

@app.route('/api/v1/drinks/data/csv', methods=['GET'])
def get_drinks_data():
    try:
        # Get data from drinks service
        response = requests.get(f'{DRINKS_SERVICE_URL}/api/v1/drinks')
        drinks_data = response.json()

        #Get data from drink sales service
        response = requests.get(f'{DRINKS_SAVER_SERVICE_URL}/api/v1/drink_sales/purchase')
        drink_sales_data = response.json()

        app.logger.info(f"drinks data: {drinks_data}")
        app.logger.info(f"drink sales data: {drink_sales_data}")

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
    