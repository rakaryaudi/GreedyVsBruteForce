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

# Global counter untuk rekursi
brute_force_counter = 0
greedy_counter = 0

# Algoritma Brute Force Rekursif
def brute_force_tsp_recursive(current_location, remaining_locations, locations, current_route, current_distance):
    global brute_force_counter
    brute_force_counter += 1

    if not remaining_locations:  # Jika tidak ada lokasi tersisa
        current_route.append(start_location)
        current_distance += haversine_distance(locations[current_location], locations[start_location])
        return current_route, current_distance

    min_route = None
    min_distance = float('inf')

    for next_location in remaining_locations:
        next_distance = haversine_distance(locations[current_location], locations[next_location])
        route, distance = brute_force_tsp_recursive(
            next_location,
            [loc for loc in remaining_locations if loc != next_location],
            locations,
            current_route + [next_location],
            current_distance + next_distance
        )
        if distance < min_distance:
            min_distance = distance
            min_route = route

    return min_route, min_distance

# Algoritma Greedy Rekursif
def greedy_tsp_recursive(current_location, remaining_locations, locations, current_route, current_distance):
    global greedy_counter
    greedy_counter += 1

    if not remaining_locations:  # Jika tidak ada lokasi tersisa
        current_route.append(start_location)
        current_distance += haversine_distance(locations[current_location], locations[start_location])
        return current_route, current_distance

    next_location = min(remaining_locations, key=lambda x: haversine_distance(locations[current_location], locations[x]))
    next_distance = haversine_distance(locations[current_location], locations[next_location])

    return greedy_tsp_recursive(
        next_location,
        [loc for loc in remaining_locations if loc != next_location],
        locations,
        current_route + [next_location],
        current_distance + next_distance
    )

def generate_random_locations(num_locations):
    locations = {}
    for i in range(num_locations):
        locations[f"Location {i + 1}"] = (
            random.uniform(-90, 90),  # Latitude
            random.uniform(-180, 180)  # Longitude
        )
    return locations

def run_tsp(locations, start_location, average_speed_kmh):
    global brute_force_counter, greedy_counter

    brute_force_counter = 0
    greedy_counter = 0

    print(f"\nRunning TSP for {len(locations)} locations starting from {start_location}\n")

    # Perbandingan eksekusi Brute Force (hanya untuk kasus kecil)
    if len(locations) <= 10:
        start_time = time.perf_counter()
        brute_force_result, brute_force_distance = brute_force_tsp_recursive(
            start_location, [loc for loc in locations if loc != start_location], locations, [start_location], 0
        )
        brute_force_time = time.perf_counter() - start_time

        brute_force_travel_time = calculate_travel_time(brute_force_distance, average_speed_kmh)

        print("## Brute Force Result ##")
        print("Route: ", brute_force_result)
        print("Distance: ", brute_force_distance, "km")
        print("Estimated Travel Time: ", brute_force_travel_time, "hours")
        print("Rekursi Count: ", brute_force_counter)
        print("Time: {:.10f} seconds".format(brute_force_time))
    else:
        print("Brute Force tidak bisa dijalankan karena waktu yang sangat lama.")

    # Perbandingan eksekusi Greedy
    start_time = time.perf_counter()
    greedy_result, greedy_distance = greedy_tsp_recursive(
        start_location, [loc for loc in locations if loc != start_location], locations, [start_location], 0
    )
    greedy_time = time.perf_counter() - start_time

    greedy_travel_time = calculate_travel_time(greedy_distance, average_speed_kmh)

    print("\n## Greedy Result ##")
    print("Route: ", greedy_result)
    print("Distance: ", greedy_distance, "km")
    print("Estimated Travel Time: ", greedy_travel_time, "hours")
    print("Rekursi Count: ", greedy_counter)
    print("Time: {:.10f} seconds".format(greedy_time))

if __name__ == "__main__":
    input_sizes = [1, 5, 10, 15, 20]  # Jumlah lokasi yang akan diuji

    for size in input_sizes:
        locations = generate_random_locations(size)
        start_location = list(locations.keys())[0]
        run_tsp(locations, start_location, 40)
