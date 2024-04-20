# Lauren March
# Student ID: 001421111

import csv
import datetime
from colorama import Fore, Style


# HashTable class to create hashmap with chaining to handle collisions
# Create insert and lookup functions for packages to be stored and accessed.
class HashTable:
    # Constructor for hashmap, allocates 40 empty buckets into a list
    # Each bucket is an empty list to handle collisions via chaining
    def __init__(self):
        self.size = 40
        self.map = [[] for _ in range(self.size)]

    # Simple custom hash function that stores packages by ID % 40
    def packages_hash(self, key):
        return key % self.size
    
    # Inse
    def insert(self, key, item):
        bucket = self.packages_hash(key)
        bucket_list = self.map[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True
        bucket_list.append([key, item])
        return True

    def search(self, key):
        bucket = self.packages_hash(key)
        bucket_list = self.map[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

# Creating a package class that includes all required package info
class Packages:
    def __init__(self, ID, street, city, state, zip_code, deadline, weight, notes, status, departure_time, delivery_time):
        self.ID = ID
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def __str__(self):
        return f"ID: {self.ID}, {self.street}, {self.city}, {self.state}, {self.zip_code}, Deadline: {self.deadline}, {self.weight}, {self.status}, Departure Time: {self.departure_time}, Delivery Time: {self.delivery_time}"

    # Will update the status of packages from "At the Hub" to "En-Route" to "Delivered" at appropriate datetime
    def status_update(self, time_change):
        if self.delivery_time is None:
            self.status = "At the hub"
        elif time_change < self.departure_time:
            self.status = "At the hub"   
        elif time_change < self.delivery_time:
            self.status = "En route"     
        else:
            self.status = "Delivered" 
        if self.ID == 9 and time_change > datetime.timedelta(hours=10, minutes=20):
            self.street = "410 S State St"  
            self.zip_code = "84111"    

# Creating truck class with all required attributes
class Trucks:
    def __init__(self, speed, miles, current_location, depart_time, packages):
        self.speed = speed
        self.miles = miles
        self.current_location = current_location
        self.time = depart_time
        self.depart_time = depart_time
        self.packages = packages

    def __str__(self):
        return f"{self.speed},{self.miles},{self.current_location},{self.time},{self.depart_time},{self.packages}"

# Function to read AddressCSV and load into 2D array
def address(address):
    for row in AddressCSV:
        if address in row[2]:
           return int(row[0])

# This function is the distance matrix for the distance between 2 addresses 
def between(address1, address2):
    distance = DistanceCSV[address1][address2]
    if distance == '':
        distance = DistanceCSV[address2][address1]
    return float(distance)

# This loads the package info into the hash table create from HashTable class
# This uses the p_id as the key, and the rest of the package info as the value pair
def load_package_data(filename):
    with open(filename) as package_file:
        package_info = csv.reader(package_file, delimiter=',')
        next(package_info)
        for package in package_info:
            p_id = int(package[0])
            p_street = package[1]
            p_city = package[2]
            p_state = package[3]
            p_zip = package[4]
            p_deadline = package[5]
            p_weight = package[6]
            p_notes = package[7]
            p_status = "At the Hub"
            p_departure_time = None
            p_delivery_time = None

            p = Packages(p_id, p_street, p_city, p_state, p_zip, p_deadline, p_weight, p_notes, p_status, p_departure_time, p_delivery_time)
            package_hash.insert(p_id, p)

# This is the variation of the nearest neighbor algo for delivering packages
def select_next_package(current_location, packages):
    min_distance = float('inf')
    closest_package = None
    for package in packages:
        distance_to_package = between(address(current_location), address(package.street))
        if distance_to_package < min_distance:
            min_distance = distance_to_package
            closest_package = package
    return closest_package

# Stores packages on trucks in list by search function to find p_ids 
# Uses nearest neighbor algo to deliever packages
# Tells truck1 to return to hub so truck2 can depart with truck1's driver
def truck_deliver_packages(truck):
    en_route = []
    for package_id in truck.packages:
        package = package_hash.search(package_id)
        en_route.append(package)

    truck.packages.clear()
    while len(en_route) > 0:
        next_package = select_next_package(truck.current_location, en_route)
        en_route.remove(next_package)
        distance_to_next = between(address(truck.current_location), address(next_package.street))
        truck.miles += distance_to_next
        truck.current_location = next_package.street
        truck.time += datetime.timedelta(hours=distance_to_next / truck.speed)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time

    # Truck1 should return to the hub after deliveries   
    if truck.depart_time == datetime.timedelta(hours=8):
        
        # Adding return trip to hub to toal miles
        truck.miles += between(address(truck.current_location), address("4001 South 700 East"))  
        truck.current_location = "4001 South 700 East"

def main():
    # Made these global so they can be accessed outside of their scope
    global AddressCSV, DistanceCSV, package_hash
    
    # Open both csvs using the csv library
    with open("WGUPS_Addresses.csv") as address_csv:
        global AddressCSV
        AddressCSV = csv.reader(address_csv)
        AddressCSV = list(AddressCSV)
    with open("WGUPS_Distances.csv") as distance_csv:
        global DistanceCSV
        DistanceCSV = csv.reader(distance_csv)
        DistanceCSV = list(DistanceCSV)

    # Initializing the HashTable() function in order to call class methods further below
    package_hash = HashTable()
    load_package_data('WGUPS_Packages.csv')

    # Loading the trucks manually for simplicity
    truck1 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8), [1, 13, 14, 15, 16, 19, 20, 25, 27, 29, 30, 34, 37, 40])
    truck2 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=11), [2, 3, 4, 5, 9, 18, 26, 28, 32, 35, 36, 38])
    truck3 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5), [6, 7, 8, 10, 11, 12, 17, 21, 22, 23, 24, 31, 33, 39])

    # Trucks sent out for delivery, handles the need for truck1 to come back to hub
    truck_deliver_packages(truck1)
    truck_deliver_packages(truck3)
    truck2.depart_time = min(truck1.time, truck3.time)
    truck_deliver_packages(truck2)

    header = Fore.CYAN + 'Welcome to Western Governors University Parcel Service!' + Style.RESET_ALL
    print(f'{header}')

    # Made this a continuous loop until the user would like to end the program
    # This way a user can get multiple packages/times without having to restart program
    while True:
        user_input = input(Fore.LIGHTBLACK_EX + "Please enter a time (HH:MM), or enter 'exit' to quit: " + Style.RESET_ALL)
        
        # Check if the user wants to exit program
        # This will print the total_miles for every truck
        if user_input.lower() == 'exit' or user_input.lower() == 'quit':
            total_miles = truck1.miles + truck2.miles + truck3.miles
            print(Fore.LIGHTBLUE_EX + f'The total miles traveled by all trucks is: {total_miles:.2f}', Style.RESET_ALL)
            print("Exiting the program.")
            break
        
        # Error handling 
        try:
            if user_input:
                (h, m) = user_input.split(":")
                hours = int(h)
                minutes = int(m)
                
                # Check if hours and minutes are within valid ranges
                if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
                    raise ValueError("Invalid time. Hours must be between 0 and 23, and minutes must be between 0 and 59.")
                
                time_change = datetime.timedelta(hours=hours, minutes=minutes)
            else:
                time_change = None
                print(Fore.YELLOW + "No time entered. Continuing without time change." + Style.RESET_ALL)

            # Error handling for invalid user input str when int needed or 'Enter' is pressed
            # Will print all packages if invalid str or 'Enter' entered 
            try:
                single_entry = [int(input("Please enter a Package ID, or hit 'Enter' to view all."))]
            except ValueError:
                single_entry = range(1, 41)

            print(f"{'ID':<5} {'Address':<45} {'City':<20} {'State':<10} {'Zip Code':<15} "
                f"{'Status':<15} {'Deadline':<15} {'Departure Time'}")

            # Uses search to search through packages until user input ID is found
            # Once found info for that package will be output
            # If invalid interger value then "Package ID not found." will be output
            for package_id in single_entry:
                package = package_hash.search(package_id)
                if package is None:
                    print(Fore.RED + "Package ID not found." + Style.RESET_ALL)
                else:
                    package.status_update(time_change)
                    id_color = Fore.MAGENTA if package.status == "Delivered" else Fore.WHITE
                    status_color = Fore.GREEN if package.status == "Delivered" else Fore.YELLOW if package.status == "En route" else Fore.RED
                    print(f"{id_color}{package.ID:<5}{Style.RESET_ALL} "
                        f"{package.street:<45} {package.city:<20} {package.state:<10} {package.zip_code:<15} "
                        f"{status_color}{package.status:<15}{Style.RESET_ALL} "
                        f"{package.deadline:<15} {package.departure_time}")
                    

        except ValueError as e:
            print(Fore.RED + str(e) + Style.RESET_ALL)



if __name__ == "__main__":
    main()
