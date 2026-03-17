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


def create_indices(dictionary):
    return {uid: lineIndex for lineIndex, uid in enumerate(sorted(dictionary.keys()))}

"""def create_item_indices():
    return {iid: lineIndex for lineIndex, iid in enumerate(sorted(items.keys()))}
"""
def main():
    if not os.path.exists("purchases_data.zip"):
        urlretrieve("https://git.io/fhxQh", "purchases_data.zip")
    
    with ZipFile("purchases_data.zip") as f:
        f.extractall()        
    users, items, purchaseSet = setup_file()
    itemIndices = create_user_indices(items)
    userIndices = create_user_indices(users)
    print(userIndices[63776])

if __name__ == "__main__":
    main()
