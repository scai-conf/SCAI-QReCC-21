# SCAI-QReCC-21
[[task page](https://scai.info/scai-qrecc/)] [[tira](https://www.tira.io/task/scai-qrecc/dataset/scai-qrecc21-test-dataset-2021-05-15)]

Answer a series of contextually-dependent questions like they may occur in natural human-to-human conversations.

## Data
[[questions](https://zenodo.org/record/4772532/files/scai-qrecc21-questions.json?download=1)] [[passage collection](https://zenodo.org/record/4772532/files/passages.zip?download=1)] [[entire dataset](https://doi.org/10.5281/zenodo.4748782)]

The input format for the task (questions) is a JSON file:
```
[
  {
    "Conversation_no": <number>,
    "Turn_no": X,
    "Context": [ "<question1>", "<answer-to-question1>", ... "<questionX-1>", "<answer-to-questionX-1>" ],
    "Question": "<questionX>"
  }, ...
]
```
With `X` being the number of the question in the conversation. Questions with the same `Conversation_no` are from the same conversation.

Upon request, we will provide question files and submission possibilities for systems that address not all three steps.


## Submission
Register for the task using [this form](https://docs.google.com/forms/d/e/1FAIpQLSem7NXwDSgv2SLJrXhuHPxGifOOyzqewcu41hTIV3ywqRcr_A/viewform?usp=sf_link). We will then send you your TIRA login once it is ready.

The challenge is hosted on [TIRA](https://www.tira.io/task/scai-qrecc/dataset/scai-qrecc21-test-dataset-2021-05-15). Participants are encouraged to upload their code and run the evaluation on the VMs provided by the platform to ensure reproducibility of the results. It is also possible to upload the submission as a single JSON file.

The submission format for the task is a JSON file similar to the input:
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
Example: [NAACL baseline](https://zenodo.org/record/4772532/files/scai-qrecc21-naacl-baseline.zip?download=1)

All `Model_xxx`-fields are optional: omit them if your system does not address the respective step.

You can use the [code of our simple baseline](https://github.com/scai-conf/SCAI-QReCC-21/tree/main/code/simple-baseline) to get started.

### Software Submission
Coming soon

### Run Submission
Coming soon


## Evaluation
[[evaluation script](https://github.com/scai-conf/SCAI-QReCC-21/tree/main/code/evaluation-script)]

The evaluation is performed on the test split of the QReCC dataset. We use the ground truth annotations in the initial phase, and will update them with alternative answer spans and passages by pooling and crowdsourcing the relevance judgements over the results submitted by the challenge participants (similar to the TREC evaluation setup).

We use the same metrics as the [QReCC paper](https://arxiv.org/abs/2010.04898), but may add more for the final evaluation: ROUGE1-R for question rewriting, Mean Reciprocal Rank (MRR) for passage retrieval, and F1 and Exact Match for question answering.

