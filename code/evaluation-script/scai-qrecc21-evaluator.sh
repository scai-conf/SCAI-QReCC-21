#!/bin/bash

# Parameters:
# $1
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
# $2
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
# $3
#   Directory to which the evaluation will be written. Will be created if it does not exist.
#

ground_truth_directory=$1
run_directory=$2
output_directory=$3
shift 3
other_params=$@

ground_truth=$ground_truth_directory/ground-truth.json
run=$run_directory/run.json
mkdir -p $output_directory

tmp=/var/tmp/scai-qrecc21-evaluator-$$

function reformat_kpqa_run() {
  cat $1 \
    | jq -c '.[] 
      | {((.Conversation_no|tostring) + "-" + (.Turn_no|tostring)) : {"Model_answer":.Model_answer}}' \
    | jq -s add
}

function reformat_kpqa_truth() {
  cat $1 \
    | jq -c '.[] 
      | {((.Conversation_no|tostring) + "-" + (.Turn_no|tostring)) : {"Truth_rewrite":.Truth_rewrite, "Truth_answer":.Truth_answer}}' \
    | jq -s add
}

mkdir -p $tmp
reformat_kpqa_run $run > $tmp/kpqa-run.json
reformat_kpqa_truth $ground_truth > $tmp/kpqa-truth.json
echo "question,answer,reference1" > $tmp/kpqa.csv
jq -s '.[0] * .[1]' $tmp/kpqa-run.json $tmp/kpqa-truth.json \
  | jq -cr '.[] 
    | [.Truth_rewrite, .Model_answer, .Truth_answer] 
    | @csv' \
  >> $tmp/kpqa.csv
python3 $(dirname $0)/KPQA/compute_KPQA.py --data $tmp/kpqa.csv --model_path $(dirname $0)/KPQA/ckpt --out_file $tmp/kpqa-result.csv --num_ref 1
# rm -rf $tmp

