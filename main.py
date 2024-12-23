import itertools
import math
import time
import random

# Menghitung jarak Haversine antara dua titik
def haversine_distance(point1, point2):
    R = 6371.0  # Radius bumi dalam kilometer
    lat1, lon1 = point1
    lat2, lon2 = point2
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# Menghitung total jarak dari jalur
def total_distance(route, locations):
    distance = 0
    for i in range(len(route) - 1):
        distance += haversine_distance(locations[route[i]], locations[route[i + 1]])
    distance += haversine_distance(locations[route[-1]], locations[route[0]])  # Kembali ke titik awal
    return distance

# Menghitung waktu tempuh dalam jam berdasarkan jarak dan kecepatan rata-rata
def calculate_travel_time(distance_km, speed_kmh):
    return distance_km / speed_kmh

# Algoritma Brute Force Iteratif
def brute_force_tsp_iterative(locations, start_location):
    iteration_count = 0
    location_names = list(locations.keys())
    location_names.remove(start_location)
    permutations = list(itertools.permutations(location_names))

    min_route = None
    min_distance = float('inf')

    for perm in permutations:
        iteration_count += 1
        route = [start_location] + list(perm) + [start_location]
        distance = total_distance(route, locations)
        if distance < min_distance:
            min_distance = distance
            min_route = route

    return min_route, min_distance, iteration_count

# Algoritma Greedy Iteratif
def greedy_tsp_iterative(locations, start_location):
    iteration_count = 0
    location_names = list(locations.keys())
    location_names.remove(start_location)

    route = [start_location]

    while location_names:
        iteration_count += 1
        last_location = route[-1]
        next_location = min(location_names, key=lambda x: haversine_distance(locations[last_location], locations[x]))
        route.append(next_location)
        location_names.remove(next_location)

    route.append(start_location)  # Kembali ke titik awal
    return route, total_distance(route, locations), iteration_count

def generate_random_locations(num_locations):
    locations = {}
    for i in range(num_locations):
        locations[f"Location {i + 1}"] = (
            random.uniform(-90, 90),  # Latitude
            random.uniform(-180, 180)  # Longitude
        )
    return locations

def run_tsp(locations, start_location, average_speed_kmh):
    print(f"\nRunning TSP for {len(locations)} locations starting from {start_location}\n")

    # Perbandingan eksekusi Brute Force (hanya untuk kasus kecil)
    if len(locations) <= 10:
        start_time = time.perf_counter()
        brute_force_result, brute_force_distance, brute_force_iterations = brute_force_tsp_iterative(locations, start_location)
        brute_force_time = time.perf_counter() - start_time

        brute_force_travel_time = calculate_travel_time(brute_force_distance, average_speed_kmh)

        print("## Brute Force Result ##")
        print("Route: ", brute_force_result)
        print("Distance: ", brute_force_distance, "km")
        print("Estimated Travel Time: ", brute_force_travel_time, "hours")
        print("Iterations: ", brute_force_iterations)
        print("Time: {:.10f} seconds".format(brute_force_time))
    else:
        print("Brute Force tidak bisa dijalankan karena waktu yang sangat lama.")

    # Perbandingan eksekusi Greedy
    start_time = time.perf_counter()
    greedy_result, greedy_distance, greedy_iterations = greedy_tsp_iterative(locations, start_location)
    greedy_time = time.perf_counter() - start_time

    greedy_travel_time = calculate_travel_time(greedy_distance, average_speed_kmh)

    print("\n## Greedy Result ##")
    print("Route: ", greedy_result)
    print("Distance: ", greedy_distance, "km")
    print("Estimated Travel Time: ", greedy_travel_time, "hours")
    print("Iterations: ", greedy_iterations)
    print("Time: {:.10f} seconds".format(greedy_time))

if __name__ == "__main__":
    input_sizes = [1, 5, 10, 15, 20]  # Jumlah lokasi yang akan diuji

    for size in input_sizes:
        locations = generate_random_locations(size)
        start_location = list(locations.keys())[0]
        run_tsp(locations, start_location, 40)
