#!/usr/bin/env python3

"""Calculates the measures for the SCAI QReCC 21 challenge"""
# Version: 2021-07-20

# Parameters:
# --input-dataset=<directory>
#   Directory that contains the ground-truth.json:
#   [
#     {
#       "Conversation_no": <number>,
#       "Turn_no": <number>,
#       "Truth_rewrite": "<rewrite-of-question>",
#       "Truth_passages": [ "<id-of-a-relevant-passage>", ... ],
#       "Truth_answer": "<answer-to-question>"
#     }, ...
#   ]
#
# --input-run=<directory>
#   Directory that contains the run.json:
#   [
#     {
#       "Conversation_no": <number>,
#       "Turn_no": <number>,
#       "Model_rewrite": "<rewrite-of-question>",
#       "Model_passages": { 
#         "<id-of-a-relevant-passage>": <score>, ...
#       },
#       "Model_answer": "<answer-to-question>"
#     }, ...
#   ]
#
# --output=<directory>
#   Directory to which the evaluation will be written. Will be created if it does not exist.
#
# --eval-missing-truth
#   Also evaluate turns with missing ground truth (i.e., no relevant passages, no answer) like in the paper.
#
# --eval-turn-one-rewrites
#   Also evaluate question rewrites for first turns of a conversations.
#
# --no-rewriting
#   Do no evaluate query rewriting, even if Model_rewrite fields exist in the run files.
#
# --no-retrieval
#   Do no evaluate passage retrieval, even if Model_passages fields exist in the run files.
#
# --no-answering
#   Do no evaluate question answering, even if Model_answer fields exist in the run files.
#
#

from datasets import load_metric
from tqdm import tqdm
import getopt
import json
import os
import pytrec_eval
import sys

# OPTIONS

input_dataset_file_name = "ground-truth.json"
input_run_file_name = "run.json"
output_file_name = "evaluation.prototext"
question_types_all = ["model", "original", "transformer", "human"]
question_types_no_model = ["original", "transformer", "human"]
question_types_model_only = ["model"]

def parse_options():
    options = {
        "digits": 3,
        "eval-missing-truth": False,
        "eval-turn-one-rewrites": False,
        "rewriting": True,
        "retrieval": True,
        "answering": True
    }

    try:
        long_options = ["input-dataset=", "input-run=", "output=", "eval-missing-truth", "eval-turn-one-rewrites", "no-rewriting", "no-retrieval", "no-answering"]
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

        if opt == "--eval-missing-truth":
            options["eval-missing-truth"] = True

        if opt == "--eval-turn-one-rewrites":
            options["eval-turn-one-rewrites"] = True

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
        if "Model_rewrite" in turn:
            rewrite = turn["Model_rewrite"]
            if rewrite != None:
                turn_id = get_turn_id(turn)
                rewriting_run[turn_id] = rewrite
    return rewriting_run

def evaluate_rewriting(ground_truth, run, eval_missing_truth, eval_turn_one_rewrites):
    print("Evaluate: Query Rewriting")

    rewriting_run = get_rewriting_run(run)
    if not rewriting_run: # no rewrite => do not evaluate
        print("  skipped for no rewrites")
        return {}

    metric = load_metric("rouge")
    rewrites = 0
    for turn in tqdm(ground_truth):
        if eval_turn_one_rewrites or turn["Turn_no"] > 1:
            if eval_missing_truth or turn["Truth_rewrite"] != "":
                turn_id = get_turn_id(turn)
                reference = turn["Truth_rewrite"]
                prediction = ""
                if turn_id in rewriting_run:
                    prediction = rewriting_run[turn_id]
                metric.add(prediction = prediction, reference = reference)
                rewrites = rewrites + 1

    if rewrites > 0:
        score = metric.compute()
        print("  used %d rewrites" % rewrites)
        return { "ROUGE1-R": score['rouge1'].mid.recall }
    else:
        print("  skipped for no rewrites")
        return { }

# STEP 2: PASSAGE RETRIEVAL

def get_retrieval_run(run):
    retrieval_run = {}
    for turn in run:
        turn_id = get_turn_id(turn)
        if "Model_passages" in turn:
            if "" in turn["Model_passages"]:
                sys.exit("Invalid passage ID: '' for turn %s" % turn_id)
            retrieval_run[turn_id] = turn["Model_passages"]
    return retrieval_run

