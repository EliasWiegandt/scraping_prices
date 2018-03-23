import csv
import os


def load_names():
    print(os.getcwd())
    products = []
    filepath = os.path.join(os.getcwd(), 'products/names.csv')
    with open(filepath) as f:
        links_csv = csv.DictReader(f, skipinitialspace=True)
        for row in links_csv:
            products.append(row['product'])
    return products
