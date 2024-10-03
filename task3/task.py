from math import log2
import json



def make_node(parent, children):
    node = {}
    node["parent"] = parent
    node["children"] = children
    return node


def rec_parse_input(parent, data, graph):
    desc = list(data.keys())
    for key, value in data.items():
        if value:
            graph[f"{key}"] = make_node(parent, rec_parse_input(key, value, graph))
        else:
            graph[f"{key}"] = make_node(parent, [])
    return desc


def json_to_tree(json_string):
    graph = {}
    data = json.loads(json_string)
    rec_parse_input(None, data, graph)
    return graph


def siblings_list(graph, curr_key):
    return [key for key in graph if graph[key]["parent"] == graph[curr_key]["parent"] and curr_key != key]


def calculate_siblings(graph, curr_key):
    if curr_key is None: return 0
    return len(siblings_list(graph, curr_key))


def calculate_parents(key: str, graph_structure):
    k = key
    counter = 0
    while graph_structure[k]["parent"] != None:
        counter+=1
        k = graph_structure[k]["parent"]
    return counter


def calculate_siblings_children(graph_structure, siblings, c):
    for sibling in siblings:
        if len(graph_structure[sibling]["children"]) != 0:
            for elem in graph_structure[sibling]["children"]:
                calculate_siblings_children(graph_structure, graph_structure[sibling]["children"], c)
                c.counter+=1
        else:
            return
    

def calculate_indirect_children(graph_structure, children, c):
    if len(children) == 0:
        return
    
    for child in children:
        calculate_indirect_children(graph_structure, graph_structure[child]["children"], c)
        c.counter+=1


        
class Counter:
    counter = 0   


def calculate_relations(graph_structure):
    ans = [[0 for _ in range(len(graph_structure))] for _ in range(5)]
    for curr_key, value in graph_structure.items():
        ans[0][int(curr_key) - 1] = 1 if value["parent"] is not None else 0 #Непосредственное управление
        ans[1][int(curr_key) - 1] = len(value["children"]) #Непосредственное подчинение
        ans[2][int(curr_key) - 1] = calculate_parents(curr_key, graph_structure) + calculate_siblings(graph_structure, graph_structure[curr_key]["parent"]) - 1 if value["parent"] is not None else 0 # Опосредованное управление
        siblings = siblings_list(graph_structure, curr_key)
        counter = Counter()
        calculate_siblings_children(graph_structure, siblings, counter)
        for child in graph_structure[curr_key]["children"]:
            calculate_indirect_children(graph_structure, graph_structure[child]["children"], counter)
        ans[3][int(curr_key) - 1] = counter.counter #Опосредованное подчинение
        ans[4][int(curr_key) - 1] = len(siblings) #Соподчинение на одном уровне (коллеги)
    # for line in ans:
    #     print(line)
    return ans


def calculate_enthropy(matrix):

    n = len(matrix[0])
    enthropy = 0
    for column in zip(*matrix):
        Hj = 0

        for elem in column:
            if elem != 0:
                p_j = elem / (n-1)
                Hj += p_j * log2(p_j)
        
        Hj = Hj * (-1)
        enthropy += Hj

    return enthropy
            

def main(test_string):
    graph_structure = json_to_tree(test_string)
    matrix = calculate_relations(graph_structure)
    enthropy = calculate_enthropy(matrix)
    print(f"Значение энтропии: {round(enthropy, 2)}")

#test code
test_string = '''{
    "1": {
        "2": {
            "3": {
                "5": {},
                "6": {}
            },
            "4": {
                "7": {},
                "8": {}

            }
        }
    }
}
'''

main(test_string)


