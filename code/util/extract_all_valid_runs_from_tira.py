#!/usr/bin/env python3

# Manually collected
VALID_RUNS = {
    'scai-qrecc21-test-dataset-2021-07-20': {
        'rachael': ['2021-09-15-09-06-44', '2021-09-15-09-05-06', '2021-09-08-21-49-44', '2021-09-08-07-07-57', '2021-09-15-09-08-40', '2021-09-08-15-40-34', '2021-09-08-07-09-57', '2021-09-15-09-07-49', '2021-09-04-10-38-07'],
        'scai-qrecc21-basic-baseline': ['2021-08-26-17-46-42'],
        'scai-qrecc21-gpt3-baseline': ['2021-07-21-08-56-42'],
        'scai-qrecc21-simple-baseline': ['2021-07-20-21-01-58'],
        'torch': ['2021-09-20-05-42-29'],
        'ultron': ['2021-09-04-17-16-58'],
    },
    'scai-qrecc21-test-dataset-rewritten-2021-07-20': {
        'rachael': ['2021-09-04-10-39-42', '2021-09-15-19-36-31', '2021-09-06-09-21-43'],
        'rali-qa': ['2021-09-09-13-01-07'],
        'scai-qrecc21-basic-baseline': ['2021-08-26-14-42-21'],
        'scai-qrecc21-simple-baseline': ['2021-07-21-08-58-25'],
        'ultron': ['2021-09-08-15-08-00', '2021-09-19-18-40-28', '2021-09-08-15-04-28', '2021-09-08-15-07-30', '2021-09-13-17-56-51', '2021-09-13-17-47-43'],
    },
}


def parse_run_name(file_name):
    import json
    try:
        lines = [i for i in open(file_name)]
        ret = json.loads(lines[-1])['run_name']
        if not ret:
            return 'no-run-identifier'
        return ret
    except:
        return 'no-run-identifier'


def copy(src, target):
    import shutil
    shutil.copy(src, target)

if __name__ == '__main__':
    from tqdm import tqdm
    for test_dataset in VALID_RUNS:
        for user in tqdm(VALID_RUNS[test_dataset]):
            for run_timestamp in VALID_RUNS[test_dataset][user]:
                run_dir = '/mnt/ceph/tira/data/runs/' + test_dataset + '/' + user + '/' + run_timestamp + '/'
                run_name = parse_run_name(run_dir + 'stdout.txt')
                copy(run_dir + 'output/run.json', 'out/' + test_dataset + '/' + test_dataset + '-' + user + '-' + run_name  + '-' + run_timestamp + '.json')

