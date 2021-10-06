import redis
import csv
import ast
import sys
from tqdm import tqdm

r = redis.Redis(host='localhost', port='6379', db='0')

def toutf8(text):
    try:
        return text.decode('utf-8')
    except AttributeError:
        return text

writer = csv.writer(sys.stdout)
for i in range(1, len(sys.argv)):
    with open(sys.argv[i], 'r') as tsv_file:
        tsv_lines = csv.reader(tsv_file, delimiter="\t")
        for tsv_line in tqdm(tsv_lines):
            passage_urls = ast.literal_eval(tsv_line[3])
            passages = [toutf8(r.get(passage_url)) for passage_url in passage_urls]
            writer.writerow([tsv_line[0], tsv_line[1], tsv_line[2], passages])
