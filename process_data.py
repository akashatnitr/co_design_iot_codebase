import googlemaps
api_key = ""
def geocode_location(lat, lon, api_key):
    gmaps = googlemaps.Client(key=api_key)
    
    try:
        reverse_geocode_result = gmaps.reverse_geocode((lat, lon))
        if reverse_geocode_result:
            address = reverse_geocode_result[0]['formatted_address']
            location_type = reverse_geocode_result[0]['types']
            return {
                'address': address,
                'name': reverse_geocode_result[0]['address_components'],
                'type': location_type
            }
        else:
            return None
    except Exception as e:
        return {'error': str(e)}

# Example usage
# api_key = 'YOUR_API_KEY'  # Replace with your Google Maps API key
lat = 40.748817
lon = -73.985428
result = geocode_location(lat, lon, api_key)
print(result)
