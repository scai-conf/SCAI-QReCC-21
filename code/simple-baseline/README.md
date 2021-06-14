# SCAI-QReCC-21 SIMPLE BASELINE

This baseline mostly serves to kickstart your own submission (see below). It does the following:
  - Question rewriting: Return the question as-is
  - Passage retrieval: BM25 with k1 = 0.82 and b = 0.68 as in the [paper](https://arxiv.org/abs/2010.04898)
  - Question answering: Use the sentence from the retrieved passages that contains the most of the stemmed noun phrases of the question (the first one if a draw)

To adapt this for your own submission:
  - Question rewriting
    - If you have no own approach to rewriting, remove `Model-rewrite` from the `result` dict of the `run_for_turn` method
    - Otherwise replace the `else`-branch of `rewrite(turn)` with your approach
  - Passage retrieval
    - Replace the `load_searcher` and/or `retrieve` methods with your approach (if it also uses Anserini)
    - If your approach uses a different index, tell us organizers: we can put it next to the Anserini one
  - Question answering
    - Replace the `answer` method with your approach

## Installation in TIRA
```
sudo apt update
sudo apt install python3-pip openjdk-11-jdk-headless # java needed for anserini
git clone https://github.com/scai-conf/SCAI-QReCC-21.git
pip3 install -r SCAI-QReCC-21/code/simple-baseline/requirements.txt
```
