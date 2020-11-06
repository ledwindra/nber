import argparse
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
from random import randint

class ID:
    def __init__(self):
        self.nber_id = randint(0, len(os.listdir('paper/')))

class HTML(ID):
    
    def string_id(self):
        if self.nber_id < 10:
            return f'000{self.nber_id}'
        elif 10 <= self.nber_id < 100:
            return f'00{self.nber_id}'
        elif 100 <= self.nber_id < 1000:
            return f'0{self.nber_id}'
        else:
            return str(self.nber_id)
    
    def url(self):
        return f'https://www.nber.org/papers/w{self.nber_id}'
    
    def request(self):
        return requests.get(self.url())
    
    def content(self):
        return BeautifulSoup(self.request().content, features='html.parser')

class Paper:
    def __init__(self, content, nber_id, file_name='data/nber.csv'):
        self.content = content
        self.nber_id = nber_id
        self.file_name = file_name
    
    def to_date(self, x):
        return date(x.year, x.month, x.day)
    
    def citation_title(self):
        return self.content.find('meta', {'name': 'citation_title'}).attrs['content']
    
    def citation_author(self):
        return [x.attrs['content'] for x in self.content.find_all('meta', {'name': 'citation_author'})]

    def citation_publication_date(self):
        citation_publication_date = self.content.find('meta', {'name': 'citation_publication_date'})
        citation_publication_date = self.to_date(datetime.strptime(citation_publication_date.attrs['content'], '%Y/%m/%d'))
        
        return citation_publication_date
    
    def paper_datetime(self):
        return [x.attrs['datetime'][:10] for x in self.content.find_all('time')]
    
    def issue_date(self):
        return self.to_date(datetime.strptime(self.paper_datetime()[0], '%Y-%m-%d'))
    
    def revision_date(self):
        try:
            revision_date = self.paper_datetime()[1]
            revision_date = self.to_date(datetime.strptime(revision_date, '%Y-%m-%d'))
            return revision_date
        except IndexError:
            return None

    def related(self):
        return self.content.find_all('div', {'class': 'info-grid__item'})
    
    def related_title(self):
        return [x.find('h3').text for x in self.related()]

    def get_related(self, title):
        try:
            index = self.related_title().index(title)
            item = [x.text for x in self.related()[index].find('div').contents if x.text != '']
            return item
        except ValueError:
            return None
    
    def abstract(self):
        return self.content.find('div', {'class': 'page-header__intro-inner'}).text
    
    def acknowledgement(self):
        return self.content.find('div', {'class': 'accordion__body', 'id': 'accordion-body-guid1'}).text
        
    def create(self):
        return pd.DataFrame([{
            'id': self.nber_id,
            'citation_title': self.citation_title(),
            'citation_author': self.citation_author(),
            'citation_publication_date': self.citation_publication_date(),
            'issue_date': self.issue_date(),
            'revision_date': self.revision_date(),
            'topics': self.get_related('Topics'),
            'program': self.get_related('Programs'),
            'projects': self.get_related('Projects'),
            'working_groups': self.get_related('Working Groups'),
            'abstract': self.abstract(),
            'acknowledgement': self.acknowledgement()
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
        raw = HTML()
        content = raw.content()
        paper = Paper(content, raw.nber_id)
        paper.save()
        i += 1
