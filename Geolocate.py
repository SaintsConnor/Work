import requests
import math
import folium
from folium.plugins import HeatMap
from geopy.geocoders import Nominatim
import os
import concurrent.futures

# Function to perform Overpass API query
def overpass_query(query):
    url = "http://overpass-api.de/api/interpreter"
    response = requests.post(url, data={'data': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Function to search for a single entity within a bounding box
def search_entity(entity, bbox=None):
    if bbox:
        bbox_str = f"({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]})"
    else:
        bbox_str = ""
    query = f"""
    [out:json][timeout:60];
    (
      node["name"="{entity}"]{bbox_str};  // Changed from "brand" to "name"
      way["name"="{entity}"]{bbox_str};   // Search for names of natural features
      relation["name"="{entity}"]{bbox_str};
    );
    out center;
    """
    data = overpass_query(query)
    locations = []
    for element in data['elements']:
        if 'lat' in element and 'lon' in element:  # For nodes
            locations.append((entity, element['lat'], element['lon'], element.get('tags', {})))
        elif 'center' in element:  # For ways and relations (use center coordinates)
            locations.append((entity, element['center']['lat'], element['center']['lon'], element.get('tags', {})))
    return locations

# Function to search for multiple entities (brands, natural features, etc.) within a bounding box
def search_entities_by_name(entity_names, bbox=None):
    locations = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(search_entity, entity, bbox) for entity in entity_names]
        for future in concurrent.futures.as_completed(futures):
            locations.extend(future.result())
    return locations

# Function to create a heatmap from the found locations
def export_heatmap(locations, proximity_radius=100):
    if not locations:
        print("No locations to create heatmap.")
        return

    # Ensure unique markers by type and filter out locations within 100 meters of each other
    unique_locations = {}
    for entity, lat, lon, tags in locations:
        if entity not in unique_locations:
            unique_locations[entity] = []
        # Check if there is any location of the same type within 100 meters
        if not any(haversine(lat, lon, other_lat, other_lon) < proximity_radius for other_lat, other_lon, _ in unique_locations[entity]):
            unique_locations[entity].append((lat, lon, tags))

    filtered_locations = [(entity, lat, lon, tags) for entity, locs in unique_locations.items() for lat, lon, tags in locs]

    # Remove locations that are not within the proximity radius of any other location
    final_locations = []
    for i, (entity1, lat1, lon1, tags1) in enumerate(filtered_locations):
        if any(haversine(lat1, lon1, lat2, lon2) < proximity_radius for j, (entity2, lat2, lon2, tags2) in enumerate(filtered_locations) if i != j):
            final_locations.append((entity1, lat1, lon1, tags1))

    if not final_locations:
        print("No locations within the specified proximity radius.")
        return

    avg_lat = sum([loc[1] for loc in final_locations]) / len(final_locations)
    avg_lon = sum([loc[2] for loc in final_locations]) / len(final_locations)
    folium_map = folium.Map(location=[avg_lat, avg_lon], zoom_start=13)
    
    # Prepare data for the heatmap
    heat_data = [[lat, lon] for _, lat, lon, _ in final_locations]

    # Add heatmap to the folium map
    HeatMap(heat_data, radius=15).add_to(folium_map)

    # Function to add markers to the map
    def add_marker(entity, lat, lon, tags):
        popup_text = f"{entity}<br>{tags}"
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_text, parse_html=True),
            icon=folium.Icon(color='blue')
        ).add_to(folium_map)

    # Add markers in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(add_marker, entity, lat, lon, tags) for entity, lat, lon, tags in final_locations]
        concurrent.futures.wait(futures)
    
    # Get the user's Documents folder path
    documents_folder = os.path.expanduser("~/Documents/locations")
    os.makedirs(documents_folder, exist_ok=True)  # Create the 'locations' directory if it doesn't exist
    filename = os.path.join(documents_folder, "heatmap.html")
    
    # Save the map as an HTML file
    folium_map.save(filename)
    print(f"Heatmap exported to {filename}")

# Function to calculate distance between two latitude/longitude pairs using the Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Radius of the Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c  # Distance in meters
    return distance

# Function to filter locations that are within a certain radius of each other
def filter_by_proximity(locations, radius):
    results = []
    
    for i, (entity1, lat1, lon1, tags1) in enumerate(locations):
        for j, (entity2, lat2, lon2, tags2) in enumerate(locations):
            if i != j:  # Don't compare the same location
                distance = haversine(lat1, lon1, lat2, lon2)
                if distance <= radius:
                    results.append({
                        'entity1': entity1, 'lat1': lat1, 'lon1': lon1, 'tags1': tags1,
                        'entity2': entity2, 'lat2': lat2, 'lon2': lon2, 'tags2': tags2,
                        'distance': distance
                    })
    return results

# Function to get the bounding box of a state, city, or region using Geopy
def get_bounding_box(location_name):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(location_name)
    if location:
        # Bounding box is (southwest_lat, southwest_lon, northeast_lat, northeast_lon)
        bbox = location.raw['boundingbox']
        return [float(bbox[0]), float(bbox[2]), float(bbox[1]), float(bbox[3])]
    else:
        print(f"Location '{location_name}' not found.")
        return None

# Main menu function
def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Search multiple entities (e.g., brands, natural features)")
        print("2. Export heatmap")
        print("3. Search in a specific area (e.g., state)")
        print("4. Exit")

        choice = input("Select an option (1-4): ")

        if choice == "1":
            entity_input = input("Enter multiple entities to search (e.g., 'Starbucks;River Thames;Mount Everest'): ")
            entity_names = [entity.strip() for entity in entity_input.split(';')]
            proximity_radius = float(input("Enter proximity radius in meters (e.g., 1000 for 1 km): "))

            print(f"Searching for locations of: {', '.join(entity_names)}...")
            locations = search_entities_by_name(entity_names)
            if locations:
                print(f"Found {len(locations)} locations.")
                export_heatmap(locations, proximity_radius)  # Automatically export heatmap after search
            else:
                print("No locations found.")

        elif choice == "2":
            if 'locations' in globals() and locations:
                print("Heatmap has already been exported automatically after the last search.")
            else:
                print("No locations available to create a heatmap. Please perform a search first.")

        elif choice == "3":
            entity_input = input("Enter multiple entities to search (e.g., 'Starbucks;River Thames;Mount Everest'): ")
            entity_names = [entity.strip() for entity in entity_input.split(';')]
            area = input("Enter the name of the area (e.g., 'California', 'New York', 'Los Angeles'): ")

            bbox = get_bounding_box(area)
            if bbox:
                print(f"Searching within the area: {area}...")
                locations = search_entities_by_name(entity_names, bbox)
                if locations:
                    print(f"Found {len(locations)} locations in {area}.")
                    proximity_radius = float(input("Enter proximity radius in meters (e.g., 1000 for 1 km): "))
                    export_heatmap(locations, proximity_radius)  # Automatically export heatmap after search
                else:
                    print(f"No locations found in {area}.")
            else:
                print(f"Could not determine bounding box for {area}.")

        elif choice == "4":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main_menu()
