## Requirements

```
pip install -r requirements.txt 
```

## Test

Download ground-truth.json from Zenodo + the run file, e.g., gpt3.json (rename to "run.json")

```
python scai-qrecc21-evaluator.py --input-dataset <dir-with-ground-truth.json> --input-run <dir-with-run.json> --output .
```
