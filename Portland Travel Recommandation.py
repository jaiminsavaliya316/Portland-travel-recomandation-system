import requests
from functools import lru_cache
import heapq 
import pandas as pd 
import tkinter as tk
import time
from dotenv import load_dotenv
import os

last_cache_clear_time = time.time()
def configure():
    load_dotenv()

graph= {
    1: {2:2.3 , 3:2.2}, 2: {1: 2.3, 3: 0.06, 4: 0.3, 5: 0.4, 6: 0.2, 7: 1.1, 8: 1.6, 12:1.1}, 3: {1: 2.2, 2: 0.06, 4: 0.3, 5: 0.3, 6: 0.2, 7: 1.2, 8: 1.7, 12: 1.1}, 4: {2:0.3, 3:0.3, 5:0.2, 6:0.1}, 
    5: {2:0.4, 3: 0.3, 4:0.2, 6:0.2}, 6: {2:0.2, 3: 0.2, 4:0.1, 5: 0.2}, 7: {2:1.1, 3:1.2 , 8:0.7, 11:0.3, 12:0.5}, 8: {7: 0.7, 9:0.5, 10:1.6, 11:0.5}, 9: {8:0.5, 10:1.1},
    10: {8:1.6, 9:1.1, 35: 2.3, 22:2.3, 23:2.4, 16:2.4}, 11: {7:0.3, 8:0.5, 12:0.7, 13:1.0, 15:0.7, 16:0.7, 22:0.9}, 12: { 2:1.1, 3:1.1 , 7:0.5, 11:0.7, 13:1.1, 14:0.9, 15:0.9, 36:5.0, 38:3.9}, 13: {12:1.1, 14:0.3, 15:0.3, 17:0.4, 18:0.4, 36:4.1, 38:3.0},
    14: {12:0.9, 13:0.3, 15:0.05, 16:0.1, 17:0.2, 18:0.3}, 15: {11:0.7, 12:0.9, 13:0.3, 14:0.05, 16:0.1, 17:0.2, 18:0.3}, 16: {10:0.8, 11:0.7, 14:0.1, 15:0.1, 17:0.2, 18:0.3, 19:0.2}, 
    17: {13:0.7, 14:0.2, 15:0.2, 16:0.2, 18:0.3, 19:0.07, 20:0.1, 21:0.1}, 18: {13:0.4, 14:0.3, 15:0.3, 16:0.3, 19:0.2, 20:0.2, 21:0.2}, 19: {17:0.07, 18:0.2, 20:0.02, 21:0.07, 22:0.07}, 20: {17:0.1, 18:0.2, 19:0.02, 21:0.04, 22:0.04}, 
    21: {19:0.07, 20:0.04, 22:0.04, 23:0.2, 24:0.2, 25:0.4}, 22: {10:0.6, 11:0.9, 19:0.07, 20:0.04, 21:0.04, 23:0.2, 24:0.2, 25:0.4}, 23: {10:2.4, 22:0.2, 24:0.09, 25:0.2, 26:0.5, 27:0.5},
    24: {21:0.2, 22:0.2, 23:0.09, 25:0.3, 26:0.4, 27:0.4, 34:0.3}, 25: {21:0.4, 22:0.4, 23:0.2, 24:0.3, 26:0.3, 27:0.3, 34:0.5}, 26: {23:0.5, 24:0.4, 25:0.3, 27:0.07, 28:0.3, 29:0.4, 30:0.7, 34:0.5}, 
    27: {23:0.5, 24:0.4, 25:0.3, 26:0.07, 28:0.2, 29:0.3, 30:0.7, 34:0.4}, 28: {26:0.3, 27:0.2, 29:0.2, 30:0.5, 31:0.6, 34:0.4}, 29: {26:0.4, 28:0.2, 30:0.5, 31:0.5, 34:0.4}, 
    30: {28:0.5, 29:0.5, 31:0.5, 32:0.6, 33:0.4, 34:0.3, 35:0.8}, 31: {28:0.6, 29:0.5, 30:0.5, 32:0.4, 33:0.4, 34:0.7}, 32: {30:0.6, 31:0.4, 33:0.4, 34:0.9}, 33: {30:0.4, 31:0.4, 32:0.4, 34:0.7}, 
    34: {24:0.3, 27:0.4, 28:0.4, 29:0.4, 30:0.3, 31:0.7, 32:0.9, 33:0.7, 35:0.6}, 35: {10:0.6, 30:0.8, 33:0.9, 34:0.6}, 36: {12:5.0, 13:4.1 , 37:0.3, 38:2.5}, 37: {36:0.3, 38:4.2}, 
    38: {12:3.9, 13:3.0, 36:2.5, 39:0.2, 40:0.3}, 39: {38:0.2, 40:0.3, 41:0.8}, 40: {39:0.3}, 41: {39:0.8, 42:0.2} , 42: {41:0.2}
}

