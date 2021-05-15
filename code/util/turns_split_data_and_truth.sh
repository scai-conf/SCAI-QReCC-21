#!/bin/bash

turns_file=$1
output_dir=$2
mkdir -p $output_dir

max_conversation_no=$(cat $turns_file | jq '.[].Conversation_no' | awk '$1>max{max=$1}END{print max}')
echo "Max Conversation_no: $max_conversation_no"
cat $turns_file \
  | jq --compact-output --sort-keys '.[]' \
  | gawk 'BEGIN {
      output_question = "jq --indent 4 --sort-keys --slurp . > '$output_dir'/questions.json"
      output_truth = "jq --indent 4 --sort-keys --slurp . > '$output_dir'/ground-truth.json"
      next_conversation_no = '$max_conversation_no' + 1
    } function add_question(conversation_no, turn_no, context, question) {
      printf "{\"Conversation_no\":%d,\"Turn_no\":%d,\"Context\":%s,\"Question\":%s}\n", conversation_no, turn_no, context, question | output_question
    } function add_truth(model_conversation_no, model_turn_no, original_conversation_no, transformer_conversation_no, human_conversation_no, truth_rewrite, truth_passages, truth_answer) {
      printf "{\"Turns\":{\"model\":{\"Conversation_no\":%d,\"Turn_no\":%d},\"original\":{\"Conversation_no\":%d,\"Turn_no\":1},\"transformer\":{\"Conversation_no\":%d,\"Turn_no\":1},\"human\":{\"Conversation_no\":%d,\"Turn_no\":1}},\"Truth_rewrite\":%s,\"Truth_passages\":%s,\"Truth_answer\":%s}\n", model_conversation_no, model_turn_no, original_conversation_no, transformer_conversation_no, human_conversation_no, truth_rewrite, truth_passages, truth_answer | output_truth
    } {
      match($0, /.*,"Context":(\[.*\]),"Conversation_no":/, contexts); context = contexts[1]
      match($0, /.*,"Conversation_no":([0-9]*),/, conversation_nos); conversation_no = conversation_nos[1]
      match($0, /.*,"Question":(".*"),"Transformer_rewrite"/, questions); question = questions[1]
      if (question == "") {
        match($0, /.*,"Question":(".*"),"Truth_answer"/, questions); question = questions[1]
        transformer_rewrite = question
      } else {
        match($0, /.*,"Transformer_rewrite":(".*"),"Truth_answer"/, transformer_rewrites); transformer_rewrite = transformer_rewrites[1]
      }
      match($0, /.*,"Truth_answer":(".*"),"Truth_passages"/, truth_answers); truth_answer = truth_answers[1]
      match($0, /.*,"Truth_passages":(\[.*\]),"Truth_rewrite":/, truth_passagess); truth_passages = truth_passagess[1]
      match($0, /.*,"Truth_rewrite":(".*"),"Turn_no"/, truth_rewrites); truth_rewrite = truth_rewrites[1]
      match($0, /.*,"Turn_no":([0-9]*)/, turn_nos); turn_no = turn_nos[1]

      add_question(conversation_no, turn_no, context, question)
      if (turn_no == 1) {
        add_truth(conversation_no, turn_no, conversation_no, conversation_no, conversation_no, truth_rewrite, truth_passages, truth_answer)
      } else {
        original_conversation_no = next_conversation_no++
        add_question(original_conversation_no, 1, "[]", question)

        transformer_conversation_no = original_conversation_no
        if (transformer_rewrite != question) {
          transformer_conversation_no = next_conversation_no++
          add_question(transformer_conversation_no, 1, "[]", transformer_rewrite)
        }

        human_conversation_no = original_conversation_no
        if (truth_rewrite != question) {
          if (truth_rewrite != transformer_rewrite) {
            human_conversation_no = next_conversation_no++
            add_question(human_conversation_no, 1, "[]", truth_rewrite)
          } else {
            human_conversation_no = transformer_conversation_no
          }
        }

        add_truth(conversation_no, turn_no, original_conversation_no, transformer_conversation_no, human_conversation_no, truth_rewrite, truth_passages, truth_answer)
      }
    } '

