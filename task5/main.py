# поисковый запрос - тоже вектор
# размерность вектора - все уникальные леммы
# элементы вектора - tf-idf слова
# формула для ранжирования: http://akorsa.ru/2017/01/vektornaya-model-i-kosinusnoe-shodstvo-cosine-similarity/
import json
import math
from functools import reduce
from os import walk

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from math import sqrt

from scipy.spatial import distance

from taks3.boolean_search import boolean_search


big = 999999999

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def read_html_lemma_tf_idf(html_name) -> dict[str, (float, float)]:
    lemmas_tf_idf_folder = "../lemmas_tf-idf/"
    lemma_tf_idf_prefix = "lemma_tf-idf_"
    lemma_info_for_html = dict()

    with open(lemmas_tf_idf_folder + lemma_tf_idf_prefix + html_name, 'r', encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        if line == "":
            continue

        line_items = line.split(" ")

        lemma = line_items[0]
        lemma_idf = float(line_items[1])
        lemma_tf_idf = float(line_items[2])

        lemma_info_for_html.setdefault(lemma, (lemma_idf, lemma_tf_idf))

    return lemma_info_for_html

iii = 0

def calc_similarity(a, b):
    # cosine = distance.cosine(a[1], b)
    # return cosine
    a = a[1]
    if len(a) != len(b):
        raise Exception("разная длина векторов")

    vector_size = len(a)

    numerator = sum([a[i] * b[i] for i in range(vector_size)])

    a_len = sqrt(sum([a[i] ** 2 for i in range(vector_size)]))
    b_len = sqrt(sum([b[i] ** 2 for i in range(vector_size)]))

    denominator = a_len * b_len

    return numerator / denominator



def vector_search(query):
    lemmatizer = WordNetLemmatizer()
    tokenizer = nltk.tokenize.TreebankWordTokenizer()

    tokens = tokenizer.tokenize(query)
    english_stopwords = stopwords.words('english')

    lemmas_in_query = [lemmatizer.lemmatize(token, get_wordnet_pos(pos)) for token, pos in nltk.pos_tag(tokens)]
    lemmas_in_query = list(filter(lambda l: l not in english_stopwords, lemmas_in_query))

    unique_lemmas = set(lemmas_in_query)

    # sort | array | java
    query_for_boolean_search = " | ".join(lemmas_in_query)

    found_html_list = boolean_search(query_for_boolean_search)

    print(found_html_list)

    # все встретившиеся леммы из html и их idf
    lemmas_idf: dict[str, float] = dict()

    # список пар: название документа, и он в виде вектора
    selection: list[(str, list[float])] = []

    for found_html in found_html_list:
        html_lemma_info = read_html_lemma_tf_idf(found_html)

        for lemma in html_lemma_info:
            unique_lemmas.add(lemma)

    unique_lemmas = list(unique_lemmas)

    for found_html in found_html_list:
        html_lemma_info = read_html_lemma_tf_idf(found_html)
        vector = []

        # здесь кароче надо не юник а иммено все
        for lemma in unique_lemmas:
            if lemma in html_lemma_info:
                lemma_idf, lemma_tf_idf = html_lemma_info.get(lemma)
                lemmas_idf.setdefault(lemma, lemma_idf)
                vector.append(lemma_tf_idf)
            else:
                # слово в запросе есть но в текущем документе нет
                vector.append(0.0)

        selection.append((found_html, vector))

    # вектор из запроса
    query_vector = []

    print('')
    print('')

    for lemma in unique_lemmas:

        if lemma in lemmas_in_query:

            lemma_count = sum([1 if current_lemma == lemma else 0 for current_lemma in lemmas_in_query])

            lemma_tf = lemma_count / len(lemmas_in_query)
            lemma_tf_idf = lemma_tf * lemmas_idf[lemma]



            print(lemma_count, lemma_tf, lemma_tf_idf, lemma)

            # for lemma in lemmas_in_query:
            #     index = unique_lemmas.index(lemma)
            #     print(sum([tokens_info[token] for token in tokens]), query_vector[index], lemma)



            query_vector.append(lemma_tf_idf)
        else:
            query_vector.append(0.0)
            # print("в запросе есть слово которое не встретилось ни в одном html")
            # return []
    print('')
    print('')
    # наконец сортируем
    # sel2 = []
    # for s in selection:
    #     sel2.append(s, calc_similarity(s, query_vector))

    selection = sorted(selection, key=lambda d: calc_similarity(d, query_vector), reverse=True)

    # for html, v in selection:
    #     print(v)

    selection_ = [(s[0], calc_similarity(s, query_vector), s[1]) for s in selection]


    # достаю инфо
    html_files_folder = '../archive/'
    lemmas_file_prefix = '../lemmas/'
    htmls: list[(str, int, dict[str, int]), dict[str, list[str]]] = []

    with open("../htmls_data.json", 'r', encoding="utf-8") as file:
        htmls = json.loads(file.read())


    with open("../task1/index.txt", 'r', encoding="utf-8") as file:
        meta = json.loads(file.read())

    for item, cd, v in selection_:
        print(item, cd, meta["../archive/" + item])
        for html_name, word_count, tokens_info, lemmas in htmls:
            if item == html_name:
                for lemma in lemmas_in_query:
                    if lemma in lemmas:
                        index = unique_lemmas.index(lemma)

                        tokens = lemmas[lemma]
                        print(sum([tokens_info[token] for token in tokens]), v[index] / lemmas_idf[lemma], v[index], lemma)

        print('')


    return selection_




if __name__ == '__main__':

    result = vector_search("variable")
