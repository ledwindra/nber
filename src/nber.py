import argparse
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from random import uniform
from time import sleep

class HTML:
    '''
    This class returns the HTML page for the corresponding NBER paper.
    '''

    def __init__(self, nber_id):
        self.nber_id = nber_id
    
    def string_id(self):
        '''
        Returns the string format for the NBER ID. For NBER ID above 1000 it will return itself.
        '''
        if self.nber_id < 10:
            return f'000{self.nber_id}'
        elif 10 <= self.nber_id < 100:
            return f'00{self.nber_id}'
        elif 100 <= self.nber_id < 1000:
            return f'0{self.nber_id}'
        else:
            return str(self.nber_id)
    
    def url(self):
        '''
        Returns the URL string for the corresponding NBER paper.
        '''
        return f'https://www.nber.org/papers/w{self.string_id()}'
    
    def request(self):
        '''
        Make a web request for the corresponding NBER paper.
        '''
        return requests.get(self.url())
    
    def content(self):
        '''
        Parse the HTML for the corresponding NBER paper.
        '''
        return BeautifulSoup(self.request().content, features='html.parser')

class Paper:
    '''
    This class processes the HTML text into a tabular DataFrame and save the output to .csv format.
    '''

    def __init__(self, content, nber_id, file_name='data/nber.csv'):
        self.content = content
        self.nber_id = nber_id
        self.file_name = file_name
    
    def to_date(self, x):
        '''
        Returns a date which will be used for several columns.
        '''
        return date(x.year, x.month, x.day)
    
    def citation_title(self):
        '''
        Returns the paper title if any, otherwise returns nothing.
        '''
        try:
            return self.content.find('meta', {'name': 'citation_title'}).attrs['content']
        except AttributeError:
            return None
    
    def citation_author(self):
        '''
        Returns a list of author(s) for the corresponding NBER paper. Can be more than one hence it is stored as a list.
        '''
        try:
            return [x.attrs['content'] for x in self.content.find_all('meta', {'name': 'citation_author'})]
        except AttributeError:
            return None

    def citation_publication_date(self):
        '''
        Returns the publication date if any, otherwise returns nothing.
        '''
        try:
            citation_publication_date = self.content.find('meta', {'name': 'citation_publication_date'})
            citation_publication_date = self.to_date(datetime.strptime(citation_publication_date.attrs['content'], '%Y/%m/%d'))
            return citation_publication_date
        except AttributeError:
            return None
    
    def paper_datetime(self):
        '''
        Returns a timestamp which will consist either issuance date, revision date, or both. Returns nothing if empty.
        '''
        try:
            return [x.attrs['datetime'][:10] for x in self.content.find_all('time')]
        except AttributeError:
            return None
    
    def issue_date(self):
        '''
        Returns the issuance date if any, otherwise returns nothing.
        '''
        try:
            return self.to_date(datetime.strptime(self.paper_datetime()[0], '%Y-%m-%d'))
        except IndexError:
            return None
    
    def revision_date(self):
        '''
        Returns the revision date if any, otherwise returns nothing.
        '''
        try:
            revision_date = self.paper_datetime()[1]
            revision_date = self.to_date(datetime.strptime(revision_date, '%Y-%m-%d'))
            return revision_date
        except IndexError:
            return None

    def related(self):
        '''
        Returns a list of items that relates to the corresponding paper such as topics, programs, and working groups.
        Returns nothing if empty.
        '''
        try:
            return self.content.find_all('div', {'class': 'info-grid__item'})
        except AttributeError:
            return None
    
    def related_title(self):
        '''
        Returns the text that comes from the related method.
        '''
        try:
            return [x.find('h3').text for x in self.related()]
        except AttributeError:
            return None

    def get_related(self, title):
        '''
        Returns a list of either topics, programs, or working groups for the corresponding paper. Returns nothing if empty.
        '''
        try:
            index = self.related_title().index(title)
            item = [x.text for x in self.related()[index].find('div').contents if x.text != '']
            return item
        except ValueError:
            return None
    
    def abstract(self):
        '''
        Returns the abstract if any, otherwise returns nothing.
        '''
        try:
            return self.content.find('div', {'class': 'page-header__intro-inner'}).text
        except AttributeError:
            return None
    
    def acknowledgement(self):
        '''
        Returns the acknowledgement if any, otherwise returns nothing.
        '''
        try:
            return self.content.find('div', {'class': 'accordion__body', 'id': 'accordion-body-guid1'}).text
        except AttributeError:
            return None
        
    def create(self):
        '''
        Returns a dataframe that consists of columns generated by the previous methods.
        '''
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
        '''
        Concatenate existing dataset with the new row. Duplicated rows are dropped. Returns a DataFrame sorted by ID in an ascending order.
        '''
        existing = pd.read_csv(self.file_name)
        df = pd.concat([self.create(), existing], sort=False)
        df = df.drop_duplicates(subset=['id'])

        return df.sort_values(by='id', ascending=True)
    
    def save(self):
        '''
        Save file into .csv format.
        '''
        output = self.file_name
        self.existing().to_csv(output, index=False) if os.path.exists(output) else self.create().to_csv(output, index=False)

class AverageTime:
    '''
    This class calculates the average scraping time per paper.
    '''

    def current_timestamp(self):
        '''
        Returns a timestamp in UTC.
        '''
        return datetime.utcnow()

    def subtract(self, start, end):
        '''
        Subtract the end timestamp with the start timestamp.
        '''
        return (end - start).total_seconds()
    
    def result(self, timestamp):
        '''
        Prints the average scraping time for each paper in second.
        '''
        timestamp = round((sum(timestamp) / len(timestamp)), 3) if timestamp != [] else 0
        print(f'On average, the operation takes {timestamp} second(s).')

def main(start, end, interval, output, existing):
    avg = AverageTime()
    timestamp = []
    while start < end:
        raw = HTML(start)
        _interval = round(uniform(interval, interval+1), 3)
        if start not in existing:
            print(f'[DOWNLOAD \U0001F4BE]: {raw.url()}')
            start_timestamp = avg.current_timestamp()
            content = raw.content()
            paper = Paper(content, raw.nber_id)
            paper.save()
            print(f'[SUCCEED \U00002705]: {raw.url()}.\n[SLEEP \U0001F634]: {_interval} seconds')
            end_timestamp = avg.current_timestamp()
            timestamp.append(avg.subtract(start_timestamp, end_timestamp))
            sleep(_interval)
        else:
            print(f'[IGNORE \U0001F4C1]: {raw.url()}')
        start += 1
    
    return avg.result(timestamp)
        
if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-s', '--start', type=int, default=0, help='Starting NBER ID', metavar='')
    PARSER.add_argument('-e', '--end', type=int, default=5, help='Ending NBER ID', metavar='')
    PARSER.add_argument('-i', '--interval', type=float, default=1, help='Time interval between iteration (in second)', metavar='')
    ARGS = PARSER.parse_args()
    START = ARGS.start
    END = ARGS.end
    INTERVAL = ARGS.interval
    OUTPUT = 'data/nber.csv'
    EXISTING = pd.read_csv(OUTPUT).id.to_list() if os.path.exists(OUTPUT) else []
    main(start=START, end=END, interval=INTERVAL, output=OUTPUT, existing=EXISTING)
