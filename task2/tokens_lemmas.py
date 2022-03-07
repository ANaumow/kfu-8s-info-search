import os
import re
import string
from functools import reduce
from os import walk

import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem


def tokenize(content):
    russian_stopwords = stopwords.words('russian')
    letters_pattern = re.compile("^[a-zA-Zа-яА-я]+$")

    def remove_tags(text):
        cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", text.strip())
        # Then we remove html comments. This has to be done before removing regular
        # tags since comments can contain '>' characters.
        cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
        # Next we can remove the remaining tags:
        cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
        # Finally, we deal with whitespace
        cleaned = re.sub(r"&nbsp;", " ", cleaned)
        cleaned = re.sub(r"  ", " ", cleaned)
        cleaned = re.sub(r"  ", " ", cleaned)
        return cleaned.strip()

    def filter_punctuation(tokens):
        return list(filter(lambda token: token not in string.punctuation, tokens))

    def filter_stopwords(tokens):
        return list(filter(lambda token: token.lower() not in russian_stopwords, tokens))

    def filter_trash(tokens):
        return list(filter(letters_pattern.match, tokens))

    input_text = remove_tags(content)

    tokens = nltk.word_tokenize(input_text)

    tokens = filter_stopwords(tokens)
    tokens = filter_punctuation(tokens)
    tokens = filter_trash(tokens)
    tokens = set(map(lambda t: t.lower(), tokens))

    return tokens

def group_tokens_by_lemmas(tokens):
    lemma_dict = {}
    mystem = Mystem()

    # tooooo slow
    # for token in tokens:
    #     lemma = mystem.lemmatize(token)[0]
    #     lemma_dict.setdefault(lemma, []).append(token)

    # super fast
    tokens_in_one_line = reduce(lambda a, b: a + '|' + b, tokens)
    lemma_list = mystem.lemmatize(tokens_in_one_line)
    lemma_list = list(filter(lambda l: l not in ['|', '\n'], lemma_list))

    for (token_index, token) in enumerate(tokens):
        lemma = lemma_list[token_index]
        lemma_dict.setdefault(lemma, []).append(token)

    return lemma_dict

def prepare_content(raw_content):
    result = re.findall(r'<div xmlns="http://www.w3.org/1999/xhtml">((.|\n)*?)<DIV class="v-portal"', raw_content)
    return result[0][0]


if __name__ == '__main__':
    # папка с html страницами
    html_files_folder = '../archive/'

    filepath_list = []
    for (_, _, filenames) in walk(html_files_folder):
        filepath_list.extend(filenames)

    for filepath in filepath_list:

        with open(html_files_folder + filepath, 'r', encoding="utf-8") as file:
            file_content = file.read()

        content = prepare_content(file_content)

        # токенизация

        tokens = tokenize(content)

        dir_name = '../tokens/'
        tokens_file_prefix = dir_name + 'tokens_'

        os.makedirs(os.path.dirname(dir_name), exist_ok=True)
        with open(tokens_file_prefix + filepath, 'w', encoding="utf-8") as lemma_file:
            for token in tokens:
                lemma_file.write(token + '\n')

        # лемматизация

        lemma_dict = group_tokens_by_lemmas(tokens)

        dir_name = '../lemmas/'
        lemmas_file_prefix = dir_name + 'lemma_'

        os.makedirs(os.path.dirname(dir_name), exist_ok=True)
        with open(lemmas_file_prefix + filepath, 'w', encoding="utf-8") as lemma_file:
            for lemma, tokens in lemma_dict.items():
                lemma_file.write(lemma + " " + reduce(lambda s1, s2: s1 + " " + s2, tokens) + '\n')

