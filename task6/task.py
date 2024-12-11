import json


def calculate_mu(x, points):
    for i in range(len(points) - 1):
        x0, mu0 = points[i]
        x1, mu1 = points[i + 1]
        if x0 <= x <= x1:
            return mu0 if mu0 == mu1 else mu0 + (mu1 - mu0) * (x - x0) / (x1 - x0)      
    return 0


def map_to_regulator(temperature_mu_vals, transition_map):

    regulator_mu_vals = {}

    for temp_term, temp_mu in temperature_mu_vals.items():
        reg_term = transition_map[temp_term]
        if reg_term in regulator_mu_vals:
            regulator_mu_vals[reg_term] = max(regulator_mu_vals[reg_term], temp_mu)
        else:
            regulator_mu_vals[reg_term] = temp_mu
    
    print(f"Результат проекции на нечеткое множество положений регулятора: {regulator_mu_vals}\n")
    return regulator_mu_vals


def fuzz(input_value, fuzzy_set):

    mu_vals = {}

    for term, points in fuzzy_set.items():
        mu_vals[term] = round(calculate_mu(input_value, points), 2)

    print(f"Результат фаззификации температуры {input_value}: {mu_vals}\n")
    return mu_vals


def defuzz_meanmax(regulator_mu_vals, fuzzy_set):

    max_mu = max(regulator_mu_vals.values()) 
    x_values = []  

    for term, mu in regulator_mu_vals.items():
        if mu == max_mu:
            points = fuzzy_set[term]
            for i in range(len(points) - 1):
                x0, mu0 = points[i]
                x1, mu1 = points[i + 1]
                
                if mu0 <= max_mu <= mu1 or mu1 <= max_mu <= mu0:
                    x_values.append(x0) if mu0 == mu1 else x_values.append(x0 + (x1 - x0) * (max_mu - mu0) / (mu1 - mu0))
                        
    return sum(x_values) / len(x_values) if x_values else 0


def main(temperatures_json: str, regulator_json: str, transition_json: str, temperature_input: float):

    temperatures_set = json.loads(temperatures_json)
    regulator_set = json.loads(regulator_json)
    transition_map = json.loads(transition_json)


    temperature_mu_vals = fuzz(temperature_input, temperatures_set)
    regulator_mu_vals = map_to_regulator(temperature_mu_vals, transition_map)

    mean_max = defuzz_meanmax(regulator_mu_vals, regulator_set)

    print(f"Дефаззифицированное положение регулятора методом среднего максимума: {mean_max}\n")

temperatures = """{
    "холодно": [
        [0, 1],
        [16, 1],
        [20, 0],
        [50, 0]
    ],
    "комфортно": [
        [16, 0],
        [20, 1],
        [22, 1],
        [26, 0]
    ],
    "жарко": [
        [0, 0],
        [22, 0],
        [26, 1],
        [50, 1]
    ]
}"""

regulator = """{
    "слабо": [
        [0, 1],
        [6, 1],
        [10, 0],
        [20, 0]
    ],
    "умеренно": [
        [6, 0],
        [10, 1],
        [12, 1],
        [16, 0]
    ],
    "интенсивно": [
        [0, 0],
        [12, 0],
        [16, 1],
        [20, 1]
    ]
}"""

transition = """{
    "холодно": "интенсивно",
    "комфортно": "умеренно",
    "жарко": "слабо"
}"""

main(temperatures, regulator, transition, 25)