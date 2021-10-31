import itertools
import json
import os
import requests
from bs4 import BeautifulSoup
from proxy import Proxy

class Wikipedia:
    def get_data(self):
        data = os.listdir('data/nber')
        data = [json.load(open(f'data/nber/{x}', 'r')) for x in data]
        
        return data

    def get_author(self, data):
        author = []
        for i in data:
            for j in i['citation_author']:
                author.append(j)

        author = list(set(author))
        author = sorted([x.replace('.', '').replace(' ', '_') for x in author])

        return author

    def get_author_combination(self, author):
        author_comb = []
        for a in author:
            a = a.split('_')
            a = [list(itertools.combinations(a, x)) for x in range(len(a)+1)]
            for i in a:
                for j in i:
                    author_comb.append('_'.join(j))

        author_comb = sorted(list(set(author_comb)))

        return author_comb

    def profile(self, author):
        try:
            url = f'https://en.wikipedia.org/wiki/{author}_(economist)'
            print(f'[GET \U0001F4BE]: {url}')
            proxy = {'https': Proxy().get_proxy()}
            response = requests.get(url, proxies=proxy, timeout=5)
            if response.status_code == 404:
                url = f'https://en.wikipedia.org/wiki/{author}'
                print(f'[GET \U0001F4BE]: {url}')
                response = requests.get(url, proxies=proxy, timeout=5)
            return response
        except:
            pass

    def biography(self, response):
        try:
            content = BeautifulSoup(response.content, features='html.parser')
            text = content.get_text()
            if 'economist' in text.lower():
                table = content.find('table', {'class': 'infobox biography vcard'}).find_all('tr')
                data = {}
                for t in table[1:]:
                    try:
                        column = [x for x in t.find('th').get_text() if x.isalpha() == True]
                        column = [x.lower() for x in column]
                        column = ''.join(column)
                        data[column] = [x.get('title') for x in t.find_all('a')]
                    except AttributeError:
                        pass

                return data

        except AttributeError:
            return None

    def save_data(self, file_name,  data):
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)


if __name__ == "__main__":
    wikipedia = Wikipedia()
    data = wikipedia.get_data()
    author = wikipedia.get_author(data)
    author = wikipedia.get_author_combination(author)
    for a in author:
        file_name = f"data/wikipedia/{a.replace('_', '-').lower()}.json"
        if not os.path.exists(file_name):
            response = wikipedia.profile(a)
            data = wikipedia.biography(response)
            if data != None:
                wikipedia.save_data(file_name, data)
                print(f'[SUCCEED \U00002705]: {a}')
