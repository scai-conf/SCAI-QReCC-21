import csv
import sys
import ast
from tqdm import tqdm
import re

csv.field_size_limit(sys.maxsize)

selected = set()
with open(sys.argv[1], 'r') as selection_file:
    records = csv.reader(selection_file)
    for record in tqdm(records):
        key = record[0] + "," + record[1]
        selected.add(key)

passage_ids = {};
with open(sys.argv[2], 'r') as passage_ids_file:
    records = csv.reader(passage_ids_file, delimiter="\t")
    for record in tqdm(records):
        key = record[0] + "," + record[1]
        passage_ids[key] = record[3]

def accumu(lis):
    total = 0
    for x in lis:
        total += len(x)
        yield total

def cumsumlength(lis):
    return list(accumu(lis))

def cutoff(lis):
    cumsum = cumsumlength(lis)
    for i in range(len(lis)):
        if cumsum[i] > 20000:
            if i == 0:
                return 0
            else:
                return i - 1
    return len(lis)

def toutf8(text):
    try:
        return text.decode('utf-8')
    except AttributeError:
        return text

print("conversation_no,turn_no,question,passage_ids,passages")
writer = csv.writer(sys.stdout, lineterminator="\n")
with open(sys.argv[3], 'r') as all_file:
    records = csv.reader(all_file)
    for record in tqdm(records):
        key = record[0] + "," + record[1]
        if key in selected:
            ids = toutf8(ast.literal_eval(passage_ids[key]))
            passages = toutf8(ast.literal_eval(re.sub(r"<[a-z/][^>]*>", "", record[3])))
            while len(ids) > 0:
                split = cutoff(passages) + 1
                cids = ids[:split]
                cpassages = passages[:split]
                writer.writerow([record[0], record[1], record[2], cids, cpassages])
                ids = ids[split:]
                passages = passages[split:]

