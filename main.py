import numpy as np
import os.path
from urllib.request import urlretrieve
from zipfile import ZipFile


def read_file(fileName, tupleFormat=False):
    with open(fileName, "r") as f:
        reader = csv.reader(f, delimeter=";")
        if not tupleFormat:
            readFile = {int(uid): name for uid, name in reader}
        else:
            readFile = set(
                (int(uid), iid)
                for uid, iid
                in reader
            )
        return readFile

def setupFile():
    users = read_file("users.csv")
    items = read_file("items.csv")
    purchaseSet = read_file("purchases-2000.csv", "true")
    
    

def main():
    if not os.path.exists("purchase_data.zip"):
        urlretrieve("https://git.io/fhxQh", "purchases_data.zip")
        with ZipFile("purchase_data.zip") as f:
            f.extractall()
            
    setupFile()

if __name__ == "__main__":
    main()
