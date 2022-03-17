import re

import requests

if __name__ == '__main__':
    path = 'https://stackoverflow.com/questions/tagged/java?tab=frequent&page=1&pagesize=50'

    pages = 10

    paths = []
    for page in range(pages):
        paths.append("https://stackoverflow.com/questions/tagged/java?tab=frequent&page={}&pagesize=50".format(str(page)))

    contents = []

    for path in paths:
        resp = requests.get(path)
        contents.append(resp.content.decode("utf-8"))


    # <a href="/questions/4216745/java-string-to-date-conversion" class="s-link">Java string to date conversion</a>
    # https://stackoverflow.com/questions/4216745/java-string-to-date-conversion

    article_pages=[]

    for content in contents:
        result = re.findall(r'<a href="(.*)" class="s-link">', content)

        for article in result:
            # print(article)
            article_pages.append("https://stackoverflow.com" + article)

    with open('source_links.txt', 'w') as out_file:
        for page in article_pages:
            out_file.write(page + '\n')
