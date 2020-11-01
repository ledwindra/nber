import argparse
import os
import pandas as pd
import requests
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup
from random import randint
from time import sleep

class NBER:
    
    def __init__(self):
        self.id = args.initial_id
        self.paper = args.paper
        self.timeout = args.timeout
        self.sleep = args.sleep
        self.user_agent = args.user_agent

    def get_latest_paper(self, headers):
        url = 'https://data.nber.org/new.html#latest'
        try:
            response = requests.get(url, timeout=self.timeout, headers=headers)
            content = BeautifulSoup(response.content, features='html.parser')
            latest = content.find('li', {'class': 'multiline-li'})
            latest = latest.find('a').attrs['href']
            latest = int(''.join([x for x in latest if x.isnumeric() == True]))
            return latest
        except Exception:
            return 1

    def get_total_cites(self, nber_id, headers):
        try:
            if 0 <= nber_id < 10:
                nber_id = f'000{nber_id}'
            elif 10 <= nber_id < 100:
                nber_id = f'00{nber_id}'
            elif 100 <= nber_id < 1000:
                nber_id = f'0{nber_id}'
            status_code = None
            while status_code != 200:
                try:
                    url = f'http://citec.repec.org/api/plain/RePEc:nbr:nberwo:{nber_id}'
                    response = requests.get(url, timeout=self.timeout, headers=headers)
                    status_code = response.status_code
                    xml = et.fromstring(response.text)
                    total_cites = int(xml.find('cites').text)
                except Exception:
                    print(f'Exception happens to get total cited by in WP {nber_id}. Don\'t worry, we\'ll try again.')
                    continue
        except UnboundLocalError:
            total_cites = None
        
        try:
            return total_cites
        except UnboundLocalError:
            return None

    def get_cited_by(self, nber_id, headers):
        try:
            if 0 <= nber_id < 10:
                nber_id = f'000{nber_id}'
            elif 10 <= nber_id < 100:
                nber_id = f'00{nber_id}'
            elif 100 <= nber_id < 1000:
                nber_id = f'0{nber_id}'
            status_code = None
            while status_code != 200:
                try:
                    url = f'http://citec.repec.org/api/plain/RePEc:nbr:nberwo:{nber_id}'
                    response = requests.get(url, timeout=self.timeout, headers=headers)
                    status_code = response.status_code
                    xml = et.fromstring(response.text)
                    cited_by = int(xml.find('citedBy').text)
                except Exception:
                    print(f'Exception happens to get total cited by in WP {nber_id}. Don\'t worry, we\'ll try again.')
                    continue
        except UnboundLocalError:
            cited_by = None
        
        try:
            return cited_by
        except UnboundLocalError:
            return None

    def get_reference(self, nber_id, headers):
        if 0 <= nber_id < 10:
            nber_id = f'000{nber_id}'
        elif 10 <= nber_id < 100:
            nber_id = f'00{nber_id}'
        elif 100 <= nber_id < 1000:
            nber_id = f'0{nber_id}'
        status_code = None
        while status_code != 200:
            try:
                url = f'http://citec.repec.org/api/amf/RePEc:nbr:nberwo:{nber_id}'
                response = requests.get(url, timeout=self.timeout, headers=headers)
                status_code = response.status_code
                xml = et.fromstring(response.text)
                text = xml.getchildren()[0]
                reference = [x.getchildren()[0].text for x in text.getchildren() if 'isreferencedby' not in x.tag]
            except Exception:
                print(f'Exception happens to get references in WP {nber_id}. Don\'t worry, we\'ll try again.')
                continue
        try:
            return reference
        except UnboundLocalError:
            return None

    def get_paper(self, paper_id, total_cites, cited_by, reference):
        paper = {
            'id': paper_id,
            'total_cites': total_cites,
            'cited_by': cited_by,
            'reference': reference
        }

        return paper

def main():
    file_name = './data/repec.zip'
    # if file already exists, it will check as follows:
    if os.path.exists(file_name):
        existing = pd.read_csv(file_name, sep='|')
    nber = NBER()
    headers = {'User-Agent': nber.user_agent}
    i = 0
    data = []
    while i < nber.paper:        
        nber_id = randint(nber.id, nber.get_latest_paper(headers))
        # whether current ID already exists in the existing file or not
        if nber_id not in existing['id'].to_list():
            url = f'https://www.nber.org/papers/w{nber_id}'
            print(f'Current paper: {url}')
            try:
                response = requests.get(url, timeout=nber.timeout, headers=headers)
                content = BeautifulSoup(response.content, features='html.parser')
                paper = nber.get_paper(
                    paper_id = nber_id,
                    total_cites = nber.get_total_cites(nber_id, headers),
                    cited_by = nber.get_cited_by(nber_id, headers),
                    reference = nber.get_reference(nber_id, headers)
                )
                df = pd.DataFrame([paper])
                data.append(df)
            except Exception:
                print(f'Exception happens to get WP {nber_id}. Don\'t worry, we\'ll try again.')
                sleep(nber.sleep)
                continue
        i += 1
    try:
        df = pd.concat(data, sort=False)
        df = pd.concat([df, existing], sort=False)
        df.drop_duplicates(subset=['id'])
        df.to_csv(file_name, index=False, header=True, sep='|')
    except ValueError:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--initial_id',
        type=int,
        default=1,
        help='NBER Working Paper ID to begin with (default is 1)',
        metavar=''
    )
    parser.add_argument(
        '-p',
        '--paper',
        type=int,
        default=3,
        help='How many papers will be scraped for each cron job (default is 10)',
        metavar=''
    )
    parser.add_argument(
        '-t',
        '--timeout',
        type=int,
        default=10,
        help='How long for each request before it timed out in seconds (default is 5)',
        metavar=''
    )
    parser.add_argument(
        '-s',
        '--sleep',
        type=int,
        default=10,
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
