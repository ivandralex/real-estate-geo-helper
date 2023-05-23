import os
from dotenv import load_dotenv
import googlemaps
from flask import jsonify

# Load .env file
load_dotenv()

def calculate_distance(request):
    # Parse request args
    address = request.args.get('address')
    coordinates = request.args.get('coordinates')

    # Ensure all necessary parameters are present in the request
    if not address or not coordinates:
        return jsonify({
            "error": "Invalid request",
            "message": "address and coordinates parameters are required"
        }), 400

    gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_MAPS_API_KEY'))

    # Geocode address
    geocode_result = gmaps.geocode(address)

    # ensure the geocoding was successful
    if not geocode_result or 'geometry' not in geocode_result[0]:
        return jsonify({
            "error": "Geocoding error",
            "message": "Could not geocode provided address"
        }), 400

    geocoded_address = geocode_result[0]['geometry']['location']

    
    modes_of_transport = ['walking', 'bicycling', 'transit']
    distance_info = {}

    for mode in modes_of_transport:
        # Calculate distance
        distance_result = gmaps.distance_matrix(origins = (geocoded_address['lat'], geocoded_address['lng']),
                                                destinations = coordinates,
                                                units = 'metric',
                                                mode = mode)
        # ensure the distance calculation was successful
        if not distance_result or 'rows' not in distance_result or not distance_result['rows']:
            return jsonify({
                "error": "Distance calculation error",
                "message": f"Could not calculate distance for mode: {mode}"
            }), 400

        distance_info[mode] = distance_result['rows'][0]['elements'][0]['duration']['text']

    response = jsonify({
        "address": address,
        "coordinates": coordinates,
        "distance_info": distance_info
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


#calculate_distance('68-80 hanbury street london e1 5jl', '51.507167,-0.058248')