# Define a function to fetch weather data using a city ID and an API key.
def fetch_weather_data(city_id, api_key_weather):
    url = "http://api.openweathermap.org/data/2.5/weather"
    complete_url = f"{url}?appid={api_key_weather}&id={city_id}"
    response = requests.get(complete_url) 

    # Check if the API request was successful.
    if response.status_code == 200:
        weather_data = response.json()
        return weather_data  # Return the parsed weather data.
    else:
        print("Failed to retrieve data from OpenWeatherMap API.")
        return None


@lru_cache(maxsize=128)  # Cache results for up to 128 unique calls
def get_distances_in_miles(start_place_number, end_place_number, api_key_map):
    # Check if 24 hours (86400 seconds) have passed since the last cache clear
    global last_cache_clear_time
    if time.time() - last_cache_clear_time > 86400:  # 24 hours in seconds
        get_distances_in_miles.cache_clear()  # Clear the LRU cache
        last_cache_clear_time = time.time()  # Reset the cache clear time

    # Read addresses from the CSV file
    filename = 'Attractions.csv'
    attractions = pd.read_csv(filename)

    start_address = attractions.loc[start_place_number, 'address']
    end_address = attractions.loc[end_place_number, 'address']

    modes = ['driving']
    distances_in_miles = {}

    for mode in modes:
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={start_address}&destinations={end_address}&mode={mode}&units=imperial&key={api_key_map}"
        response = requests.get(url)
        print("Data retrieved from api")
        if response.status_code == 200:
            data = response.json()

            if data["rows"][0]["elements"][0]["status"] == "OK":
                distance = data["rows"][0]["elements"][0]["distance"]["text"]
                distances_in_miles[mode] = distance
            else:
                print("There is no driving route.")
                distances_in_miles[mode] = "N/A"

        else:
            print(f"Request for {mode} mode failed with status code: {response.status_code}")
            distances_in_miles[mode] = "N/A"

    return distances_in_miles  # Convert dictionary to tuple for hashability


import heapq

def dijkstra_with_path(graph, start):
    # Set the initial distances.
    shortest_paths = {vertex: float('infinity') for vertex in graph}
    shortest_paths[start] = 0 
    pred = {vertex: None for vertex in graph}
    
    # Initialize priority queue with the start node (distance, node).
    priority_queue = [(0, start)]
    visited = set()

    # Continue looping as long as the priority queue is not empty.
    while priority_queue:
        new_dist, new_vertex = heapq.heappop(priority_queue)
        if new_vertex in visited:
            continue
        
        # Mark the node as visited.
        visited.add(new_vertex)

        # Explore each neighbor of the current node.
        for neighbor, weight in graph[new_vertex].items():
            dist = new_dist + weight

            if dist < shortest_paths[neighbor]:
                shortest_paths[neighbor] = dist
                pred[neighbor] = new_vertex
                heapq.heappush(priority_queue, (dist, neighbor))

    return shortest_paths, pred




def path_information(predecessor, start, end):
    path = []  # Initialize the path as an empty list.
    current_node = end  # Start with the end node.
    
    # Loop backwards from end to start using the predecessor info.
    while current_node != start:
        path.append(current_node)  # Add the current node to the path.
        current_node = predecessor[current_node] 
    
    path.append(start)
    path.reverse()
    return path


