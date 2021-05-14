#!/usr/bin/env python3

"""Calculates the measures for the SCAI QReCC 21 challenge"""
# Version: 2021-05-13

# Parameters:
# --input-dataset=<directory>
#   Directory that contains the ground-truth.json:
#   [
#     {
#       "Rewrite": "<rewrite-of-question>",
#       "Passages": [ "<id-of-a-relevant-passage>", ... ],
#       "Answer": "<answer-to-question>",
#       "Conversation_no": <number>,
#       "Turn_no": <number>,
#     }, ...
#   ]
#
# --input-run=<directory>
#   Directory that contains the output one run.json:
#   [
#     {
#       "Model-Rewrite": "<rewrite-of-question>",
#       "Model-Passages": { 
#         "<id-of-a-relevant-passage>": <score>, ...
#       },
#       "Model-Answer": "<answer-to-question>",
#       "Conversation_no": <number>,
#       "Turn_no": <number>,
#     }, ...
#   ]
#
# --output=<directory>
#   Directory to which the evaluation will be written. Will be created if it does not exist.
#
# --invalid-turns
#   Skip turns with invalid ground truth (i.e., no relevant passages, no answer) like in the paper.
#
# --no-rewriting
#   Do no evaluate query rewriting, even if Model-Rewrite fields exist in the run files.
#
# --no-retrieval
#   Do no evaluate passage retrieval, even if Model-Passages fields exist in the run files.
#
# --no-answering
#   Do no evaluate question answering, even if Model-Answer fields exist in the run files.
#
#

import json
from datasets import load_metric
import pytrec_eval
import sys
import getopt
import os

# OPTIONS

input_dataset_file_name = "ground-truth.json"
input_run_file_name = "run.json"
output_file_name = "evaluation.prototext"

def parse_options():
    options = {
        "invalid-turns": False,
        "rewriting": True,
        "retrieval": True,
        "answering": True
    }

    try:
        long_options = ["input-dataset=", "input-run=", "output=", "invalid-turns", "no-rewriting", "no-retrieval", "no-answering"]
        opts, _ = getopt.getopt(sys.argv[1:], "", long_options)
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--input-dataset":
            if not os.path.exists(arg):
                sys.exit("The input dataset folder does not exist (%s)." % arg)
            options["ground-truth"] = load_ground_truth(arg + "/" + input_dataset_file_name)

        if opt == "--input-run":
            if not os.path.exists(arg):
                sys.exit("The input run folder does not exist (%s)." % arg)
            options["run"] = load_run(arg + "/" + input_run_file_name)

        if opt == "--output":
            if not os.path.exists(arg):
                os.mkdir(arg)
            options["output-file-name"] = arg + "/" + output_file_name

        if opt == "--invalid-turns":
            options["invalid-turns"] = True

        if opt == "--no-rewriting":
            options["rewriting"] = False

        if opt == "--no-retrieval":
            options["retrieval"] = False

        if opt == "--no-answering":
            options["answering"] = False

    if not "ground-truth" in options:
        sys.exit("Missing option: --input-dataset")
    if not "run" in options:
        sys.exit("Missing option: --input-run")
    if not "output-file-name" in options:
        sys.exit("Missing option: --output")

    return options

def load_ground_truth(input_dataset_file):
    return json.load(open(input_dataset_file, "r"))

def load_run(input_run_file):
    return json.load(open(input_run_file, "r"))

# UTILITY

def get_turn_id(turn):
    return "%d_%d" % (turn["Conversation_no"], turn["Turn_no"])

# STEP 1: QUESTION REWRITING

def get_rewriting_run(run):
    rewriting_run = {}
    for turn in run:
        turn_id = get_turn_id(turn)
        if "Model-Rewrite" in turn:
            rewrite = turn["Model-Rewrite"]
            if rewrite != None:
                rewriting_run[turn_id] = rewrite
    return rewriting_run

def evaluate_rewriting(ground_truth, run, invalid_turns):
    rewriting_run = get_rewriting_run(run)
    if not rewriting_run: # no rewrite => do not evaluate
        return {}

    metric = load_metric("rouge")

    for turn in ground_truth:
        turn_id = get_turn_id(turn)
        reference = turn["Rewrite"]
        prediction = ""
        if turn_id in rewriting_run:
            prediction = rewriting_run[turn_id]
        metric.add(prediction = prediction, reference = reference)

    score = metric.compute()
    return { "qr-rouge1r": score['rouge1'].mid.recall }

