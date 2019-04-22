import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import spacy
from constants import additional_stopwords
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.tokenize import RegexpTokenizer
import json


def remove_stopwords(texts, stop_words):
    return [[word for word in doc if word not in stop_words] for doc in texts]

def make_bigrams(texts, bigram_mod):
    return [bigram_mod[doc] for doc in texts]


def lemmatization(texts, nlp,allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


def lda_try():
    stop_words = ENGLISH_STOP_WORDS.union(additional_stopwords)
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

    final_tokenized = []
    for document in documents:
        tokenizer = RegexpTokenizer(r'\w+')
        final_tokenized.append(tokenizer.tokenize(document))

    final_tokenized = list(final_tokenized)

    bigram_modification = gensim.models.Phrases(final_tokenized, min_count = 5, threshold = 100)

    data_nostops_words = remove_stopwords(final_tokenized, stop_words)

    data_bigrams = make_bigrams(data_nostops_words, bigram_modification)

    nlp = spacy.load('en', disable=['parser', 'ner'])

    data_lemmatized = lemmatization(data_bigrams, nlp, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

    id2word = corpora.Dictionary(data_lemmatized)

    corpus = [id2word.doc2bow(text) for text in data_lemmatized]

    # lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
    #                                        id2word=id2word,
    #                                        num_topics=20,
    #                                        random_state=100,
    #                                        update_every=1,
    #                                        chunksize=100,
    #                                        passes=10,
    #                                        alpha='auto',
    #                                        per_word_topics=True)
    # pprint(lda_model.print_topics())
    mallet_path = '../data/mallet-2.0.8/bin/mallet'

    ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=20, id2word=id2word)

    # model_topics = ldamallet.show_topics(formatted=False)
    # print(ldamallet.print_topics(num_words=10))

    final_lst = ldamallet.show_topics(num_topics = 20, formatted=False)
    # print((final_lst))
    final_dict = {}
    for topic in final_lst:
        final_dict[str(topic[0])] = {}
        for word in topic[1]:
            (final_dict[str(topic[0])])[word[0]] = word[1]



    with open('../data/lda.json', 'w') as f:
        json.dump(final_dict, f)















if __name__ == "__main__":
    lda_try()
