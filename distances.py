import csv
from data_structures import HashTable


class DistanceLoader:
    @staticmethod
    def load_distances(file_name):
        distances = {}

        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # Skip the header row

            for row in reader:
                source = row[0]
                distances[source] = {}

                for i, distance in enumerate(row[1:], start=1):
                    destination = headers[i]
                    distances[source][destination] = float(distance) if distance else 0.0

        return distances
