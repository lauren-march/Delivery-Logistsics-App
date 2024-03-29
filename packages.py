import csv
from data_structures import HashTable

class PackageLoader:
    @staticmethod
    def load_packages(file_name):
        hash_table = HashTable(size=40)  # Adjust the size as per your needs
        with open(file_name, 'r', newline='', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                package_id = int(row[0])
                street_address = row[1]
                city = row[2]
                state = row[3]
                zip_code = row[4]
                time_of_delivery = row[5]
                weight = int(row[6])

                # Assuming package_id is unique and used as the key for the hash table
                package_info = (street_address, city, state, zip_code, time_of_delivery, weight)
                hash_table.insert(package_id, package_info)

        return hash_table