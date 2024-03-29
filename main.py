from packages import PackageLoader
from distances import DistanceLoader

packages_csv_file = "WGUPS_Package_File.csv"
package_loader = PackageLoader()
hash_table = package_loader.load_packages(packages_csv_file)

# Example usage of lookup method
package_id = 39
package_info = hash_table.lookup(package_id)  # Lookup package with ID 1
if package_info:
    print(f"Package found: {package_info}")
else:
    print("Package not found.")

distances_csv_file = "WGUPS_Distance_Table.csv"
distance_loader = DistanceLoader()
distances = distance_loader.load_distances(distances_csv_file)

# Example usage
source = "4001 South 700 East"
destination = "1060 Dalton Ave S"
distance = distances[source][destination]
print(f"Distance from {source} to {destination}: {distance} miles")

