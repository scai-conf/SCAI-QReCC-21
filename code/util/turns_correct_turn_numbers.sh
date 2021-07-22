#!/bin/bash

# Usage: <turns_file>
# Where:
#   - <turns_file>
#       JSON list of objects, each of which has a "Conversation_no" and
#       "Turn_no" field with integer values

turns_file=$1
cat $turns_file \
  | awk '{
      if ($1 == "\"Conversation_no\":") {
      old_conversation_no = conversation_no
      conversation_no = sprintf("%d", $2)
      }

      if ($1 == "\"Turn_no\":") {
        if (conversation_no == old_conversation_no) {
          turn_no = turn_no + 1
        } else {
          turn_no = 1
        }
        $2 = sprintf("%d", turn_no)
      }
      print $0
    }' \
  | jq '.'
