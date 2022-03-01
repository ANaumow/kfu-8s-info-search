import re

import requests

if __name__ == '__main__':
    path = 'https://habr.com/ru/top/yearly/'

    pages = 10

    paths = [path + 'page' + str(x + 1) + "/" for x in range(pages)]

    contents = []

    for path in paths:
        resp = requests.get(path)
        contents.append(resp.content.decode("utf-8"))

    article_ids = []

    for content in contents:
        result = re.findall(r'<article id="[0-9]*', content)

        for article in result:
            # print(article)
            article_ids.append(int(article[13:]))

    article_pages = ['https://habr.com/ru/post/' + str(x) + '/' for x in article_ids]

    with open('source_links.txt', 'w') as out_file:
        for page in article_pages:
            out_file.write(page + '\n')
