import json


def read_json():
    with open('config.json', 'r') as openfile:
        json_object = json.load(openfile)

    return json_object


def write_json(dictionary):
    with open("sample.json", "w") as outfile:
        json.dump(dictionary, outfile)
