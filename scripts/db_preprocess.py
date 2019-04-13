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
            if "\"" in needed_sentence:
                matches=re.findall(r'\"(.*?)\"',needed_sentence)
            else:
                # print(needed_sentence)
                curr_phrase = re.findall(r'(known as(\s\S+)+[,)])', needed_sentence)
                if len(curr_phrase) == 0:
                    new_leafly_data.append(curr_strain_data)
                    done_lst.append(curr_strain_name)
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


def combine_leafly_data(curr_strainobject, strain_match_lst,):
    pass





    #     if counter % 1000 == 0:
    #         print(str(counter/len(allbud_data) * 100) + "% done")
    #
    # with open('../data/cleaned_allbud.json', 'w') as outfile:
    #     json.dump(new_allbud_data, outfile)



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
            # curr_strain_data = allbud_data[allbud_strain]
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
                    # print(needed_sentence)
                    curr_phrase = re.findall(r'(known as(\s\S+)+[,)])', needed_sentence)
                    if len(curr_phrase) == 0:
                        new_leafly_data.append(curr_strain_data)
                        done_lst.append(curr_strain_name)
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

                info_return = combine_leafly_data(curr_strain_data, final_match_lst)
                done_lst = done_lst + final_match_lst
                new_leafly_data.append(info_return)

    with open('../data/cleaned_leafly.json', 'w') as outfile:
        json.dump(new_leafly_data, outfile)

def combine_otri_leafly():
    leafly_data = {}
    otri_data = {}
    with open('../data/cleaned_leafly.json', encoding="utf8") as f:
        leafly_data = json.load(f)
    with open('../data/strains.json', encoding="utf8") as d:
        otri_data = json.load(d)
    i = 0
    for l_data in leafly_data:
        if l_data != None:
            i +=1
            print(l_data['name'])
    print(i)
        # for o_data in otri_data.keys():







if __name__ == "__main__":
    # remove_dupes_allbud()
    # remove_dupes_leafly()
    # combine_leafly_allbud_dicts()
    combine_otri_leafly()


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
