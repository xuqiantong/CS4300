import json
from nltk.tokenize import sent_tokenize
import re
from constants import *

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


def find_strain_obj_in_lst(name, lst):
    '''
        return object with key "name" == input name
        otherwise return None
    '''
    answer = {}
    for obj in lst:
        if obj["name"] == name:
            return obj
    return None

def combine_allbud_data(curr_strainobject, strain_match_lst, info_dict):
    strain_match_objectlst = []
    # find new strain object and add to lst
    for strain_match in strain_match_lst:
        new_strain = find_strain_obj_in_lst(strain_match, info_dict)
        if new_strain is None:
            continue
        else:
            strain_match_objectlst.append(new_strain)

    strain_match_objectlst.append(curr_strainobject)
    new_obj = {}

    for m in strain_match_objectlst:
        if "name" in new_obj.keys():
            new_obj["name"] += [m["name"]]
        else:
            new_obj["name"] = [m["name"]]

        if "description" in new_obj.keys():
            new_obj["description"] += "/n" + m["description"]
        else:
            new_obj["description"] = m["description"]
        if "rating" in new_obj.keys():
            new_obj["rating"] += float(m["rating"])
        else:
            new_obj["rating"] = float(m["rating"])
        if "positive" in new_obj.keys():
            curr_pos = new_obj["positive"]
            new_pos = m["positive"]
            new_obj["positive"] = list(set(curr_pos + new_pos))
        else:
            new_obj["positive"] = m["positive"]
        if "flavor" in new_obj.keys():
            curr_flavor = new_obj["flavor"]
            new_flavor = m["flavor"]
            new_obj["flavor"] = list(set(curr_flavor + new_flavor))
        else:
            new_obj["flavor"] = m["flavor"]
        if "aroma" in new_obj.keys():
            curr_aroma = new_obj["aroma"]
            new_aroma = m["aroma"]
            new_obj["aroma"] = list(set(curr_aroma + new_aroma))
        else:
            new_obj["aroma"] = m["aroma"]
        if "medical" in new_obj.keys():
            curr_medical = new_obj["medical"]
            new_medical = m["medical"]
            new_obj["medical"] = list(set(curr_medical + new_medical))
        else:
            new_obj["medical"] = m["medical"]
        if "percentages" in new_obj.keys():
            curr_percentages = new_obj["percentages"]
            new_percentages = m["percentages"]
            new_obj["percentages"] = {**new_percentages, **curr_percentages}
        else:
            new_obj["percentages"] = m["percentages"]
    new_obj["rating"] = new_obj["rating"] / len(strain_match_objectlst)
    return new_obj


def remove_dupes_allbud():
    allbud_data = {}
    with open('../data/allbud_output.json', encoding="utf8") as f:
        allbud_data = json.load(f)

    new_allbud_data = []
    done_lst = [] #holds names of strains that we want to skip since they are duplicates
    counter = 0

    for curr_strain_data in allbud_data:
        counter += 1
        if curr_strain_data['name'] in done_lst:
            continue
        else:
            # curr_strain_data = allbud_data[allbud_strain]
            curr_description = curr_strain_data['description']
            tokenize_lst = sent_tokenize(curr_description)
            needed_sentence = ""
            for sentence in tokenize_lst:
                if "known as" in sentence:
                    needed_sentence = sentence
                    break
            if needed_sentence == "":
                new_allbud_data.append(curr_strain_data)
                done_lst.append(curr_strain_data['name'])
            else:
                final_match_lst = []
                matches = []
                if "\"" in needed_sentence:
                    matches=re.findall(r'\"(.*?)\"',needed_sentence)
                else:
                    # print(needed_sentence)
                    curr_phrase = re.findall(r'(known as(\s\S+)+[,)])', needed_sentence)
                    if len(curr_phrase) == 0:
                        new_allbud_data.append(curr_strain_data)
                        done_lst.append(curr_strain_data['name'])
                    else:
                        # print(curr_phrase[0][0])
                        matches1 = re.findall(r'([A-Z]\w+\s)*([A-Z]\w+)+', curr_phrase[0][0])
                        for match in matches1:
                            curr_name = match[0] + match[1]
                            matches.append(curr_name)

                for match in matches:
                    new_match = match
                    if "," in match:
                        new_match = match.replace(",", "")
                        final_match_lst.append(new_match)

                info_return = combine_allbud_data(curr_strain_data, final_match_lst, allbud_data)
                done_lst = done_lst + final_match_lst
                new_allbud_data.append(info_return)

        if counter % 1000 == 0:
            print(str(counter/len(allbud_data) * 100) + "% done")

    with open('../data/cleaned_allbud.json', 'w') as outfile:
        json.dump(new_allbud_data, outfile)


