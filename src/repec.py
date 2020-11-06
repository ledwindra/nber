import argparse
import os
from os import stat
import pandas as pd
import requests
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup
from random import randint
from time import sleep

class ID:
    def __init__(self):
        self.df = pd.read_csv('data/nber.csv')
        self.length = len(self.df) - 1
        self.nber_id = self.df.id[randint(0, self.length)]

class RePEc:

    def __init__(self, nber_id):
        self.url = 'http://citec.repec.org/api/plain/RePEc:nbr:nberwo:'
        self.file_name = './data/repec.csv'
        self.nber_id = nber_id

    def string_id(self):
        if self.nber_id < 10: return f'000{self.nber_id}'
        elif 10 <= self.nber_id < 100: return f'00{self.nber_id}'
        elif 100 <= self.nber_id < 1000: return f'0{self.nber_id}'
        else: return str(self.nber_id)

    def citation(self, xml_find):
        status_code = None
        while status_code != 200:
            try:
                url = f'{self.url}{self.string_id()}'
                response = requests.get(url)
                status_code = response.status_code
                xml = et.fromstring(response.text)
                # either cites or citedBy
                xml = int(xml.find(xml_find).text)
                if status_code == 200:
                    try: return xml
                    except UnboundLocalError: return None
            except Exception as err:
                print(f'{err}: {self.nber_id}')
                continue

    def reference(self):
        status_code = None
        while status_code != 200:
            try:
                url = f'http://citec.repec.org/api/amf/RePEc:nbr:nberwo:{self.string_id()}'
                response = requests.get(url)
                status_code = response.status_code
                parser = et.XMLParser(encoding='utf-8')
                xml = et.fromstring(response.text, parser=parser)
                text = list(xml)[0]
                reference = [list(x)[0].text for x in text if 'isreferencedby' not in x.tag]
                if status_code == 200:
                    try:
                        return reference
                    except UnboundLocalError:
                        return None
            except Exception as err:
                print(f'{err}: {self.nber_id}')
                continue

    def create(self):
        return pd.DataFrame([{
            'id': self.nber_id,
            'cites': self.citation('cites'),
            'cited_by': self.citation('citedBy'),
            'reference': self.reference()
        }])

    def existing(self):
        existing = pd.read_csv(self.file_name)
        df = pd.concat([self.create(), existing], sort=False)
        df = df.drop_duplicates(subset=['id'])
        return df.sort_values(by='id', ascending=True)
    
    def save(self):
        if os.path.exists(self.file_name):
            self.existing().to_csv(self.file_name, index=False)
        else:
            self.create().to_csv(self.file_name, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--total', type=int, default=5, help='Total paper(s) that will be downloaded', metavar='')
    args = parser.parse_args()
    i = 0
    while i < args.total:
        repec = RePEc(ID().nber_id)
        repec.save()
        i += 1
