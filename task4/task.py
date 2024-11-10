import numpy as np
from math import log2

#Функция, подсчитывающая энтропию на заданном массиве вероятностей
def calculate_enthropy(probabilities):
    enthropy = 0

    for prob in np.nditer(probabilities):
        enthropy -= prob * log2(prob)

    return enthropy

#Функция, вычисляющая энтропию совместного события и количество информации
def main(input_matrix):
    
    initial_matrix = np.array(input_matrix)

    amount_of_purchases = initial_matrix.sum()

    compatible_event_prob_matrix = initial_matrix / amount_of_purchases

    p_y_vector = compatible_event_prob_matrix.sum(axis=1) #Суммарная вероятность по возрастной группе
    p_x_vector = compatible_event_prob_matrix.sum(axis=0) #Суммарная вероятность по категории товара
    
    H_XY = calculate_enthropy(compatible_event_prob_matrix)
    H_Y = calculate_enthropy(p_y_vector)
    H_X = calculate_enthropy(p_x_vector)
    
    conditional_prob_matrix = np.copy(compatible_event_prob_matrix)
    overall_conditional_H = 0
    
    for row_index in range(len(compatible_event_prob_matrix)):
        conditional_prob_matrix[row_index] /= p_y_vector[row_index]
        conditional_H = calculate_enthropy(conditional_prob_matrix[row_index])    
        overall_conditional_H += conditional_H * p_y_vector[row_index]

    information_quantity = H_X - overall_conditional_H

    H_XY_through_sum = H_Y + overall_conditional_H # Это значение должно быть равно H_XY, которое посчитали ранее

    print(f"Количество информации I(X,Y): {round(information_quantity, 2)}")
    print(f"Энтропия совместного события H(XY): {round(H_XY_through_sum, 2)} (для обоих способов расчета)")

    
#По строкам находятся возрастные группы, по столбцам - категории товаров, в ячейке - количество товаров определенной категории,
#купленных определенной возрастной группы
test_matrix = [[20, 15, 10, 5],
               [30, 20, 15, 10],
               [25, 25, 20, 15],
               [20, 20, 25, 20],
               [15, 15, 30, 25]]

main(test_matrix)