def combine_leafly_allbud_strain(leafly_strain, allbud_strain):
    '''
        combine a specific instance of an allbud strain and a leafly strain
    '''
    # print('leafly')
    # print(leafly_strain.keys())
    # print('allbud')
    # print(allbud_strain.keys())
    pass


def clean_name_string(name):
    return name.lower().replace(" ", "")


def combine_leafly_allbud_dicts():
    '''
        combine allbud dictionary and leafly dictionary
    '''
    with open('../data/leafly_output.json', encoding="utf8") as f:
        leafly_strains_data = json.load(f)
    with open('../data/cleaned_allbud.json', encoding="utf8") as f:
        allbud_strains_data = json.load(f)

    # it has an empty strain
    del leafly_strains_data['']

    full_data = []
    counter = 0
    counter2 = 0
    for strain1_name in leafly_strains_data.keys():
        strain1 = leafly_strains_data[strain1_name]
        strain1_name = clean_name_string(strain1_name)
        # print(strain1_name)
        counter2 += 1
        if counter2 % 20 == 0:
            print(counter, counter2)
        for strain2 in allbud_strains_data:
            strain2_names = strain2["name"]

            #if within a certain edit distance, we combine, otherwise we throw out
            for strain2_name in strain2_names:
                strain2_name = clean_name_string(strain2_name)
                if editDistDP(strain1_name, strain2_name, len(strain1_name), len(strain2_name)) <= EDIT_DIST_THRESHOLD:
                    print(strain1_name, strain2_name)
                    counter += 1
                    combined_data = combine_leafly_allbud_strain(strain1, strain2)
                    full_data.append(combined_data)
                    break
            else:
                # if we didn't find a match
                continue
            break




    with open('../data/leafly_allbud.json', 'w') as outfile:
        json.dump(full_data, outfile)


def combine_leafly_data(curr_strainobject, strain_match_lst, info_dict):

    new_obj = curr_strainobject
    counter = 0
    if new_obj["rating"] != "No Reviews" and new_obj["rating"] != "":
        new_obj["rating"] = float(new_obj["rating"])
        counter += 1
    else:
        new_obj["rating"] = 0.0

    new_obj["name"] = [new_obj["name"]]

    obj_match_lst = []
    for k in strain_match_lst:
        if k in info_dict.keys():
            obj_match_lst.append(info_dict[k])
        else:
            new_obj["name"] += [k]



    for m in obj_match_lst:
        if "name" not in m.keys():
            continue
        else:
            new_obj["description"] += "/n" + m["description"]
            curr_pos = new_obj["negative_effects"]
            new_pos = m["negative_effects"]
            new_obj["negative_effects"] = list(set(curr_pos + new_pos))

            curr_loc = new_obj["popular_locations"]
            new_loc = m["popular_locations"]
            new_obj["popular_locations"] = list(set(curr_loc + new_loc))

            curr_gen = new_obj["general_effects"]
            new_gen = m["general_effects"]
            new_obj["general_effects"] = list(set(curr_gen + new_gen))

            curr_med = new_obj["medical_symptoms_it_treats"]
            new_med = m["medical_symptoms_it_treats"]
            new_obj["medical_symptoms_it_treats"] = list(set(curr_med + new_med))

            curr_flavor = new_obj["flavor_descriptors"]
            new_flavor = m["flavor_descriptors"]
            new_obj["flavor_descriptors"] = list(set(curr_flavor + new_flavor))

            new_obj["reviews"] += m["reviews"]

            if new_obj["rating"] != "No Reviews":
                new_obj["rating"] += float(m["rating"])
                counter += 1


    if counter > 0:
        new_obj["rating"] = new_obj["rating"] / counter
    else:
        new_obj["rating"] = "No Reviews"


    return new_obj