def get_retrieval_ground_truth(ground_truth, eval_missing_truth):
    retrieval_ground_truth = {}
    for turn in ground_truth:
        turn_id = get_turn_id(turn)
        if "Truth_passages" in turn and len(turn["Truth_passages"]) > 0:
            retrieval_ground_truth[turn_id] = {passage:1 for passage in turn["Truth_passages"]}
        elif eval_missing_truth: # paper version
            retrieval_ground_truth[turn_id] = {"":1}
    return retrieval_ground_truth

def evaluate_retrieval(ground_truth, run, eval_missing_truth):
    print("Evaluate: Passage Retrieval")
    result = {}
    retrieval_run = get_retrieval_run(run)
    retrieval_ground_truth_for_type = get_retrieval_ground_truth(ground_truth, eval_missing_truth)
    retrieval_run_for_type = {turn_id:passages for (turn_id, passages) in retrieval_run.items() if turn_id in retrieval_ground_truth_for_type}
    if retrieval_run_for_type: # at least one turn for this type => evaluate
        metric = pytrec_eval.RelevanceEvaluator(retrieval_ground_truth_for_type, {'recip_rank'})
        mrrs = [score["recip_rank"] for score in metric.evaluate(retrieval_run_for_type).values()]
        average_mrr = sum(mrrs) / len(mrrs)
        result["MRR"] = average_mrr
        print("    used retrieved passages for %d questions" % len(retrieval_run_for_type))
    else:
        print("    skipped for no retrieved passages")
    return result

# STEP 3: QUESTION ANSWERING

def get_answering_run(run):
    answering_run = {}
    for turn in run:
        turn_id = get_turn_id(turn)
        if "Model_answer" in turn:
            answer = turn["Model_answer"]
            if answer != None:
                answering_run[turn_id] = answer
    return answering_run

def evaluate_answering(ground_truth, run, eval_missing_truth):
    print("Evaluate: Question Answering")
    result = {}
    answering_run = get_answering_run(run)
    metric = load_metric("squad_v2")
    answers = 0
    for turn in tqdm(ground_truth, desc = "  "):
        turn_id = get_turn_id(turn)
        if eval_missing_truth or turn["Truth_answer"] != "":
            reference = {
                    "id": turn_id,
                    "answers": {'answer_start': [0], 'text': [turn["Truth_answer"]]}
                }
            prediction = {
                    "id": turn_id,
                    "prediction_text": "",
                    'no_answer_probability': 0.
                }
            if turn_id in answering_run:
                prediction["prediction_text"] = answering_run[turn_id]
                answers = answers + 1
            metric.add(prediction = prediction, reference = reference)
    if answers > 0:
        score = metric.compute()
        result["Exact match"] = score['exact'] / 100
        result["F1"] = score['f1'] / 100
        print("    used %d answers" % answers)
    else:
        print("    skipped for no answers")
    return result

# EVALUATE

def has_model_rewrites(run):
    for turn in run:
        if "Model_rewrite" in turn:
            return True
    return False

def evaluate(ground_truth, run, eval_missing_truth = False, eval_turn_one_rewrites = False, rewriting = True, retrieval = True, answering = True):
    results = {}
    if rewriting:
        results.update(evaluate_rewriting(ground_truth, run, eval_missing_truth, eval_turn_one_rewrites))
    if retrieval:
        results.update(evaluate_retrieval(ground_truth, run, eval_missing_truth))
    if answering:
        results.update(evaluate_answering(ground_truth, run, eval_missing_truth))
    return results

# MAIN

def sprint_results(results, digits):
    value_format = "%0." + str(digits) + "f"
    measure_strings = [ "measure{\n  key: \"%s\"\n  value: \"%s\"\n}" % (name, value_format % value) for (name, value) in results.items()]
    return "\n".join(measure_strings)

def main(options):
    results = evaluate(
            ground_truth = options["ground-truth"],
            run = options["run"],
            eval_missing_truth = options["eval-missing-truth"],
            eval_turn_one_rewrites = options["eval-turn-one-rewrites"],
            rewriting = options["rewriting"],
            retrieval = options["retrieval"],
            answering = options["answering"])
    results_string = sprint_results(results, options["digits"])
    print(results_string)
    with open(options["output-file-name"], "w") as output_file:
        output_file.write(results_string)

if __name__ == '__main__':
    main(parse_options())

