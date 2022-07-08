import json


def read_json():
    with open('config.json', 'r') as openfile:
        json_object = json.load(openfile)

    return json_object


def write_json(data):
    with open("config.json", "w") as outfile:
        json.dump(data, outfile, indent=4)


def set_limit(limit):
    data = read_json()
    data['limit'] = limit
    write_json(data)



