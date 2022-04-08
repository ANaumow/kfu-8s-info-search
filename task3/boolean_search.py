import json
from os import walk

from task2.main import load_meta
from task3.parser import parser

html_files_folder = '../archive/'

def load_term_index():
    with open("../task3/term_index.json", 'r', encoding="utf-8") as index_file:
        return json.loads(index_file.read())

# работает только с леммами
def boolean_search(query):

    # прочитали индекс
    index = load_term_index()

    # построили дерево по запросу
    root_node = parser.parse(query)

    # прочитали какие статьи вообще есть
    content_files = load_meta()

    # сюда кладем подходящие для запроса статьи
    result_html_list = []

    # проходимся по ВСЕМ стаьям
    for html in content_files:

        # проверяем подходит ли статья под запрос
        suits = root_node.eval(index, html)

        # если проходит сохраняем
        if suits:
            result_html_list.append(html)

    return result_html_list

if __name__ == '__main__':

    search_result = boolean_search("дефицит")

    print(len(search_result))
    print(search_result)

    search_result = boolean_search("дефицит & ! конкурировать")

    print(len(search_result))
    print(search_result)


