from sklearn.feature_extraction.text import TfidfVectorizer
import json
from scipy.sparse.linalg import svds
import matplotlib
from constants import additional_stopwords
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import numpy as np


def find_dims():
    input_data = {}
    with open('../data/combined_cleaned_data.json') as f:
        input_data = json.load(f)

    # combine description and reviews
    documents = []
    for input in input_data:
        text = input['description']
        reviews = input['reviews']
        for review in reviews:
            text += review
        documents.append(text)

    #turn text into matrix
    stop_words = ENGLISH_STOP_WORDS.union(additional_stopwords)
    vectorizer = TfidfVectorizer(stop_words = stop_words, max_df = .90, min_df = 200)
    my_matrix = vectorizer.fit_transform(documents)#.transpose()



    #this is our machine learning component
    words_compressed, s, docs_compressed = svds(my_matrix,k=40)
    docs_compressed = docs_compressed.transpose()
    word_to_index = vectorizer.vocabulary_

    keys_vector = []
    # index_to_word = {i:t for t,i in word_to_index.items()}
    with open('../data/extra_svd_dims.json', 'w') as f:
        json.dump(list(word_to_index.keys()), f)
    with open('../data/keys_vector.json') as f:
        keys_vector = json.load(f)

    # rev_des_matrix = words_compressed.toarray()
    rev_des_matrix = np.ceil(words_compressed)

    cond_vectors = []
    for input in input_data:
        cond_vector = strain_to_vector(input, keys_vector)
        cond_vectors.append(cond_vector)
    condition_matrix = np.array([np.array(xi) for xi in cond_vectors])
    final_matrix = np.concatenate((rev_des_matrix, condition_matrix), axis=1)

    # add vector to every strain
    i = 0
    for data in input_data:
        data['vector'] = list(final_matrix[i,:])
        i += 1

    with open('../data/combined_cleaned_data.json', 'w') as f:
        json.dump(input_data, f)


def strain_to_vector(input, keys_vector):
    vector_list = input['positive'] + input['negative_effects'] + \
        input['medical'] + input['aroma'] + input['flavor_descriptors']
    cond_vector = []
    for key in keys_vector:
        if key in vector_list:
            cond_vector.append(1)
        else:
            cond_vector.append(0)
    return cond_vector

def gather_keys():
    '''
        find all keys so we can use them to generate a vector of binaries
    '''
    input_data = {}
    with open('../data/combined_cleaned_data.json') as f:
        input_data = json.load(f)

    # combine description and reviews
    positive = set()
    negative = set()
    medical = set()
    aroma = set()
    flavor = set()
    #'positive', 'medical', 'aroma', 'flavor_descriptors',  'negative_effects'

    for input in input_data:
        for pos in input['positive']:
            positive.add(pos)
        for neg in input['negative_effects']:
            negative.add(neg)
        for med in input['medical']:
            medical.add(med)
        for aro in input['aroma']:
            aroma.add(aro)
        for flav in input['flavor_descriptors']:
            flavor.add(flav)

    union_set = list(positive.union(negative).union(medical).union(aroma).union(flavor))
    with open('../data/keys_vector.json', 'w') as f:
        json.dump(union_set, f)



if __name__ == "__main__":
    # gather_keys()
    find_dims()
