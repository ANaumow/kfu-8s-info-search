import json
import math
import os

from task2.main import load_meta


from task3.boolean_search import load_term_index
from task3.inverting_index import load_lemmas


def load_tokens(content_file):
    content_filename = content_file.replace("../archive/", "")

    # вычисляю путь до файла с леммами для текущей страницы
    tokens_filename = "../tokens/token_" + content_filename

    with open(tokens_filename, 'r', encoding="utf-8") as file:
        return json.loads(file.read())


def save_lemma_info(lemmas_info, content_file):
    content_filename = content_file.replace("../archive/", "")

    # вычисляю путь до файла с леммами для текущей страницы
    lemmas_filename = "../lemmas_info/lemma_info_" + content_filename
    os.makedirs(os.path.dirname(lemmas_filename), exist_ok=True)
    with open(lemmas_filename, 'w', encoding="utf-8") as file:
        json.dump(lemmas_info, file, indent=4, sort_keys=True, ensure_ascii=False)


def save_lemmas_idf(lemmas_idf):
    lemmas_filename = "../task4/lemmas_idf.json"

    with open(lemmas_filename, 'w', encoding="utf-8") as file:
        json.dump(lemmas_idf, file, indent=4, sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    meta = load_meta()

    # путь статьи -> кол-ва слов
    content_info: dict[str, int] = {}

    for content_file in meta:
        tokens = load_tokens(content_file)
        word_count = 0

        for token in tokens:
            token_count = tokens[token]
            word_count += token_count

        content_info[content_file] = word_count

    # считаем идф
    index = load_term_index()
    lemmas_idf = dict()
    for lemma in index:
        articles_with_lemma = index[lemma]
        document_with_lemma_count = len(articles_with_lemma)
        document_count = len(content_info)
        idf = math.log2(document_count / document_with_lemma_count)
        idf = round(idf, 6)
        lemmas_idf[lemma] = idf
    save_lemmas_idf(lemmas_idf)

    # считаем тф и тф-идф
    for content_file in content_info:

        lemmas = load_lemmas(content_file)
        tokens = load_tokens(content_file)
        word_count = content_info[content_file]

        # лемма -> (тф, тф-идф)
        lemma_info: dict[str, (float, float)] = {}

        for lemma in lemmas:
            tokens_of_lemma = lemmas[lemma]

            lemma_count = 0
            for token in tokens_of_lemma:
                token_count = tokens[token]
                lemma_count += token_count

            lemma_tf = lemma_count / word_count
            lemma_tf_idf = lemma_tf * lemmas_idf[lemma]

            lemma_tf = round(lemma_tf, 6)
            lemma_tf_idf = round(lemma_tf_idf, 6)

            lemma_info[lemma] = (lemma_tf, lemma_tf_idf)

        save_lemma_info(lemma_info, content_file)
