import json
from math import sqrt

from task2.main import tokenize, lemmatize, load_meta
from task3.inverting_index import load_lemmas
from task4.main import load_tokens
from task3.boolean_search import boolean_search, load_term_index

#            | lemma1 | lemma2 | lemma3 |   ...  |
# ----------------------------------------------------
# document 1 | tf-idf |  ...   |        |        |
# ----------------------------------------------------
# document 2 | ...    |  ...   |   0    |        |
# ----------------------------------------------------
# document 3 |        |        |        |        |
# ----------------------------------------------------
# document 4 |        |        |        |        |
# ----------------------------------------------------
#     ...    |        |        |        |        |
# ----------------------------------------------------
#   запрос   |        |        |        |        |
# ----------------------------------------------------


def load_lemmas_info(content_file):
    content_filename = content_file.replace("../archive/", "")

    # вычисляю путь до файла с леммами для текущей страницы
    lemma_filename = "../lemmas_info/lemma_info_" + content_filename

    with open(lemma_filename, 'r', encoding="utf-8") as file:
        return json.loads(file.read())


def load_lemmas_idf():
    with open("../task4/lemmas_idf.json", 'r', encoding="utf-8") as file:
        return json.loads(file.read())

def similarity(a, b):
    if len(a) != len(b):
        raise Exception("len is different")

    vector_size = len(a)

    numerator = sum([a[i] * b[i] for i in range(vector_size)])

    a_len = sqrt(sum([a[i] ** 2 for i in range(vector_size)]))
    b_len = sqrt(sum([b[i] ** 2 for i in range(vector_size)]))

    denominator = a_len * b_len

    return numerator / denominator


def vector_search(query):
    query_tokens = tokenize(query)
    query_lemmas = lemmatize(query_tokens)
    documents_lemmas = load_term_index()

    all_lemmas = set()

    for lemma in query_lemmas:
        all_lemmas.add(lemma)

    for lemma in documents_lemmas:
        all_lemmas.add(lemma)

    # "взлом | страница"
    query_for_boolean_search = " | ".join(query_lemmas)

    found_content_files = boolean_search(query_for_boolean_search)

    lemmas_idf = load_lemmas_idf()

    # вектор запроса
    query_vector = []

    for lemma in all_lemmas:
        if lemma in query_lemmas:
            lemma_count = sum([1 if l == lemma else 0 for l in query_lemmas])

            lemma_tf = lemma_count / len(query_lemmas)
            lemma_tf_idf = lemma_tf * lemmas_idf.get(lemma, 0)

            query_vector.append(lemma_tf_idf)
        else:
            query_vector.append(0)

    # путь статьи, его вектор, значение схожести
    documents: list[(str, list[float], float)] = []

    # для каждой статьи создаем вектор
    for content_file in found_content_files:
        document_lemma = load_lemmas_info(content_file)
        current_vector = []

        for lemma in all_lemmas:
            if lemma in document_lemma:
                tf, tf_idf = document_lemma[lemma]
                current_vector.append(tf_idf)
            else:
                current_vector.append(0.0)

        sim_result = similarity(current_vector, query_vector)
        documents.append((content_file, current_vector, sim_result))

    documents.sort(key=lambda d: d[2], reverse=True)

    return documents

if __name__ == '__main__':
    query = "взлом страниц"
    result_documents = vector_search(query)

    # собираем инфу по результирующей выборке
    query_lemmas = lemmatize(tokenize(query))
    meta = load_meta()
    for content_file, v, sim_result in result_documents:
        print(meta[content_file])
        print('сходство', sim_result)

        lemmas_info = load_lemmas_info(content_file)
        lemmas = load_lemmas(content_file)
        tokens = load_tokens(content_file)

        for query_lemma in query_lemmas:
            if query_lemma in lemmas:
                for token in lemmas[query_lemma]:
                    print(token, ":", tokens[token])

        print()







