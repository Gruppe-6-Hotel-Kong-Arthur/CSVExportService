import json
import csv
import os, requests

from flask import Flask, send_file, jsonify

app = Flask(__name__)

RESERVATION_SERVICE_URL = os.getenv("RESERVATION_SERVICE_URL")
DRINKS_SERVICE_URL = os.getenv("DRINKS_SERVICE_URL")
DRINKS_SALES_SERVICE_URL = os.getenv("DRINKS_SALES_SERVICE_URL")


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
        drinks_response = requests.get(f'{DRINKS_SERVICE_URL}/api/v1/drinks')
        drinks_data = drinks_response.json()

        #Get data from drink sales service
        drinks_sales_response = requests.get(f'{DRINKS_SALES_SERVICE_URL}/api/v1/drink_sales/purchase')
        drink_sales_data = drinks_sales_response.json()

        # Convert both lists to dictionaries based on "drink_id"
        drinks_dict = {drink["drink_id"]: drink for drink in drinks_data}
        drink_sales_dict = {sale["drink_id"]: sale for sale in drink_sales_data}


        # Combine data on the "drink_id" key
        combined_data = []
        for drink_id, drink in drinks_dict.items():
            combined_entry = {**drink, **drink_sales_dict.get(drink_id, {})}
            combined_data.append(combined_entry)

        # Write data to CSV
        csv_filename = 'drinks_data.csv'

        # Define the field names for our CSV
        fieldnames = ['drink_id', 'drink_name', 'category', 'price_dkk', 'units_sold']

        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            # Process each drink
            for drink in combined_data:
                data_row = {
                    "drink_id": drink.get("drink_id"),
                    "drink_name": drink.get("drink_name"),
                    "category": drink.get("category"),
                    "price_dkk": drink.get("price_dkk"),
                    "units_sold": drink.get("units_sold")
                }
                writer.writerow(data_row)

        app.logger.info(f"CSV file created successfully")

        # Send the CSV file as a response to the client
        return send_file(
            csv_filename,
            mimetype='text/csv',
            download_name='drinks_data.csv',
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
    