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
    purchaseSet = read_file("purchases-2000.csv", True)
    return users, items, purchaseSet

def get_array_len(matrix):
    return len(matrix)

def create_indices(dictionary):
    return {uid: lineIndex for lineIndex, uid in enumerate(sorted(dictionary.keys()))}

def create_purchases(columnSize, rowSize):
    return np.zeros((get_array_len(columnSize), 
                    get_array_len(rowSize)),
                   dtype=int)

def populate_purchase(userIndices, itemIndices, purchases, purchaseSet):
    for couple in purchaseSet:
        purchases[userIndices[couple[0]], itemIndices[int(couple[1])]] = 1

def convert_to_bool(matrixToConvert):
    return matrixToConvert.astype(bool)

def create_user_names_vector(nUsers):
    return np.empty(nUsers, dtype=object)

def purchased_by_specific_user(matrix, uID):
    return matrix[uID] # Also possible to use [uID, :]

def get_first_n_elements(matrix, nElements):
    return matrix[:nElements]

def get_elements_from_array(matrixToExtractFrom, 
                            arrayFilter
                            ):
    return matrixToExtractFrom[arrayFilter]

def sum_elements(matrix):
    return matrix.sum()

# axis 0 = row, axis 1 = columns
def sum_elements(matrix, axis=0):
    return matrix.sum(axis)
    
def main():
    if not os.path.exists("purchases_data.zip"):
        urlretrieve("https://git.io/fhxQh", "purchases_data.zip")
    
    with ZipFile("purchases_data.zip") as f:
        f.extractall()        
    users, items, purchaseSet = setup_file()
    
    # userIndices = UserID, index
    userIndices = create_indices(users)
    # itemIndices = ItemID, index
    itemIndices = create_indices(items)

    purchases = create_purchases(userIndices, itemIndices)
    # print(itemIndices.items())
    
    populate_purchase(userIndices, itemIndices, purchases, purchaseSet)
    
    purchases_bool = convert_to_bool(purchases)
    
    userNames = create_user_names_vector(get_array_len(userIndices))
    
    userNames = np.array([users[name] for name in userIndices])
    
    itemNames = np.array([items[item] for item in itemIndices])
    
    # print(user_names)
    
    # TEST
    assert userNames[0] == "malachix"
    assert itemNames[0] == "Age of Innocence [VHS]"
    assert purchases[0, 0] == 0
    assert purchases[-4, 10] == 1
    assert purchases[-2, 12] == 1
    assert purchases[-1, -1] == 0
    print("OKAY")

    user_purchases = sum_elements(purchases, 1)
    item_purchases = sum_elements(purchases, 0)
    
    print(user_purchases[:10])
    print(item_purchases[:10])
    
if __name__ == "__main__":
    main()
