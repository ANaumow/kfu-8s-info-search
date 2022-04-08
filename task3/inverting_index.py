import json

from task2.main import load_meta


def load_lemmas(content_file):
    content_filename = content_file.replace("../archive/", "")

    # вычисляю путь до файла с леммами для текущей страницы
    lemma_filename = lemmas_files_folder + "lemma_" + content_filename

    with open(lemma_filename, 'r', encoding="utf-8") as file:
        return json.loads(file.read())

def save_term_index(term_index):
    with open("./term_index.json", 'w', encoding="utf-8") as index:
        json.dump(term_index, index, indent=4, sort_keys=True, ensure_ascii=False)


lemmas_files_folder = '../lemmas/'
html_files_folder = '../archive/'

if __name__ == '__main__':

    # объявил свой индекс
    term_index: dict[str, list[str]] = {}

    meta = load_meta()
    for content_file in meta:

        # леммы в данной статье
        lemmas = load_lemmas(content_file)

        for lemma in lemmas:
            term_index.setdefault(lemma, []).append(content_file)

    save_term_index(term_index)
