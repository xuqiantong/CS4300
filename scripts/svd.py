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
    my_matrix = vectorizer.fit_transform(documents).transpose()

    #this is our machine learning component
    words_compressed, s, docs_compressed = svds(my_matrix,k=40)
    docs_compressed = docs_compressed.transpose()

    word_to_index = vectorizer.vocabulary_
    # index_to_word = {i:t for t,i in word_to_index.items()}

    my_matrix = my_matrix.toarray()

    i = 0
    for data in input_data:
        data['tfidf'] = list(my_matrix[:,i])
        i += 1

    with open('../data/extra_svd_dims.json', 'w') as f:
        json.dump(list(word_to_index.keys()), f)


    with open('../data/combined_cleaned_data.json', 'w') as f:
        json.dump(input_data, f)


if __name__ == "__main__":
    find_dims()
