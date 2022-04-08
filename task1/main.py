import json
import os
import re
from bs4 import BeautifulSoup
import codecs

import requests

if __name__ == '__main__':
    path = 'https://habr.com/ru/top/yearly/'

    suitable_html = 0

    pages = 10
    paths = [path + 'page' + str(x + 1) + "/" for x in range(pages)]

    # массив сырых страниц с сылками на страницы со статьями(page1, page2)
    contents = []

    # скачиваем файлы в массив
    for path in paths:
        resp = requests.get(path)
        contents.append(resp.content.decode("utf-8"))

    article_ids = []
    for content in contents:
        result = re.findall(r'<article id="[0-9]*', content)

        for article in result:
            # print(article)
            article_ids.append(int(article[13:]))

    # массив с ссылками на статьи
    article_pages = ['https://habr.com/ru/post/' + str(x) + '/' for x in article_ids]

    # словарь путь до файла -> ссылка на статью
    meta = {}

    for i, url in enumerate(article_pages):

        if suitable_html >= 100:
            break

        # скачиваем статью
        response = requests.get(url)
        decoded_content = response.content

        # убираем html
        soup = BeautifulSoup(decoded_content, "html.parser")
        text = " ".join(soup.get_text().split())

        word_count = len(text.split(" "))

        if word_count < 1000:
            continue
        else:
            suitable_html += 1

        print(text)

        # сохраняем в файлы
        filename = '../archive/' + str(suitable_html) + '.txt'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with codecs.open(filename, "w", "utf-8") as out_file:
            out_file.write(text)

        # запоминаем какой файл отвечает за текущую статью
        meta[filename] = url

    # сохраняем индекс
    json_string = json.dumps(meta, indent=4, sort_keys=True)
    with open("./index.txt", 'w') as index:
        index.write(str(json_string))
