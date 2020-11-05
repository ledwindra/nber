import argparse
import pdftotext
import os
from glob import glob
from time import sleep
from random import randint

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--total', type=int, default=5, help='how many papers that you want to download', metavar='')
args = parser.parse_args()

if not os.path.exists('paper'):
    os.mkdir('paper')

paper = glob('paper/*')
i =  len(paper)
total_download = i + args.total

def get_nber_id(i):
    if i < 10:
        return f'000{i}'
    elif 10 <= i < 100:
        return f'00{i}'
    elif 100 <= i < 1000:
        return f'0{i}'
    else:
        return i

while i < total_download:
    nber_id = get_nber_id(i)
    url = f'https://www.nber.org/system/files/working_papers/w{nber_id}/w{nber_id}.pdf'
    os.system(f'wget {url} -O paper/{nber_id}.pdf')
    with open(f'{nber_id}.pdf', 'rb') as f:
        pdf = pdftotext.PDF(f)
    os.system(f'rm -rf paper/{nber_id}.pdf')
    i += 1
