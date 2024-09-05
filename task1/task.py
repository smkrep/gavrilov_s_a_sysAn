import json

def json_to_tree(json_string):
    data = json.loads(json_string)


test_string = "{ a: {}}"

json_to_tree(test_string)
