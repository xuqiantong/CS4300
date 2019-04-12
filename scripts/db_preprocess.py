import json
from nltk.tokenize import sent_tokenize
import re

def editDistDP(str1, str2, m, n):
    # Create a table to store results of subproblems
    dp = [[0 for x in range(n+1)] for x in range(m+1)]

    # Fill d[][] in bottom up manner
    for i in range(m+1):
        for j in range(n+1):

            # If first string is empty, only option is to
            # insert all characters of second string
            if i == 0:
                dp[i][j] = j    # Min. operations = j

            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i    # Min. operations = i

            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]

            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = min( 1 + dp[i][j-1],        # Insert
                                 1 +  dp[i-1][j],        # Remove
                                  2 + dp[i-1][j-1])    # Replace

    return dp[m][n]

def combine_data(curr_strain, strain_match_lst, info_dict):
    curr_strainobject = info_dict[curr_strain]
    strain_match_objectlst = []
    for strain_match in strain_match_lst:
        strain_match_objectlst.append(info_dict[strain_match])
    strain_match_objectlst.append(curr_strainobject)
    new_obj = {}
    for m in strain_match_objectlst:
        if "name" in new_obj.keys():
            new_obj["name"] += ", " + m["name"]
        else:
            new_obj["name"] = m["name"]
        if "description" in new_obj.keys():
            new_obj["description"] += "/n" + m["description"]
        else:
            new_obj["description"] = m["description"]
        if "rating" in new_obj.keys():
            new_obj["rating"] += m["rating"]
        else:
            new_obj["rating"] = m["rating"]
        if "positive" in new_obj.keys():
            curr_pos = new_obj["positive"]
            new_pos = m["positive"]
            new_obj["positive"] = set(curr_pos + new_post)
        else:
            new_obj["positive"] = m["positive"]
        if "flavor" in new_obj.keys():
            curr_flavor = new_obj["flavor"]
            new_flavor = m["flavor"]
            new_obj["flavor"] = set(curr_flavor + new_flavor)
        else:
            new_obj["flavor"] = m["flavor"]
        if "aroma" in new_obj.keys():
            curr_aroma = new_obj["aroma"]
            new_aroma = m["aroma"]
            new_obj["aroma"] = set(curr_aroma + new_aroma)
        else:
            new_obj["aroma"] = m["aroma"]
        if "medical" in new_obj.keys():
            curr_medical = new_obj["medical"]
            new_medical = m["medical"]
            new_obj["medical"] = set(curr_medical + new_medical)
        else:
            new_obj["medical"] = m["medical"]
        if "percentages" in new_obj.keys():
            curr_percentages = new_obj["percentages"]
            new_percentages = m["percentages"]
            new_obj["percentages"] = {**new_percentages, **curr_percentages}
        else:
            new_obj["percentages"] = m["percentages"]
    new_obj["rating"] = new_obj["rating"] / len(strain_match_objectlst)
    return new_obj["name"], new_obj









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

    

    new_allbud_dict = {}
    done_lst = []
    for allbud_strain in allbud_data.keys():
        if allbud_strain in done_lst:
            continue
        else:
            curr_strain_data = allbud_data[allbud_strain]
            curr_description = curr_strain_data['description']
            tokenize_lst = sent_tokenize(curr_description)
            needed_sentence = ""
            for sentence in tokenize_lst:
                if "known as" in sentence:
                    needed_sentence = sentence
                    break
            if needed_sentence == "":
                new_allbud_dict[allbud_strain] = allbud_data[allbud_strain]
            else:
                # matches=re.findall(r'“(.*?)”',needed_sentence)
                matches=re.findall(r'\"(.*?)\"',needed_sentence)
                final_match_lst = []
                for match in matches:
                    new_match = match
                    if "," in match:
                        new_match = match.replace(",", "")
                        final_match_lst.append(new_match)
                info_return = combine_data(allbud_strain, final_match_lst, allbud_data)
                new_allbud_dict[info_return[0]] = info_return[1]







        # curr_lst = []
        # for allbud_strain1 in allbud_data.keys():
        #     curr_score = editDistDP(allbud_strain, allbud_strain1, \
        #         len(allbud_strain), len(allbud_strain1) )
        #     if curr_score <= 2:
        #         curr_tup = (curr_otreeba_strain, curr_score)
        #         curr_lst.append(curr_tup)
        #     curr_tup = (allbud_strain1, curr_score)
        #     curr_lst.append(curr_tup)
        # curr_lst.sort(key=lambda tup: tup[1])




    # total_lst = []
    # for allbud_strain in allbud_data.keys():
    #     curr_lst = []
    #     for otreeba_strain in otreeba_strains_data:
    #         curr_otreeba_strain = otreeba_strain['name']
    #         curr_score = editDistDP(allbud_strain.lower(), curr_otreeba_strain.lower(), \
    #             len(allbud_strain), len(curr_otreeba_strain) )
    #         if curr_score <= 3:
    #             curr_tup = (curr_otreeba_strain, curr_score)
    #             curr_lst.append(curr_tup)
    #     # curr_lst.sort(key=lambda tup: tup[1])
    #     if curr_lst != []:
    #         total_lst.append(allbud_strain)
    #         print(allbud_strain)
    # print(len(total_lst))
