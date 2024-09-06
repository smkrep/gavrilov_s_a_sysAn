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

graph_structure = json_to_tree(test_string)

print(graph_structure)