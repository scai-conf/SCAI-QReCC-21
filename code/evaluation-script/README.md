## Requirements

```
pip3 install -r requirements.txt 
python3 -m spacy download en_core_web_sm
```

## Test

Download ground-truth.json from Zenodo + the run file, e.g., gpt3.json (rename to "run.json")

```
python scai-qrecc21-evaluator.py --input-dataset <dir-with-ground-truth.json> --input-run <dir-with-run.json> --output .
```

## Docker
```
sudo docker build -t registry.webis.de/code-lib/public-images/scai-qrecc21-evaluator:1.0.1 .
sudo docker push registry.webis.de/code-lib/public-images/scai-qrecc21-evaluator:1.0.1
```
