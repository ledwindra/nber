import argparse
import os
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from random import randint
from time import sleep

class Wikipedia:

    def __init__(self):
        self.timeout = args.timeout
        self.user_agent = args.user_agent

    def nested_author(self):
        author = pd.read_csv('data/nber.zip', sep='|')
        author = author.loc[:, 'citation_author'] .to_list()
        author = [re.sub('[^A-Za-z0-9,\' ]+', '', x) for x in author]
        author = [x.split('\'') for x in author]

        return author

    def unnest_author(self, nested_author):
        author = []
        for i in nested_author:
            for j in i:
                author.append(j)

        author = [x for x in author if x != '' and x != ', ']
        author = [x.split(', ') for x in author]
        author = [x[::-1] for x in author]
        author = ['_'.join(x) for x in author]

        return author

    def profile(self, row, author):
        headers = {'User-Agent': self.user_agent}

        # request to wikipedia
        status_code = None
        try:
            url = f'https://en.wikipedia.org/wiki/{author[row]}_(economist)'
            res = requests.get(url, timeout=self.timeout, headers=headers)
            res.raise_for_status()
        except requests.exceptions.HTTPError:
            url = f'https://en.wikipedia.org/wiki/{author[row]}'
            res = requests.get(url, timeout=self.timeout, headers=headers)
        
        # get biography
        try:
            content = BeautifulSoup(res.content, features='html.parser')
            table = content.find('table', {'class': 'infobox biography vcard'}).find_all('tr')
            biography = {}
            for t in table[1:]:
                try:
                    column = [x for x in t.find('th').get_text() if x.isalpha() == True]
                    column = [x.lower() for x in column]
                    column = ''.join(column)
                    biography[column] = [x.get('title') for x in t.find_all('a')]
                except AttributeError:
                    pass
            
            df = pd.DataFrame([biography])
            df.insert(0, 'wikipedia', author[row])
                
            return df
        
        except AttributeError:
            return None

def main():
    wikipedia = Wikipedia()
    nested_author = wikipedia.nested_author()
    author = wikipedia.unnest_author(nested_author)
    file_name = './data/wikipedia.csv'
    if os.path.exists(file_name):
        existing = pd.read_csv(file_name, sep='|')
    i = 0
    data = []
    while i < args.profile:
        try:
            row = randint(0, len(author))
            df = wikipedia.profile(row, author)
            data.append(df)
        except Exception:
            pass
        i += 1
    try:
        df = pd.concat(data, sort=False)
        df = pd.concat([df, existing], sort=False)
        df = df.drop_duplicates(subset=['wikipedia'])
        df = df.sort_values(by='wikipedia', ascending=True)
        df.to_csv(file_name, index=False, sep='|')
    except UnboundLocalError:
        df = pd.concat(data, sort=False)
        df.to_csv(file_name, index=False, sep='|')
    except ValueError:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--profile',
        type=int,
        default=10,
        help='How many profiles will be scraped (default is 10)',
        metavar=''
    )
    parser.add_argument(
        '-t',
        '--timeout',
        type=int,
        default=5,
        help='How long for each request before it timed out in seconds (default is 5)',
        metavar=''
    )
    parser.add_argument(
        '-s',
        '--sleep',
        type=int,
        default=5,
        help='How long to make time interval between iterations in case exception occurs in seconds (default is 10)',
        metavar=''
    )
    parser.add_argument(
        '-u',
        '--user-agent',
        type=str,
        default='user-agent',
        help='User agent used for headers (default is user-agent)',
        metavar=''
    )
    args = parser.parse_args()
    main()
