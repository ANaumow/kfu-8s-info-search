import os

import requests as requests
import json

if __name__ == '__main__':
    input_file = 'source_links.txt'

    meta = {}

    with open(input_file, 'r') as in_file:

        i = 0
        while True:
            url = in_file.readline()
            url = url[:-1]  # remove '\n' ending
            if url == '':
                break

            response = requests.get(url)
            decoded_content = response.content

            filename = '../archive/' + str(i) + '.txt'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'wb') as out_file:
                out_file.write(decoded_content)

            meta[filename] = url

            i += 1

        json_string = json.dumps(meta, indent=4, sort_keys=True)

        with open("./index.txt", 'w') as index:
            index.write(str(json_string))
