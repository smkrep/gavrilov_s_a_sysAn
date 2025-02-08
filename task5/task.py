import json
import numpy as np

def calculate_matrix(A):
    rankings = {}
    for index in range(len(A)):
        if type(A[index]) is list:
            for elem in A[index]:
                rankings[elem] = index
        else:
            rankings[A[index]] = index
    
    Y_a = []
    for i in range(1,len(rankings) + 1):
        row = []
        for key, _ in rankings.items():
            if rankings[key] >= rankings[i]:
                row.append(1)
            else:
                row.append(0)
        Y_a.append(row)

    return Y_a

def calculate_K(Y_a, Y_b):
    Y_a, Y_b = np.array(Y_a), np.array(Y_b)
    Y_AB = Y_a * Y_b
    Y_AB_t = Y_a.transpose() * Y_b.transpose()
    K = np.logical_or(Y_AB, Y_AB_t)
    print(K)



def main(A, B):
    pass



A = [1,[2,3],4,[5,6,7],8,9,10]
B = [[1,2],[3,4,5,],6,7,9,[8,10]]

Y_a = calculate_matrix(A)
Y_b = calculate_matrix(B)

calculate_K(Y_a, Y_b)