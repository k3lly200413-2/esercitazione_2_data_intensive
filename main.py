import numpy as np
import os.path
from urllib.request import urlretrieve
from zipfile import ZipFile
import csv


def read_file(fileName, tupleFormat=False):
    with open(fileName, "r") as f:
        reader = csv.reader(f, delimiter=";")
        if not tupleFormat:
            readFile = {int(uid): name for uid, name in reader}
        else:
            readFile = set(
                (int(uid), iid)
                for uid, iid
                in reader
            )
        return readFile

def setup_file():
    users = read_file("users.csv")
    items = read_file("items.csv")
    purchaseSet = read_file("purchases-2000.csv", "true")
    return users, items, purchaseSet

def get_array_len(matrix):
    return len(matrix)

def create_indices(dictionary):
    return {uid: lineIndex for lineIndex, uid in enumerate(sorted(dictionary.keys()))}

def create_purchases(columnSize, rowSize):
    return np.zeros((get_array_len(columnSize), 
                    get_array_len(rowSize)),
                   dtype=int)

"""def create_item_indices():
    return {iid: lineIndex for lineIndex, iid in enumerate(sorted(items.keys()))}
"""
def main():
    if not os.path.exists("purchases_data.zip"):
        urlretrieve("https://git.io/fhxQh", "purchases_data.zip")
    
    with ZipFile("purchases_data.zip") as f:
        f.extractall()        
    users, items, purchaseSet = setup_file()
    userIndices = create_indices(users)
    itemIndices = create_indices(items)
    create_purchases(userIndices, itemIndices)
    print(create_purchases(userIndices, itemIndices))
    
if __name__ == "__main__":
    main()
