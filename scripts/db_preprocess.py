import json


if __name__ == "__main__":
    allbud_data = {}
    otreeba_strains_data = []
    otreeba_conditions_data = []
    otreeba_studies_data = []
    leafly_data = {}


    with open('../data/allbud_output.json', encoding="utf8") as f:
        allbud_data = json.load(f)

    with open('../data/strains.json', encoding="utf8") as f:
        otreeba_strains_data = json.load(f)['data']

    with open('../data/conditions.json', encoding="utf8") as f:
        otreeba_conditions_data = json.load(f)['data']

    with open('../data/studies.json', encoding="utf8") as f:
        otreeba_studies_data = json.load(f)['data']

    print(len(allbud_data))
    print(len(otreeba_strains_data))
    print(len(otreeba_conditions_data))
    print(len(otreeba_studies_data))
