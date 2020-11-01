import argparse
import os
import pandas as pd
import requests
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

    def get_citation_item(self, content, item):
        item = content.find('meta', {'name': f'{item}'})
        try:
            item = item.attrs['content']
        except AttributeError:
            item = None

        return item

    def get_citation_author(self, content):
        author = content.find_all('meta', {'name': 'citation_author'})
        author = [x.get('content') for x in author]

        return author

    def get_topics(self, content):
        try:
            bibtop = content.find('p', {'class': 'bibtop'})
            topics = bibtop.find_all('a')
            topics = [x.get_text() for x in topics]
        except AttributeError:
            topics = None

        return topics

    def get_abstract(self, content):
        try:
            abstract = content.find('p', {'style': 'margin-left: 40px; margin-right: 40px; text-align: justify'})
            abstract = abstract.contents[0].replace('\n', '')
            if '\x00' in abstract:
                abstract = abstract.replace('\x00', '')
        except AttributeError:
            abstract = None

        return abstract

    def get_also_downloaded(self, content):
        try:
            also_downloaded = content.find('table', {'class': 'also-downloaded'})
            also_downloaded = also_downloaded.find_all('td')
            also_downloaded = [x.find('a') for x in also_downloaded if x.find('a') != None]
            also_downloaded = [x.attrs['href'] for x in also_downloaded]
        except AttributeError:
            also_downloaded = None

        return also_downloaded

    def get_acknowledgement(self, nber_id, headers):
        url = f'https://www.nber.org/papers/w{nber_id}.ack'
        ack = requests.get(url, timeout=self.timeout, headers=headers)
        content = BeautifulSoup(ack.content, features='html.parser')
        ack = content.find_all('div', {'align': 'left'})[0]
        ack = ack.get_text()
        ack = ack.split(' ')
        ack = ' '.join([x for x in ack if x.isalpha() == True])

        return ack

    def get_paper(
        self,
        paper_id,
        citation_title,
        citation_author,
        citation_date,
        citation_publication_date,
        citation_technical_report_institution,
        citation_technical_report_number,
        citation_journal_title,
        citation_journal_issn,
        citation_pdf_url,
        topics,
        abstract,
        also_downloaded,
        acknowledgement
    ):
        paper = {
            'id': paper_id,
            'citation_title': citation_title,
            'citation_author': citation_author,
            'citation_date': citation_date,
            'citation_publication_date': citation_publication_date,
            'citation_technical_report_institution': citation_technical_report_institution,
            'citation_technical_report_number': citation_technical_report_number,
            'citation_journal_title': citation_journal_title,
            'citation_journal_issn': citation_journal_issn,
            'citation_pdf_url': citation_pdf_url,
            'topics': topics,
            'abstract': abstract,
            'also_downloaded': also_downloaded,
            'acknowledgement': acknowledgement
        }

        return paper

def main():
    file_name = './data/nber.zip'
    if os.path.exists(file_name):
        existing = pd.read_csv(file_name, sep='|')
    nber = NBER()
    headers = {'User-Agent': nber.user_agent}
    i = 0
    data = []
    while i < nber.paper:
        nber_id = randint(nber.id, nber.get_latest_paper(headers))
        if nber_id not in existing['id'].to_list():
            url = f'https://www.nber.org/papers/w{nber_id}'
            print(f'Current paper: {url}')
            try:
                response = requests.get(url, timeout=nber.timeout, headers=headers)
                content = BeautifulSoup(response.content, features='html.parser')
                paper = nber.get_paper(
                    paper_id = nber_id,
                    citation_title = nber.get_citation_item(content, 'citation_title'),
                    citation_author = nber.get_citation_author(content),
                    citation_date = nber.get_citation_item(content, 'citation_date'),
                    citation_publication_date = nber.get_citation_item(content, 'citation_publication_date'),
                    citation_technical_report_institution = nber.get_citation_item(content, 'citation_technical_report_institution'),
                    citation_technical_report_number = nber.get_citation_item(content, 'citation_technical_report_number'),
                    citation_journal_title = nber.get_citation_item(content, 'citation_journal_title'),
                    citation_journal_issn = nber.get_citation_item(content, 'citation_journal_issn'),
                    citation_pdf_url = nber.get_citation_item(content, 'citation_pdf_url'),
                    topics = nber.get_topics(content),
                    abstract = nber.get_abstract(content),
                    also_downloaded = nber.get_also_downloaded(content),
                    acknowledgement = nber.get_acknowledgement(nber_id, headers)
                )
                df = pd.DataFrame([paper])
                data.append(df)
            except Exception:
                sleep(nber.sleep)
                pass
        i += 1
    try:
        df = pd.concat(data, sort=False)
        df = pd.concat([df, existing], sort=False)
        df = df.drop_duplicates(subset=['id'])
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