def remove_dupes_leafly():
    leafly_data = {}
    with open('../data/leafly_output.json', encoding="utf8") as f:
        leafly_data = json.load(f)

    del leafly_data['']

    new_leafly_data = []
    done_lst = [] #holds names of strains that we want to skip since they are duplicates
    counter = 0
    for curr_strain_name in leafly_data.keys():
        counter += 1
        curr_strain_data = leafly_data[curr_strain_name]
        curr_strain_data['name'] = curr_strain_name
        if curr_strain_name in done_lst:
            continue
        else:
            curr_description = curr_strain_data['description']
            tokenize_lst = sent_tokenize(curr_description)
            needed_sentence = ""
            for sentence in tokenize_lst:
                if "known as" in sentence:
                    needed_sentence = sentence.replace('\u201c','\"'). \
                        replace('\u201d','\"').replace('\u2019','\''). \
                        replace('\u2013','-')
                    break
            if needed_sentence == "":
                new_leafly_data.append(curr_strain_data)
                done_lst.append(curr_strain_name)
            else:
                final_match_lst = []
                matches = []
                if "\"" in needed_sentence:
                    matches=re.findall(r'\"(.*?)\"',needed_sentence)
                else:
                    curr_phrase = re.findall(r'(known as(\s\S+)+[,)])', needed_sentence)
                    if len(curr_phrase) == 0:
                        new_leafly_data.append(curr_strain_data)
                        done_lst.append(curr_strain_name)
                    else:
                        matches1 = re.findall(r'([A-Z]\w+\s)*([A-Z]\w+)+', curr_phrase[0][0])
                        for match in matches1:
                            curr_name = match[0] + match[1]
                            matches.append(curr_name)
                for match in matches:
                    new_match = match
                    if "," in match:
                        new_match = match.replace(',' , "")
                        final_match_lst.append(new_match)
                    else:
                        final_match_lst.append(new_match)


                info_return = combine_leafly_data(curr_strain_data, final_match_lst, leafly_data)
                done_lst = done_lst + final_match_lst
                new_leafly_data.append(info_return)

    for new_data in new_leafly_data:
        new_data['description'] = (new_data["description"]).replace('\u201c','\"'). \
            replace('\u201d','\"').replace('\u2019','\''). \
            replace('\u2013','-')
        reviews= new_data["reviews"]
        new_reviews = []
        for review in reviews:
            curr_reviews = review.replace('\u201c','\"'). \
                replace('\u201d','\"').replace('\u2019','\''). \
                replace('\u2013','-')
            new_reviews.append(curr_reviews)
        new_data["reviews"] = new_reviews


    with open('../data/cleaned_leafly.json', 'w') as outfile:
        json.dump(new_leafly_data, outfile)


def combine_otri_leaf_data(o_data, l_data):
    new_obj = {**l_data, **o_data}
    l_name = l_data["name"]
    final_alt_names = []
    if type(l_name) != list:
        l_name = [l_name]
    for alt_name in l_name:
        if alt_name != o_data["name"]:
            if type(alt_name) != list:
                final_alt_names.append(alt_name)
            else:
                final_alt_names + l_name
    new_obj["alternative_names"] = final_alt_names
    return new_obj

def combine_allbud_ol_data(allbud_data, ol_data):
    new_obj = {** allbud_data, ** ol_data}
    new_obj["description"] = allbud_data["description"] + "\n" + ol_data["description"]
    if allbud_data["rating"] == "No Reviews" or ol_data["rating"] == "No Reviews" or allbud_data["rating"] == "" or ol_data["rating"] == "":
        if allbud_data["rating"] != "No Reviews" or allbud_data["rating"] !="":
            new_obj["rating"] = allbud_data["rating"]
        else:
            new_obj["rating"] = ol_data["rating"]
    else:
        new_obj["rating"] = (float(allbud_data["rating"]) + float(ol_data["rating"])) / 2
    new_obj["flavor_descriptors"] = list(set(new_obj['flavor'] + new_obj["flavor_descriptors"]))
    new_obj.pop('flavor', None)
    new_obj["medical"] = list(set(new_obj['medical_symptoms_it_treats'] + new_obj['medical']))
    new_obj.pop('medical_symptoms_it_treats', None)
    return new_obj




def combine_all_data():
    leafly_data = {}
    otri_data = {}
    all_bud_data = {}
    with open('../data/cleaned_leafly.json', encoding="utf8") as f:
        leafly_data = json.load(f)
    with open('../data/cleaned_allbud.json', encoding="utf8") as d:
        all_bud_data = json.load(d)
    with open('../data/strains.json', encoding="utf8") as k:
        otri_data = json.load(k)

    o_l_lst = []
    for o_data in otri_data["data"]:
        curr_obj = o_data
        o_name = o_data["name"]
        for l_data in leafly_data:
            l_name = l_data["name"]
            if type(l_name) == list:
                if o_name in l_name:
                    combined_obj = combine_otri_leaf_data(o_data, l_data)
                    o_l_lst.append(combined_obj)
            else:
                if o_name == l_name:
                    combined_obj = combine_otri_leaf_data(o_data, l_data)
                    o_l_lst.append(combined_obj)


    final_lst = []
    for o_l_data in o_l_lst:
        curr_obj = o_l_data
        o_l_name_lst = (curr_obj["alternative_names"])
        o_l_name_lst.append(curr_obj["name"])
        for all_bud_point in all_bud_data:
            all_bud_names = all_bud_point['name']
            if type(all_bud_names) != list:
                all_bud_names = [all_bud_names]
            temp = set(all_bud_names)
            final_name_cross = [value for value in o_l_name_lst if value in temp]
            if len(final_name_cross) > 0:
                combined_dict = combine_allbud_ol_data(all_bud_point, o_l_data)
                final_lst.append(combined_dict)


    with open('../data/combined_cleaned_data.json', 'w') as outfile:
        json.dump(final_lst, outfile)











if __name__ == "__main__":
    # remove_dupes_allbud()
    # remove_dupes_leafly()
    # combine_leafly_allbud_dicts()
    combine_all_data()

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
