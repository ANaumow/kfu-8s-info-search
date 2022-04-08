import json
import os
import re
import string
from functools import reduce

import nltk

from nltk.corpus import stopwords
from pymystem3 import Mystem

def load_meta():
    with open("../task1/index.txt", 'r', encoding="utf-8") as file:
        return json.loads(file.read())


def read_content(content_file):
    with open(content_file, 'r', encoding="utf-8") as file:
        return file.read()

def save_lemmas(lemmas, content_file):
    content_filename = content_file.replace("../archive/", "")
    json_string = json.dumps(lemmas, indent=4, sort_keys=True, ensure_ascii=False)
    filedir = "../lemmas"
    filename = filedir + "/lemma_" + content_filename

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding="utf-8") as index:
        index.write(str(json_string))

def save_tokens(tokens, content_file):
    content_filename = content_file.replace("../archive/", "")
    json_string = json.dumps(tokens, indent=4, sort_keys=True, ensure_ascii=False)
    filedir = "../tokens"
    filename = filedir + "/token_" + content_filename

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding="utf-8") as index:
        index.write(str(json_string))


def tokenize(content):

    token_list = nltk.word_tokenize(content)

    # слово(токен) -> сколько раз встречается
    raw_tokens: dict[str, int] = {}
    for token in token_list:
        raw_tokens[token] = raw_tokens.setdefault(token, 0) + 1

    russian_stopwords = stopwords.words('russian')
    letters_pattern = re.compile("^[a-zA-Zа-яА-я]+$")

    filtered_tokens = {}
    for token in raw_tokens:
        if token not in russian_stopwords and \
                token not in string.punctuation and \
                letters_pattern.match(token):  # оставляем русские и англ слова
            filtered_tokens[token.lower()] = raw_tokens[token]

    return filtered_tokens

def lemmatize(tokens):
    mystem = Mystem()

    # tooooo slow
    # for token in tokens:
    #     lemma = mystem.lemmatize(token)[0]
    #     lemma_dict.setdefault(lemma, []).append(token)

    # super fast
    tokens_in_one_line = reduce(lambda a, b: a + '|' + b, tokens)
    lemma_list = mystem.lemmatize(tokens_in_one_line)
    lemma_list = list(filter(lambda l: l not in ['|', '\n'], lemma_list))

    # лемма -> список токенов
    lemmas: dict[str, list[str]] = {}
    for i, token in enumerate(tokens):
        lemma_for_token = lemma_list[i]
        # собираем токены по леммам
        lemmas.setdefault(lemma_for_token, []).append(token)

    return lemmas

if __name__ == '__main__':
    meta = load_meta()

    for content_file in meta:
        content = read_content(content_file)

        tokens = tokenize(content)
        lemmas = lemmatize(tokens)

        save_tokens(tokens, content_file)
        save_lemmas(lemmas, content_file)
