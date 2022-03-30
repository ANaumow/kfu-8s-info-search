import json
import math
import os
import re
import string
from os import walk

import nltk
from nltk.corpus import stopwords


def tokenize(content):
    russian_stopwords = stopwords.words('russian')
    english_stopwords = stopwords.words('english')
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
        return list(
            filter(lambda token: token.lower() not in russian_stopwords and token.lower() not in english_stopwords,
                   tokens))

    def filter_trash(tokens):
        return list(filter(letters_pattern.match, tokens))

    input_text = remove_tags(content)

    tokens = nltk.word_tokenize(input_text)

    tokens = filter_stopwords(tokens)
    tokens = filter_punctuation(tokens)
    tokens = filter_trash(tokens)

    # здесь лист, а не сет как в task2
    tokens = list(map(lambda t: t.lower(), tokens))

    return tokens


def prepare_content(raw_content):
    if '<div xmlns="http://www.w3.org/1999/xhtml">' in raw_content:
        result = re.findall(r'<div xmlns="http://www.w3.org/1999/xhtml">((.|\n)*?)<DIV class="v-portal"', raw_content)
        return result[0][0]
    if '<div id="mainbar" role="main.py" aria-label="question and answers">' in raw_content:
        result = re.findall(
            r'<div id="mainbar" role="main.py" aria-label="question and answers">((.|\n)*)?</div>((.|\n)*)?<div id="sidebar" class="show-votes" role="complementary" aria-label="sidebar">',
            raw_content)
        result2 = result[0][0]
        return result2
    else:
        return raw_content


if __name__ == '__main__':

    html_files_folder = '../archive/'
    lemma_files_folder = '../lemmas/'
    lemmas_file_prefix = lemma_files_folder + 'lemma_'

    filepath_list = []
    for (_, _, filenames) in walk(html_files_folder):
        filepath_list.extend(filenames)

    # лист из имени, кол-ва слов, словарь(токен, кол-во токена в файле), словарь(лем, список токенов)
    htmls: list[(str, int, dict[str, int]), dict[str, list[str]]] = []
    for filepath in filepath_list:

        with open(html_files_folder + filepath, 'r', encoding="utf-8") as file:
            file_content = file.read()

        token_list = tokenize(prepare_content(file_content))

        word_count = len(token_list)

        tokens_info: dict[str, int] = dict()
        for token in token_list:
            tokens_info[token] = tokens_info.get(token, 0) + 1

        lemmas = dict()
        with open(lemmas_file_prefix + filepath, 'r', encoding="utf-8") as lemma_file:
            lines = lemma_file.read().split("\n")
            for line in lines:
                if line == '':
                    continue

                words = line.split(" ")

                lemma_on_line = words[0]
                tokens_on_line = words[1:]
                lemmas[lemma_on_line] = tokens_on_line

        htmls.append((filepath, word_count, tokens_info, lemmas))


    with open("../htmls_data.json", 'w', encoding="utf-8") as index:
        index.truncate()
        json.dump(htmls, index, indent=4, sort_keys=True, ensure_ascii=False)


    for html_name, word_count, tokens_info, lemmas in htmls:
        tf_tokens = dict()
        idf_tokens = dict()
        tf_idf_tokens = dict()

        for token, token_count in tokens_info.items():
            token_tf = token_count / sorted(tokens_info.items(), key=lambda e: e[1], reverse=True)[0][1] # word_count
            token_idf = math.log2(len(htmls) / len(list(filter(lambda h: token in h[2], htmls))))

            tf_tokens[token] = token_tf
            idf_tokens[token] = token_idf
            tf_idf_tokens[token] = token_tf * token_idf

        tf_lemma = dict()
        idf_lemma = dict()
        tf_idf_lemma = dict()

        max_lemma_count = 0
        for lemma, tokens in lemmas.items():
            current_lemma_count = 0
            for token in tokens:
                token_count = tokens_info[token]
                current_lemma_count += token_count

            max_lemma_count = max([max_lemma_count, current_lemma_count])
            # for token in toke

        for lemma, tokens in lemmas.items():
            # lemma_tf = sum([tf_tokens[token] for token in tokens])
            lemma_tf = sum([tokens_info[token] for token in tokens]) / max_lemma_count
            lemma_idf = math.log2(len(htmls) / len(list(filter(lambda h: lemma in h[3], htmls))))

            tf_lemma[lemma] = lemma_tf
            idf_lemma[lemma] = lemma_idf
            tf_idf_lemma[lemma] = lemma_tf * lemma_idf


        token_dir_name = '../tokens_tf-idf/'
        tokens_file_prefix = token_dir_name + 'tokens_tf-idf_'

        os.makedirs(os.path.dirname(token_dir_name), exist_ok=True)
        with open(tokens_file_prefix + html_name, 'w', encoding="utf-8") as token_file:
            token_file.truncate()
            for token in tokens_info:
                token_file.write("{} {} {}\n".format(token, idf_tokens[token], tf_idf_tokens[token]))

        lemmas_dir_name = '../lemmas_tf-idf/'
        lemmas_file_prefix = lemmas_dir_name + 'lemma_tf-idf_'

        os.makedirs(os.path.dirname(lemmas_dir_name), exist_ok=True)
        with open(lemmas_file_prefix + html_name, 'w', encoding="utf-8") as lemma_file:
            lemma_file.truncate()
            for lemma in lemmas:
                lemma_file.write("{} {} {}\n".format(lemma, idf_lemma[lemma], tf_idf_lemma[lemma]))





