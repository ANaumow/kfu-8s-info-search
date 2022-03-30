import json
from os import walk
import taks3.parcer

html_files_folder = '../archive/'

def boolean_search(query):

    with open("../taks3/term_index.json", 'r', encoding="utf-8") as index_file:
        index = json.loads(index_file.read())

    root_node = taks3.parcer.parse(query)

    html_files = []
    for (_, _, filenames) in walk(html_files_folder):
        html_files.extend(filenames)

    result_html_list = []
    for html in html_files:
        if root_node.eval(index, html):
            result_html_list.append(html)

    return result_html_list

if __name__ == '__main__':



    search_result = boolean_search("best & (way | find) & element")

    print(len(search_result))
    print(search_result)


    search_result = boolean_search("best & way | find & element")

    print(len(search_result))
    print(search_result)

