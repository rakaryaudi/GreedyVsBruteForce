import itertools
import math
import time

# Lokasi dalam bentuk koordinat latitude dan longitude.
locations = {
    'Telkom University': (-6.972946, 107.63314),
    'Bojongsoang': (-6.9150085, 106.972504),
    'Pasteur': (-6.900347, 107.600725),
    'Batununggal': (-6.952957, 107.637493),
    'Gedebage': (-6.941167, 107.689832),
    'Cijawura': (-6.955268, 107.650417),
    'Moh Toha': (-6.952243, 107.610419),
    'Kopo': (-6.945768, 107.589692),
    'Pasil Kaliki': (-6.906616, 107.59763)
}

# Titik awal dan titik kembali
start_location = 'Telkom University'

# Kecepatan rata-rata kendaraan (km/jam)
average_speed_kmh = 40

# Menghitung jarak Haversine antara dua titik
def haversine_distance(point1, point2):
    # Radius bumi dalam kilometer
    R = 6371.0

    lat1, lon1 = point1
    lat2, lon2 = point2

    # Menghitung perbedaan koordinat dalam radian
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Menghitung jarak dalam kilometer
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

# Algoritma Brute Force
def brute_force_tsp(locations, start_location):
    location_names = list(locations.keys())
    location_names.remove(start_location)

    permutations = list(itertools.permutations(location_names))

    # Mencari jalur terpendek
    min_route = None
    min_distance = float('inf')
    k = 0
    for perm in permutations:
        route = [start_location] + list(perm) + [start_location]
        distance = total_distance(route, locations)
        k += 1
        if distance < min_distance:
            min_distance = distance
            min_route = route
    return min_route, min_distance, k

# Algoritma Greedy
def greedy_tsp(locations, start_location):
    location_names = list(locations.keys())
    location_names.remove(start_location)

    route = [start_location]
    k = 0

    while location_names:
        last_location = route[-1]
        next_location = min(location_names, key=lambda x: haversine_distance(locations[last_location], locations[x]))
        route.append(next_location)
        location_names.remove(next_location)
        k += 1

    route.append(start_location)  # Kembali ke titik awal
    return route, total_distance(route, locations), k

print("\nCOMPARISON\n")
# Perbandingan eksekusi Brute Force
start_time = time.time()
brute_force_result, brute_force_distance, brute_force_k = brute_force_tsp(locations, start_location)
brute_force_time = time.time() - start_time

brute_force_travel_time = calculate_travel_time(brute_force_distance, average_speed_kmh)

print("## Brute Force Result ##")
print("Route: ", brute_force_result)
print("Distance: ", brute_force_distance, "km")
print("Estimated Travel Time: ", brute_force_travel_time, "hours")
print("Iterations (k): ", brute_force_k)
print("Time: ", brute_force_time, "seconds")

# Perbandingan eksekusi Greedy
start_time = time.time()
greedy_result, greedy_distance, greedy_k = greedy_tsp(locations, start_location)
greedy_time = time.time() - start_time

greedy_travel_time = calculate_travel_time(greedy_distance, average_speed_kmh)

print("\n## Greedy Result ##")
print("Route: ", greedy_result)
print("Distance: ", greedy_distance, "km")
print("Estimated Travel Time: ", greedy_travel_time, "hours")
print("Iterations (k): ", greedy_k)
print("Time: ", greedy_time, "seconds")
