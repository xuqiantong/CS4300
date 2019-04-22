import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import spacy
from constants import additional_stopwords
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.tokenize import RegexpTokenizer
import json
import pandas as pd

def format_topics_sentences(ldamodel, corpus, texts):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)

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

    mallet_path = '../data/mallet-2.0.8/bin/mallet'

    ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=20, id2word=id2word)

    # model_topics = ldamallet.show_topics(formatted=False)
    # print(ldamallet.print_topics(num_words=10))

    df_topic_sents_keywords = format_topics_sentences(ldamodel=ldamallet, corpus=corpus, texts=final_tokenized)
    final_lda_list = df_topic_sents_keywords['Dominant_Topic'].tolist()
    print(final_lda_list)
    with open('../data/final_lda.json', 'w') as f:
        json.dump(final_lda_list,f)


    # final_lst = ldamallet.show_topics(num_topics = 20, formatted=False)
    # # print((final_lst))
    # final_dict = {}
    # for topic in final_lst:
    #     final_dict[str(topic[0])] = {}
    #     for word in topic[1]:
    #         (final_dict[str(topic[0])])[word[0]] = word[1]
    #
    #
    #
    #
    # with open('../data/lda.json', 'w') as f:
    #     json.dump(final_dict, f)















if __name__ == "__main__":
    lda_try()
