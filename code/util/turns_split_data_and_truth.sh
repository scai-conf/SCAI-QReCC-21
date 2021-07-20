#!/bin/bash

turns_file=$1
output_dir=$2
mkdir -p $output_dir

cat $turns_file \
  | jq --compact-output --sort-keys '.[]' \
  | gawk 'BEGIN {
      output_questions = "jq --indent 4 --sort-keys --slurp . > '$output_dir'/questions.json"
      output_questions_rewritten = "jq --indent 4 --sort-keys --slurp . > '$output_dir'/questions-rewritten.json"
      output_truth = "jq --indent 4 --sort-keys --slurp . > '$output_dir'/ground-truth.json"
    } function add_question(conversation_no, turn_no, question, output) {
      printf "{\"Conversation_no\":%d,\"Turn_no\":%d,\"Question\":%s}\n", conversation_no, turn_no, question | output
    } function add_truth(conversation_no, turn_no, truth_rewrite, truth_passages, truth_answer) {
      printf "{\"Conversation_no\":%d,\"Turn_no\":%d,\"Truth_rewrite\":%s,\"Truth_passages\":%s,\"Truth_answer\":%s}\n", conversation_no, turn_no, truth_rewrite, truth_passages, truth_answer | output_truth
    } {
      match($0, /.*,"Context":(\[.*\]),"Conversation_no":/, contexts); context = contexts[1]
      match($0, /.*,"Conversation_no":([0-9]*),/, conversation_nos); conversation_no = conversation_nos[1]
      match($0, /.*,"Question":(".*"),"Transformer_rewrite"/, questions); question = questions[1]
      if (question == "") {
        match($0, /.*,"Question":(".*"),"Truth_answer"/, questions); question = questions[1]
      }
      match($0, /.*,"Truth_answer":(".*"),"Truth_passages"/, truth_answers); truth_answer = truth_answers[1]
      match($0, /.*,"Truth_passages":(\[.*\]),"Truth_rewrite":/, truth_passagess); truth_passages = truth_passagess[1]
      match($0, /.*,"Truth_rewrite":(".*"),"Turn_no"/, truth_rewrites); truth_rewrite = truth_rewrites[1]
      match($0, /.*,"Turn_no":([0-9]*)/, turn_nos); turn_no = turn_nos[1]

      add_question(conversation_no, turn_no, question, output_questions)
      add_question(conversation_no, turn_no, truth_rewrite, output_questions_rewritten)
      add_truth(conversation_no, turn_no, truth_rewrite, truth_passages, truth_answer)
    } '

