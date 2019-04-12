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
    i = 0
    for allbud_strain in allbud_data.keys():
        curr_strain_data = allbud_data[allbud_strain]
        curr_description = curr_strain_data['description']
        tokenize_lst = sent_tokenize(curr_description)
        needed_sentence = ""
        for sentence in tokenize_lst:
            if "known as" in sentence:
                i += 1
                needed_sentence = sentence
                break
        if needed_sentence == "":
            new_allbud_dict[allbud_strain] = allbud_data[allbud_strain]
        else:
            print(needed_sentence)
            matches=re.findall(,needed_sentence)
            print(matches)




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
