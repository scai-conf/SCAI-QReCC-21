#!/usr/bin/env python3

"""Simple baseline for the SCAI QReCC 21 challenge"""
# Version: 2021-05-14

# Parameters:
# --input=<directory>
#   Directory that contains
#   - passages-index-anserini: Anserini index of the QReCC passage collection.
#   - questions.json:
#     [
#       {
#         "Context": [ "<question1>", "<answer-to-question1>", ... "<questionX-1>", "<answer-to-questionX-1>" ],
#         "Question": "<questionX>",
#         "Conversation_no": <number>,
#         "Turn_no": X,
#       }, ...
#     ]
#
# --output=<directory>
#   Directory to which the run will be written (as run.json). Will be created if it does not exist.
#   - run.json:
#     [
#       {
#         "Model-Rewrite": "<questionX>",
#         "Model-Passages": { 
#           "<id-of-a-relevant-passage>": <score>, ...
#         },
#         "Model-Answer": "<sentence-in-passages-with-highest-term-overlap-with-questionX>",
#         "Conversation_no": <number>,
#         "Turn_no": X,
#       }, ...
#     ]
#
#

import json
from pyserini.search import SimpleSearcher
import getopt
import os
import sys
from textblob import TextBlob
import nltk

# OPTIONS

input_questions_file_name = "questions.json"
input_index_directory_name = "passages-index-anserini"
output_run_file_name = "run.json"

def parse_options():
    options = {
        "num_passages": 100
    }

    try:
        long_options = ["input=", "output="]
        opts, _ = getopt.getopt(sys.argv[1:], "", long_options)
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--input":
            if not os.path.exists(arg):
                sys.exit("The input dataset folder does not exist (%s)." % arg)
            options["input"] = arg

        if opt == "--output":
            if not os.path.exists(arg):
                os.mkdir(arg)
            options["output"] = arg

    if not "input" in options:
        sys.exit("Missing option: --input")
    if not "output" in options:
        sys.exit("Missing option: --output")

    return options

# STEP 1: QUESTION REWRITING

def rewrite(turn):
    if len(turn["Context"]) == 0:
        # Do not rewrite if there is no previous question (copy for your approach)
        return turn["Question"]
    else:
        # This baseline does actually never rewrite (change for your approach)
        return turn["Question"]

# STEP 2: PASSAGE RETRIEVAL

def load_searcher(index_directory):
    searcher = SimpleSearcher(index_directory)
    searcher.set_bm25(0.82, 0.68) # from paper
    return searcher

def retrieve(turn, rewritten_question, searcher, num_passages):
    hits = searcher.search(rewritten_question, k = num_passages)
    return [{"id": hit.docid, "score": hit.score, "text": json.loads(hit.raw)["contents"]} for hit in hits]

# STEP 3: QUESTION ANSWERING

def answer(turn, rewritten_question, retrieved_passages):
    # Take the first of the sentences that contains the most noun phrases of the question
    question_blob = TextBlob(rewritten_question)
    question_phrases = question_blob.noun_phrases.stem()

    best_answer = ""
    best_score = -1
    for passage in retrieved_passages:
        passage_blob = TextBlob(passage["text"])
        for passage_sentence in passage_blob.sentences:
            if passage_sentence.ends_with("."): # simple sentence check: should end in a "."
                passage_sentence_phrases = passage_sentence.noun_phrases.stem()
                score = len([phrase for phrase in passage_sentence_phrases if phrase in question_phrases])
                if score > best_score:
                    best_answer = passage_sentence.raw
                    best_score = score
    return best_answer

# RUN

def run_for_turn(turn, searcher, num_passages):
    rewritten_question = rewrite(turn)
    retrieved_passages = retrieve(turn, rewritten_question, searcher, num_passages)
    retrieved_passages.sort(reverse = True, key = lambda passage: passage["score"])
    question_answer = answer(turn, rewritten_question, retrieved_passages)
    return {
        "Model-Rewrite": rewritten_question,
        "Model-Passages": {passage["id"]: passage["score"] for passage in retrieved_passages},
        "Model-Answer": question_answer,
        "Conversation_no": turn["Conversation_no"],
        "Turn_no": turn["Turn_no"]
    }

def run(turns, searcher, num_passages):
    return [run_for_turn(turn, searcher, num_passages) for turn in turns]

# MAIN

def load_turns(questions_file):
    return json.load(open(questions_file, "r"))

def main(options):
    input_directory = options["input"]
    output_directory = options["output"]
    turns = load_turns(input_directory + "/" + input_questions_file_name)
    searcher = load_searcher(input_directory + "/" + input_index_directory_name)
    nltk.download('brown')
    nltk.download('punkt')
    results = run(turns, searcher, num_passages = options["num_passages"])
    with open(output_directory + "/" + output_run_file_name, "w") as output_file:
        json.dump(results, output_file)

if __name__ == '__main__':
    main(parse_options())

