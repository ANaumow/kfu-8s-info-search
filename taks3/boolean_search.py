import json
from os import walk
import parcer

html_files_folder = '../archive/'

def boolean_search(input, index: dict[str, list[str]]):

    root_node = parcer.parse(input)

    html_files = []
    for (_, _, filenames) in walk(html_files_folder):
        html_files.extend(filenames)

    result_html_list = []
    for html in html_files:
        if root_node.eval(index, html):
            result_html_list.append(html)

    return result_html_list

if __name__ == '__main__':

    with open("./term_index.json", 'r', encoding="utf-8") as index:
        html_to_lemmas = json.loads(index.read())

    search_result = boolean_search("best & (way | find) & element", html_to_lemmas)

    print(len(search_result))
    print(search_result)


    search_result = boolean_search("best & way | find & element", html_to_lemmas)

    print(len(search_result))
    print(search_result)

