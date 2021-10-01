#!/bin/bash
  
echo '"Conversation_no","Turn_no","Passage","Lowest_rank"'
for input in $@;do
  cat $input \
    | jq -cr '.[] 
      | {Conversation_no,
         Turn_no,
         Model_passages:(.Model_passages
          |to_entries
          |sort_by(.value)
          |reverse[])
        }
      | [.Conversation_no, .Turn_no, .Model_passages.key]
      | @csv' \
    | awk -F, '{
        if ($1 == lastc && $2 ==lastt) {
          rank = rank+1
        } else {
          rank = 1
        }
        printf "%s,%d\n", $0, rank
        lastc = $1
        lastt = $2
      }'
done \
  | awk -F, '{
      key = $1","$2","$3
      rank = $4
      if (key in ranks) {
        if (ranks[key] > rank) {
          ranks[key] = rank
        }
      } else {
        ranks[key] = rank
      }
    } END {
      for (key in ranks) {
        printf "%s,%d\n", key, ranks[key]
      }
    }'

