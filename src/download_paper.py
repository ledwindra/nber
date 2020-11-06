import argparse
import os
from time import sleep
from random import randint

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--start', type=int, default=0, help='Start ID (default 0)', metavar='')
parser.add_argument('-e', '--end', type=int, default=5, help='End ID (default 5)', metavar='')
parser.add_argument('-w', '--whole', type=str, choices=['true', 'false'], default='false', help='Download all paper? (default false)', metavar='')
args = parser.parse_args()

if not os.path.exists('paper'):
    os.mkdir('paper')

def get_nber_id(i):
    if i < 10:
        return f'000{i}'
    elif 10 <= i < 100:
        return f'00{i}'
    elif 100 <= i < 1000:
        return f'0{i}'
    else:
        return i

if args.whole == 'true':
    total_download = len(os.listdir('paper/'))
else:
    total_download = args.end

while args.start < total_download:
    nber_id = get_nber_id(args.start)
    url = f'https://www.nber.org/system/files/working_papers/w{nber_id}/w{nber_id}.pdf'
    os.system(f'wget {url} -O paper/{nber_id}.pdf')
    os.system(f'pdftotext paper/{nber_id}.pdf paper/{nber_id}.txt')
    os.system(f'rm -rf paper/{nber_id}.pdf')
    args.start += 1