# STEP 2: PASSAGE RETRIEVAL

def get_retrieval_run(run):
    retrieval_run = {}
    for turn in run:
        turn_id = get_turn_id(turn)
        if "Model-Passages" in turn:
            if "" in turn["Model-Passages"]:
                sys.exit("Invalid passage ID: '' for turn %s" % turn_id)
            retrieval_run[turn_id] = turn["Model-Passages"]
    return retrieval_run

def get_retrieval_ground_truth(ground_truth, invalid_turns):
    retrieval_ground_truth = {}
    for turn in ground_truth:
        turn_id = get_turn_id(turn)
        if "Passages" in turn and len(turn["Passages"]) > 0:
            retrieval_ground_truth[turn_id] = {passage:1 for passage in turn["Passages"]}
        elif invalid_turns: # paper version
            retrieval_ground_truth[turn_id] = {"":1}
    return retrieval_ground_truth

def evaluate_retrieval(ground_truth, run, invalid_turns):
    retrieval_run = get_retrieval_run(run)
    if not retrieval_run: # no retrieval done => do not evaluate
        return {}

    retrieval_ground_truth = get_retrieval_ground_truth(ground_truth, invalid_turns)
    if not invalid_turns:
        retrieval_run = {turn_id:passages for (turn_id,passages) in retrieval_run.items() if turn_id in retrieval_ground_truth}

    metric = pytrec_eval.RelevanceEvaluator(retrieval_ground_truth, {'recip_rank'})
    mrrs = [score["recip_rank"] for score in metric.evaluate(retrieval_run).values()]
    average_mrr = sum(mrrs) / len(mrrs)
    return { "pr-mrr": average_mrr }

# STEP 3: QUESTION ANSWERING

def get_answering_run(run):
    answering_run = {}
    for turn in run:
        turn_id = get_turn_id(turn)
        if "Model-Answer" in turn:
            answer = turn["Model-Answer"]
            if answer != None:
                answering_run[turn_id] = answer
    return answering_run

def evaluate_answering(ground_truth, run, invalid_turns):
    answering_run = get_answering_run(run)
    if not answering_run: # no answer => do not evaluate
        return {}

    metric = load_metric("squad_v2")

    for turn in ground_truth:
        turn_id = get_turn_id(turn)
        if invalid_turns or turn["Answer"] != "": # skip turns with no answer: deviation from paper!
            reference = {
                    "id": turn_id,
                    "answers": {'answer_start': [0], 'text': [turn["Answer"]]}
                }
            prediction = {
                    "id": turn_id,
                    "prediction_text": "",
                    'no_answer_probability': 0.
                }
            if turn_id in answering_run:
                prediction["prediction_text"] = answering_run[turn_id]
            metric.add(prediction = prediction, reference = reference)

    score = metric.compute()
    return { "qa-em": score['exact'], "qa-f1": score['f1'] }

# EVALUATE

def evaluate(ground_truth, run, invalid_turns = False, rewriting = True, retrieval = True, answering = True):
    results = {}
    if rewriting:
        results.update(evaluate_rewriting(ground_truth, run, invalid_turns))
    if retrieval:
        results.update(evaluate_retrieval(ground_truth, run, invalid_turns))
    if answering:
        results.update(evaluate_answering(ground_truth, run, invalid_turns))
    return results

# MAIN

def sprint_results(results):
    measure_strings = [ "measure{\n  key: \"%s\"\n  value: \"%s\"\n}" % (name, value) for (name, value) in results.items()]
    return "\n".join(measure_strings)

def main(options):
    results = evaluate(
            ground_truth = options["ground-truth"],
            run = options["run"],
            invalid_turns = options["invalid-turns"],
            rewriting = options["rewriting"],
            retrieval = options["retrieval"],
            answering = options["answering"])
    results_string = sprint_results(results)
    print(results_string)
    with open(options["output-file-name"], "w") as output_file:
        output_file.write(results_string)

if __name__ == '__main__':
    main(parse_options())