# List of categories and corresponding places
categories_and_places = {
"Transportation": [
{"id": 1, "name": "Portland International Jetport"},
{"id": 2, "name": "Amtrak Downeaster Ticket Office"},
{"id": 3, "name": "Portland Transportation Center Bus Station"},
{"id": 26, "name": "Casco Bay Lines Ferry Terminal"},
{"id": 35, "name": "Greyhound: Bus Stop"}
],
"Art & Culture": [
{"id": 4, "name": "International Cryptozoology Museum"},
{"id": 5, "name": "Children's Museum & Theatre of Maine"},
{"id": 14, "name": "Portland Museum of Art"},
{"id": 15, "name": "State Theatre"},
{"id": 16, "name": "Portland Stage"},
{"id": 22, "name": "Portland Public Library"},
{"id": 23, "name": "Merrill Auditorium"},
{"id": 30, "name": "Portland Observatory"},
{"id": 34, "name": "Maine Jewish Museum"}
],
"Attraction": [
{"id": 6, "name": "Thompson's Point"},
{"id": 7, "name": "James A Banks Sr Portland Exposition Building"},
{"id": 11, "name": "Portland Farmers' Market"},
{"id": 18, "name": "Cross Insurance Arena"},
{"id": 21, "name": "Portland Farmers Market||"}
],
"College/University": [
{"id": 8, "name": "University of Southern Maine"},
{"id": 17, "name": "Maine College of Art & Design"},
{"id": 29, "name": "The Roux Institute at Northeastern University"},
{"id": 39, "name": "Southern Maine Community College"}
],
"Recreation": [
{"id": 9, "name": "Baxter Boulevard"},
{"id": 10, "name": "Back Cove Bay Trail"},
{"id": 12, "name": "Western Promenade"},
{"id": 20, "name": "Congress Street"},
{"id": 24, "name": "Lincoln Park"},
{"id": 25, "name": "Old Port"},
{"id": 27, "name": "Commercial Street"},
{"id": 31, "name": "Fort Allen Park"},
{"id": 32, "name": "East End Beach"},
{"id": 33, "name": "Eastern Promenade"},
{"id": 36, "name": "Fort Williams Park"},
{"id": 38, "name": "Willard Beach"},
{"id": 43, "name": "Peaks Island"}
],
"Historic": [
{"id": 13, "name": "Victoria Mansion"},
{"id": 19, "name": "Maine Historical Society Brown Library"},
{"id": 28, "name": "Maine Narrow Gauge Railroad"},
{"id": 37, "name": "Portland Head Light"},
{"id": 40, "name": "Fort Preble"},
{"id": 41, "name": "South Portland Historical Society"},
{"id": 42, "name": "Bug Light"}
]
}

# Function to list categories and places for the user
def list_categories_and_places():
    for category, places in categories_and_places.items():
        print(f"Category: {category}")
        for place in places:
            print(f"  {place['id']}. {place['name']}")


def recommend_transportation(weather_data, distance, start_node, end_node):
    if start_node == 1:
        return "we recommend using your own car or Uber from Portland Jetport to the next place."
    elif (start_node == 12 and end_node in [36, 38]) or (start_node == 13 and end_node in [36, 38]):
        return "As there is a bridge between this points, we recommend using your own car or public transportation."
    else:
        if weather_data:
            weather_description = weather_data['weather'][0]['description']
            if 'rain' in weather_description.lower() or 'snow' in weather_description.lower():
                if distance < 0.5:
                    return "It's rainy or snowy. We recommend walking and bringing an umbrella."
                else:
                    return "It's rainy or snowy. We recommend taking your own car or public transportation."
            else:
                if distance < 1.0:
                    return "The weather is good. We recommend walking."
                else:
                    return "The weather is good but you can use your own car."
        else:
            return "Weather data not available."


