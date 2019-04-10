import json


if __name__ == "__main__":
    with open('../data/allbud_output.json') as f:
        data = json.load(f)
        print(len(data))
