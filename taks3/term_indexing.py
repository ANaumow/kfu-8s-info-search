import json
from os import walk

lemmas_files_folder = '../lemmas/'
html_files_folder = '../archive/'


if __name__ == '__main__':
    term_index: dict[str, list[str]] = {}

    for (_, _, filenames) in walk(html_files_folder):

        for html_filename in filenames:
            lemma_filename = lemmas_files_folder + "lemma_" + html_filename

            with open(lemma_filename, 'r', encoding="utf-8") as file:

                file_content = file.read()

                lines = file_content.split("\n")
                for line in lines:
                    words = line.split(" ")

                    lemma_on_line = words[0]
                    term_index.setdefault(lemma_on_line, []).append(html_filename)

    json_string = json.dumps(term_index, indent=4, sort_keys=True, ensure_ascii=False)

    with open("./term_index.json", 'w', encoding="utf-8") as index:
        index.truncate()
        json.dump(term_index, index, indent=4, sort_keys=True, ensure_ascii=False)





