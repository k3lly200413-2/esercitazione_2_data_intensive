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
                            arrayFilter):
    return matrixToExtractFrom[arrayFilter]

def sum_elements(matrix):
    return matrix.sum()

# axis 0 = row, axis 1 = columns
def sum_elements(matrix, axis=0):
    return matrix.sum(axis)

def similarity(array1, array2):
    # we could do this different ways, this way only checks if they both are True
    # return array1 & array2
        # if we have 0s and 1s we can multiply them together
    # return array1 * array2
        # we can then get the number of 1s using sum
    # return np.sum(array1 * array2)
    
    # all of this is made into a function called np.dot(...)
    # return np.dot(array1, array2)
    # or 
    # return array1.dot(array2) 
    # we can also use @
    return array1 @ array2

def similarity_matrix(matrix1, matrix2):
    # We need a similarity matrix NxN with all the similarities between all entries in purchases
    # similarity[i, j] ==  purchases[i, :] @ purchases[:, j]
    # Matrix product returns the product of ones lines for the others columns
    # (A @ B)[i, j] == A[i, :] @ B[:, j]
    # We can also just use the transposed of the second matrix
    pass
    # return (matrix1 @ matrix2.T)[i, j] == matrix1[1, :] @ matrix2[:, j]

def similarity_matrix(matrix):
    return matrix @ matrix.T
def check_if_symmetric(matrix):
    # return (matrix == matrix.T).all()
    # Safer way to run this we can use: array_equal
    return np.array_equal(matrix, matrix.T)

def change_diagonal(matrix, numberToReplaceDiagonalWith):
    np.fill_diagonal(matrix, numberToReplaceDiagonalWith)

def get_max_common_product_with_user(matrix, uIndex):
    return matrix[uIndex].max()

def sort_by_args(array, row=1):
    # argsort just returns the position of the numbers that allow the array to be sorted
    # if we have x = np.array([320, 80, 20, 40, 160, 640, 10])
    # with argsort we would get array([6, 2, 3, 1, 4, 0, 5])#
    if array.ndim > 1:
        print(True)
        return array.argsort(row)
    return array.argsort()

def populate_updated_matrix(oldMatrix):
    return np.zeros_like(oldMatrix)

def XOR(matrix, matrix2):
    return matrix ^ matrix2

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
    
    # print(purchases)
    
    """print(item_purchases[:5])
    for user in userIndices.values():
        print(purchased_by_specific_user(purchases, user).mean())
    
    print(item_purchases.max())
    
    print(userNames[np.where(user_purchases == user_purchases.max())[0][0]])
    
    users_more_than_50_purchases = (user_purchases >= 50)
    print(sum_elements(users_more_than_50_purchases))
    
    print(sum_elements(item_purchases >= 35))
    """
    # print(similarity(purchases[0], purchases[1]))
    
    
    # When slicing the matrix you will call matrix[person1, person2]
    # This will tell you how many items both people have pruchesed
    # print(similarity_matrix(purchases)[:10, :10])
    
    # print(check_if_symmetric(similarity_matrix(purchases)))
    similarityMatrix = similarity_matrix(purchases)
    change_diagonal(similarityMatrix, 0)
    # print(similarityMatrix.max())
    
    # print(get_max_common_product_with_user(similarityMatrix, userIndices[7661]))
    
    # print(similarityMatrix[1])
    
    # Interesse stimato del primo utente verso il secondo prodotto
    # print(similarityMatrix[0] @ purchases[:, 1])
    
    interest = similarityMatrix @ purchases
    
    """print(interest.shape == purchases.shape)"""
    
    interest[purchases_bool] = 0
    
    # TEST
    assert interest[0, 0] == 0
    assert interest[3, 3] == 8
    assert interest[-4, 10] == 0
    assert interest[-2, 12] == 0
    assert interest[-1, -1] == 5
    print("OK")
    
    interest_rangking_user_0 = sort_by_args(sort_by_args(-interest[0]))
    
    interest_rangking_user_0 = interest_rangking_user_0 < 20
        
    interest_rangking = sort_by_args(sort_by_args(-interest))
    
    suggestions = interest_rangking < 20 
    
    assert suggestions[0, 0] == False
    assert suggestions[0, 170] == True
    assert suggestions[1, 400] == True
    assert suggestions[1, 570] == False
    print("OK")
    
    purchases_update = populate_updated_matrix(purchases)
    
    with open("purchases-2014.csv", "r") as f:
        reader = csv.reader(f, delimiter=";")
        for uid, iid in reader:
            purchases_update[userIndices[int(uid)], itemIndices[int(iid)]] = 1
    
    new_purchases = XOR(purchases, purchases_update).astype(bool)
    hits = suggestions & new_purchases
    
    print(hits.any(1).sum())
    print(hits.any(1).mean() * 100)
    
    
    
    np.random.seed(123)
    random_interest = np.random.random(interest.shape)
    
    random_interest[purchases_bool] = 0
    
    random_interest_ranking = sort_by_args(sort_by_args(- random_interest))
    
    random_suggestions = random_interest_ranking < 20
    
    random_hits = random_suggestions & new_purchases
    randomly_satisfied_users = random_hits.any(1)
    
    print(randomly_satisfied_users)
    
    print(round(randomly_satisfied_users.mean() * 100))
    
if __name__ == "__main__":
    main()
