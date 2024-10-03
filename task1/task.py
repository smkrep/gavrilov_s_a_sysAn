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

def output_siblings_and_children(graph):
    for curr_key, value in graph.items():
        print("Вершина: " + curr_key)
        print(f"\tБратья: {[key for key in graph if graph[key]["parent"] == graph[curr_key]["parent"] and curr_key != key]}")
        print(f"\tДети: {value["children"]}")


def main(test_string):
    graph_structure = json_to_tree(test_string)
    output_siblings_and_children(graph_structure)



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


