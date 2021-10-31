import argparse
import json
import os
import requests
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup
from datetime import datetime
from proxy import Proxy
from requests import exceptions

class RePEc:

    def __init__(self, nber_id):
        self.nber_id = nber_id
        self.url = 'http://citec.repec.org/api/plain/RePEc:nbr:nberwo:'

    def timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def string_id(self):
        '''Returns the string format for the NBER ID. For NBER ID above 1000 it will return itself.
        '''

        if self.nber_id < 10: return f'000{self.nber_id}'
        elif 10 <= self.nber_id < 100: return f'00{self.nber_id}'
        elif 100 <= self.nber_id < 1000: return f'0{self.nber_id}'
        else: return str(self.nber_id)

    def citation(self, timeout=5):
        '''Returns either numbers of citations or numbers of being cited if any, otherwise returns nothing.
        '''
        status_code = None
        while status_code != 200:
            try:
                url = f'{self.url}{self.string_id()}'
                proxy = {'http': Proxy().get_proxy()}
                print(f'{self.timestamp()} {url} DOWNLOAD CITATION \U0001F4BE')
                response = requests.get(url, timeout=timeout, proxies=proxy)
                status_code = response.status_code
                try:
                    xml = et.fromstring(response.text)
                    return xml
                except UnboundLocalError: return None
                except et.ParseError: return None
            except exceptions.ConnectionError:
                print(f'{self.timestamp()} {url} CONNECTION ERROR \U0001F494')
                continue

    def reference(self, timeout=5):
        '''Returns a list of references for the corresponding NBER paper.
        '''
        status_code = None
        while status_code != 200:
            try:
                proxy = {'http': Proxy().get_proxy()}
                url = f'http://citec.repec.org/api/amf/RePEc:nbr:nberwo:{self.string_id()}'
                print(f'{self.timestamp()} {url} DOWNLOAD REFERENCE \U0001F4BE')
                response = requests.get(url, timeout=timeout, proxies=proxy)
                status_code = response.status_code
                try:
                    parser = et.XMLParser(encoding='utf-8')
                    xml = et.fromstring(response.text, parser=parser)
                    text = list(xml)[0]
                    reference = [list(x)[0].text for x in text if 'isreferencedby' not in x.tag]
                    return reference
                except UnboundLocalError: return None
                except IndexError: return None
                except et.ParseError: return None
            except exceptions.ConnectionError:
                print(f'{self.timestamp()} {url} CONNECTION ERROR \U0001F494')
                continue

    def create_dictionary(self):
        '''Create a dictionary from the parsed XML object.
        '''
        xml = self.citation()
        try:
            cites = int(xml.find('cites').text)
            cited_by = int(xml.find('citedBy').text)
        except AttributeError:
            cites, cited_by = None, None

        data = {'id': self.nber_id, 'cites': cites, 'cited_by': cited_by, 'reference': self.reference()}

        return data

    def save(self):
        '''Save the paper using JSON format.
        '''
        data = self.create_dictionary()
        with open(f'data/repec/{self.nber_id}.json', 'w') as file:
            json.dump(data, file, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start', type=int, default=0, help='Starting NBER ID', metavar='')
    parser.add_argument('-e', '--end', type=int, default=5, help='Ending NBER ID', metavar='')
    args = parser.parse_args()
    start = args.start
    end = args.end
    while start < end:
        repec = RePEc(start)
        file_check = os.path.exists(f'data/repec/{start}.json')
        if file_check:
            print(f'{repec.timestamp()} {repec.url}{repec.string_id()} IGNORE \U0001F4C1')
        else:
            repec.save()
            print(f'{repec.timestamp()} {repec.url}{repec.string_id()} SUCCEED \U00002705')
        start += 1