# Main function 
def main():
    configure()
    def search_path():
        start_node = int(start_entry.get())
        end_node = int(end_entry.get())

        api_key_map = os.getenv("GOOGLEMAP_API_KEY") # Google Api key
        distances = get_distances_in_miles(start_node, end_node, api_key_map)
        # Time measurement starts here
        start_time = time.time()

        # Execute Dijkstra
        shortest_paths, pred = dijkstra_with_path(graph, start_node)
        path = path_information(pred, start_node, end_node)

        # Time measurement ends here
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Dijkstra's Algorithm Execution Time: {elapsed_time:.9f} seconds")

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Direct driving distances between the selected attractions:\n")
        for mode, distance in distances.items():
            result_text.insert(tk.END, f"{mode}: {distance}\n")

        shortest_paths, predecessor = dijkstra_with_path(graph, start_node)
        path = path_information(predecessor, start_node, end_node)

        # Find the real names of the start and end points
        start_name = None
        end_name = None
        for category, places in categories_and_places.items():
            for place in places:
                if place['id'] == start_node:
                    start_name = place['name']
                if place['id'] == end_node:
                    end_name = place['name']
                if start_name and end_name:
                    break
            if start_name and end_name:
                break

        if start_name and end_name:
            result_text.insert(tk.END, f"\nShortest path from {start_name} to {end_name} is: {path}\n")
        
        result_text.tag_configure("bold", font=("Arial", 10, "bold"))
        result_text.tag_configure("blue", foreground="blue")
        result_text.insert(tk.END, "\nPlaces visited along this path include:\n", ("bold", "blue"))

        path_with_attractions = []
        for node in path:
            place_found = False
            for category, places in categories_and_places.items():
                for place in places:
                    if place['id'] == node:
                        path_with_attractions.append(place['name'])
                        place_found = True
                        break
                if place_found:
                    break
            if not place_found:
                path_with_attractions.append(f"Node {node}")

        result_text.insert(tk.END, " ---> ".join(path_with_attractions) + "\n")

        api_key_weather = os.getenv("OPENWEATHER_API_KEY") 
        city_id = 4975802  # The city ID for Portland, Maine

        fetched_weather_data = fetch_weather_data(city_id, api_key_weather)
        if fetched_weather_data:
            result_text.tag_configure("bold", font=("Arial", 10, "bold"))
            result_text.tag_configure("blue", foreground="blue")
            result_text.insert(tk.END, "\n\nCurrent weather in Portland, Maine:\n\n", ("bold", "blue"))
            result_text.insert(tk.END, f"Temperature: {fetched_weather_data['main']['temp'] - 273.15:.2f}°C\n")
            result_text.insert(tk.END, f"Humidity: {fetched_weather_data['main']['humidity']}%\n")
            result_text.insert(tk.END, f"Description: {fetched_weather_data['weather'][0]['description']}\n")
        else:
            result_text.insert(tk.END, "Failed to fetch weather data.\n")


        result_text.tag_configure("bold", font=("Arial", 10, "bold"))
        result_text.tag_configure("blue", foreground="blue")
        result_text.insert(tk.END, "\n\nTransportation Recommendations:\n\n", ("bold", "blue"))

        for i in range(len(path) - 1):
            start = path[i]
            end = path[i + 1]
            distance = graph[start][end]

            start_name = None
            end_name = None
            for category, places in categories_and_places.items():
                for place in places:
                    if place['id'] == start:
                        start_name = place['name']
                    if place['id'] == end:
                        end_name = place['name']
                    if start_name and end_name:
                        break
                if start_name and end_name:
                    break

            recommendation = recommend_transportation(fetched_weather_data, distance, start, end)
            result_text.insert(tk.END, f"From {start_name} to {end_name}: {recommendation} (Distance: {distance} miles)\n\n")

    def show_categories():
        category_window = tk.Toplevel(window)
        category_window.title("Categories and Places")

        category_text = tk.Text(category_window, wrap=tk.WORD)
        category_text.pack(expand=True, fill=tk.BOTH)

        for category, places in categories_and_places.items():
            category_text.insert(tk.END, f"Category: {category}\n")
            for place in places:
                category_text.insert(tk.END, f"  {place['id']}. {place['name']}\n")
            category_text.insert(tk.END, "\n")

        category_text.configure(state=tk.DISABLED)

    window = tk.Tk()
    window.title("Portland Travel And Recommendation System")
    window.geometry("600x400")  
    window.configure(bg="#F0F0F0")  

    start_label = tk.Label(window, text="Start Point:")
    start_label.pack()
    start_entry = tk.Entry(window)
    start_entry.pack()

    end_label = tk.Label(window, text="End Point:")
    end_label.pack()
    end_entry = tk.Entry(window)
    end_entry.pack()

    search_button = tk.Button(window, text="Search", command=search_path)
    search_button.pack()

    category_button = tk.Button(window, text="Show Categories and Places", command=show_categories)
    category_button.pack()

    result_text = tk.Text(window, wrap=tk.WORD)
    result_text.pack(expand=True, fill=tk.BOTH)

    window.mainloop()


if __name__ == "__main__":
    main()    