#!/bin/bash

# Usage: <turns_file> <annotations_file>
# Where:
#   - <turns_file>
#       JSON list of objects, each of which has a "Conversation_no" and
#       "Turn_no" field with integer values
#   - <annotations_file>
#       Each line: <conversation_no> <turn_no> <addition (one or more)>

turns_file=$1
additions_file=$2

cat $turns_file \
  | jq --indent 4 . \
  | awk 'FILENAME == "'$additions_file'" {
      conversation_no = $1
      turn_no = $2
      addition = $3
      for (f = 4; f <= NF; ++f) {
        addition = addition" "$f
      }
      additions[conversation_no"_"turn_no] = addition
    } FILENAME == "/dev/stdin" { 
      if ($1 == "\"Conversation_no\":") {
        conversation_no = $2
        sub(/,/, "", conversation_no)
      } else if ($1 == "\"Turn_no\":") {
        turn_no = $2
        sub(/,/, "", turn_no)
      } else if ($0 ~ /^    }/) {
        if (conversation_no"_"turn_no in additions) {
          printf ", %s", additions[conversation_no"_"turn_no]
        }
        conversation_no = ""
        turn_no = ""
      }
      print $0
    }' $additions_file /dev/stdin \
  | jq --indent 4 --sort-keys .
