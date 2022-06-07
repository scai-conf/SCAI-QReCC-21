# SCAI-QReCC-22

[[leaderboards](https://www.tira.io/task/scai-qrecc/)]  [[registration](https://forms.gle/fwfo6fUoHUXdsGGM6)] [[forum](https://www.tira.io/c/scai/)]   [[contact](mailto:scai-qrecc@googlegroups.com)] [[SCAI](https://scai.info/)]

Answer a series of contextually-dependent questions like they may occur in natural human-to-human conversations.

- Submission deadline: July 3, 2022
- Results announcement: July 10, 2022
- Workshop presentations: July 15, 2022


## Data
[[Zenodo](https://doi.org/10.5281/zenodo.4748782)] [[original](https://github.com/apple/ml-qrecc)]

File names here refer to the respective files hosted on [[Zenodo](https://doi.org/10.5281/zenodo.4748782)].

The passage collection (`passages.zip`) is 27.5GB with 54M passages!

The input format for the task (`scai-qrecc21-[toy,training,test]-questions[,-rewritten].json`) is a JSON file:
```
[
  {
    "Conversation_no": <number>,
    "Turn_no": X,
    "Question": "<questionX>"
  }, ...
]
```
With `X` being the number of the question in the conversation. Questions with the same `Conversation_no` are from the same conversation.

The `questions-rewritten.json`-files contain human rewritten questions that can be used by systems that do not want to participate in question rewriting.


## Submission
Register for the task using [this form](https://forms.gle/fwfo6fUoHUXdsGGM6). We will then send you your TIRA login once it is ready.

The challenge is hosted on [TIRA](https://www.tira.io/task/scai-qrecc). Participants can upload their submission as a single JSON file. Alternatively, participants can upload their code and run the evaluation on the VMs provided by the platform to ensure reproducibility of the results.

The submission format for the task is a JSON file similar to the input (all `Model_xxx`-fields are optional and you can omit them from the submission, e.g. provide only Conversation_no, Turn_no and Model_answer to get the EM and F1 scores for the generated answers):
```
[
  {
    "Conversation_no": <number>,
    "Turn_no": X,
    "Model_rewrite": "<your-rewrite-of-questionX>",
    "Model_passages": { 
      "<ID-of-your-first-retrieved-passage-for-questionX>": <score-for-that-passage>, ...
    },
    "Model_answer": "<your-answer-for-questionX>"
  }, ...
]
```
Example: `scai-qrecc21-naacl-baseline.zip`

You can use the [code of our simple baseline](https://github.com/scai-conf/SCAI-QReCC-21/tree/main/code/simple-baseline) to get started.


### Run Submission

You can upload a JSON file as a submission at [https://www.tira.io/task/scai-qrecc](https://www.tira.io/task/scai-qrecc).

Please click on the submit button to enter the upload formular:

![tira-submit](https://user-images.githubusercontent.com/10050886/172434817-60b2f296-440e-4a8d-90e7-613ddd2ba802.png)

Please click on Uploads and select either scai-qrecc22-dataset (if the run uses the original questions) or scai-qrecc22-rewritten-dataset (if the run uses the rewritten questions) as dataset:

![tira-upload](https://user-images.githubusercontent.com/10050886/172435730-f70b4a3b-1a7a-4853-9363-30e18198cd13.png)


After you have uploaded your run, you can [evaluate](#evaluation) your run to verify that your run is valid. At the "Uploads" section, you can click on the blue (i)-icon to double-check your upload. You can also download the run from there.


## Evaluation
[[script](https://github.com/scai-conf/SCAI-QReCC-21/tree/main/code/evaluation-script)]

Once you run your software or uploaded your run, "Run" the evaluator on that run through the TIRA web interface (below the software; works out-of-the-box).

![TIRA Interface: Evaluation](tira/img/tira-software-evaluation.png)

Then go to the "Runs" section below and click on the blue (i)-icon of the evaluator run to see your scores.

### Ground truth
We use the [QReCC paper](https://arxiv.org/abs/2010.04898) annotations in the initial phase, and will update them with alternative answer spans and passages by pooling and crowdsourcing the relevance judgements over the results submitted by the challenge participants (similar to the TREC evaluation setup).

### Metrics
We use the same metrics as the [QReCC paper](https://arxiv.org/abs/2010.04898), but may add more for the final evaluation: ROUGE1-R for question rewriting, Mean Reciprocal Rank (MRR) for passage retrieval, and F1 and Exact Match for question answering.

### Baselines
We provide the following baselines for comparison:
  - **scai-qrecc21-simple-baseline**: BM25 baseline for passage retrieval using original conversational questions without rewriting. We recommend to use [this code](https://github.com/scai-conf/SCAI-QReCC-21/tree/main/code/simple-baseline) as a boilerplate to kickstart your own submission using the VM.
  - **scai-qrecc21-naacl-baseline**: results for the end-to-end approach using supervised question rewriting and QA models reported in the [QReCC paper](https://arxiv.org/abs/2010.04898) (accepted at NAACL'21). This sample run is available [on Zenodo as scai-qrecc21-naacl-baseline.zip](https://doi.org/10.5281/zenodo.4748782).
  
Note that the baseline results differ from the ones reported in the paper since we made several corrections to the evaluation script and the ground truth annotations:

* We excluded the samples for which the ground truth is missing from the evaluation (i.e., no relevant passages or no answer text or no rewrite provided by the human annotators)

* We removed 5,251 passages judgements annotated by the heuristic as relevant for the short answers with lengths <= 5 since these matches are often trivial and unrelated, e.g., the same noun phrase appearing in different contexts.



### Resources
Some useful links to get you started on a new conversational open-domain QA system:

#### Conversational Passage Retrieval

  - [ConvDR](https://github.com/thunlp/ConvDR)
  - [CQE](https://arxiv.org/pdf/2104.08707.pdf)
  - [Chatty Goose](https://github.com/castorini/chatty-goose)

#### Answer Generation

  - [RAG](https://huggingface.co/transformers/model_doc/rag.html)
  - [BART](https://huggingface.co/facebook/bart-large)
  - [ELECTRA](https://huggingface.co/google/electra-large-generator)

#### Passage Retrieval

  - [BEIR](https://github.com/UKPLab/beir)
  - [Haystack](https://colab.research.google.com/github/deepset-ai/haystack/blob/master/tutorials/Tutorial6_Better_Retrieval_via_DPR.ipynb)
  - [BPR](https://github.com/studio-ousia/bpr)
  - [ColBERT](https://github.com/stanford-futuredata/ColBERT)
  - [docTTTTTquery](https://github.com/castorini/docTTTTTquery)

#### Conversational Question Reformulation

  - [QuReTeC](https://github.com/nickvosk/sigir2020-query-resolution)
  - [BART-FC](https://github.com/aquaktus/CAsT_BART_query_rewriting)


# SCAI-QReCC-21
[[leaderboards](https://www.tira.io/task/scai-qrecc/)] [[forum](https://www.tira.io/c/scai/)] [[contact](mailto:scai-qrecc@googlegroups.com)] [[SCAI](https://scai.info/)]

The SCAI-QReCC-21 shared task is over and the results are reported in the [overview paper](https://arxiv.org/abs/2201.11094).

Answer a series of contextually-dependent questions like they may occur in natural human-to-human conversations.

- Submission deadline: <s>September 8, 2021</s> <b>Extended:</b> September 15, 2021
- Results announcement: September 30, 2021
- Workshop presentations: October 8, 2021
