def city_to_coordinates(city_name):
    """
    Convert a city name to its geographic coordinates.
    In a real implementation, this would use a geocoding API.
    For simulation, we use a hardcoded dictionary of major port cities.
    
    Args:
        city_name (str): Name of the city to look up
        
    Returns:
        dict or None: Dictionary with 'lat' and 'lon' keys if city is found, None otherwise
    """
    # Dictionary of sample port cities and their coordinates
    city_coords = {
        "vladivostok": {"lat": 43.1056, "lon": 131.8735},
        "san francisco": {"lat": 37.7749, "lon": -122.4194},
        "shanghai": {"lat": 31.2304, "lon": 121.4737},
        "rotterdam": {"lat": 51.9244, "lon": 4.4777},
        "dubai": {"lat": 25.2048, "lon": 55.2708},
        "singapore": {"lat": 1.3521, "lon": 103.8198},
        "long beach": {"lat": 33.7701, "lon": -118.1937},
        "houston": {"lat": 29.7604, "lon": -95.3698},
        "tokyo": {"lat": 35.6762, "lon": 139.6503},
        "sydney": {"lat": -33.8688, "lon": 151.2093}
    }
    
    # Normalize the city name (lowercase) for lookup
    normalized_city = city_name.lower()
    
    if normalized_city in city_coords:
        return city_coords[normalized_city]
    else:
        return None  # City not found

def generate_shodan_query(city_name, search_term="ICS", radius_km=5):
    """
    Generate a Shodan query string based on city name and search term
    
    Args:
        city_name (str): Name of the city to search near
        search_term (str): Term to search for in Shodan (default: "ICS")
        radius_km (int): Search radius in kilometers (default: 5)
        
    Returns:
        tuple: (query_string, coordinates) if city is found, or (None, error_message) if not found
    """
    coords = city_to_coordinates(city_name)
    
    if not coords:
        return None, f"City '{city_name}' not found in our database."
    
    # Format the geo search query for Shodan
    geo_query = f"geo:\"{coords['lat']},{coords['lon']},{radius_km}\""
    
    # Combine with search term
    query = f"{geo_query} \"{search_term}\""
    
    return query, coords 