import random
import requests

# Google Maps Geocoding API endpoint
GEOCODING_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

# Google Maps API Key
API_KEY = 'your_google_maps_api_key'

def generate_coordinates(address):
    """Generate latitude and longitude coordinates for a given address using Google Maps Geocoding API."""
    params = {
        'address': address,
        'key': API_KEY
    }
    response = requests.get(GEOCODING_API_URL, params=params)
    data = response.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        return None, None

class GPSTrackingResource:
    def post(self):
        try:
            data = request.get_json()
            address = data['address']
            latitude, longitude = generate_coordinates(address)
            if latitude is not None and longitude is not None:
                # Store location data in the database
                store_location_data({'latitude': latitude, 'longitude': longitude, 'cab_id': data['cab_id']})
                return jsonify({'message': 'GPS data received successfully'}), 201
            else:
                return jsonify({'message': 'Failed to generate coordinates for the address'}), 400
        except Exception as e:
            logger.error("Error processing GPS data: %s", e)
            return jsonify({'message': 'Internal Server Error'}), 500
