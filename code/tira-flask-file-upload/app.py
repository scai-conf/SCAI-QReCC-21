from flask import Flask
from flask import request
import datetime
import json
import os
from subprocess import check_output
app = Flask(__name__)

OUT_DIR='/mnt/ceph/tira/data/runs/scai-qrecc21-toy-dataset-2021-05-15'

def vm_name(request):
    if not(request) or not(request.headers) or not('X-Disraptor-Groups' in request.headers):
        return None
    
    groups = request.headers.get('X-Disraptor-Groups')
    if not groups or 'tira_vm_' not in groups:
        return None
    ret = (',' + groups +',').split(',tira_vm_')[1].split(',')[0]
    ret = ret if ret else None

    print('Handle request for virtual machine "' + ret + '".')
    return ret

HEADER='''<h1>Run File Submissions for SCAI QReCC 21: Conversational Question Answering Challenge</h1>

'''

NOT_REGISTERED=HEADER +  'Your TIRA account is currently not registered for the shared task "SCAI QReCC 21: Conversational Question Answering Challenge".<br><br> Please contact us to register.'


@app.route('/run-upload-scai-qrecc21')
def hello_world():
    vm = vm_name(request)

    if not vm:
        return NOT_REGISTERED
    
    href_link = '<a href="https://www.tira.io/task/scai-qrecc/user/' + vm + '">https://www.tira.io/task/scai-qrecc/user/' + vm + '</a>'
    return HEADER + '''
The preferred way to submit runs for the shared task is via software submissions in TIRA to ensure reproducibility.<br>
You can make software submissions at ''' + href_link + '''.<br>
If you don't want to make software submissions, you can upload a run file with the following formular.<br>
Please note (todo: add some hints on how to get your stuff on the leaderboard, etc).<br>

<form action="/run-upload-scai-qrecc21/upload" method="POST" enctype="multipart/form-data">
  <label for="user">Upload run file for: ''' + vm + '''</label><br>
  <input type="file" id="file" name="file">
  <input type="submit" value="Submit">
</form>'''

def run_id():
    return datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

def build_run(data, run_id, vm):
    run_dir = os.path.join(OUT_DIR, vm, run_id)
    os.makedirs(os.path.join(run_dir, 'output'))
    output_file = os.path.join(run_dir, 'output', 'run.json')

    with open(os.path.join(run_dir, 'output', 'run.json'), 'wb') as f:
        f.write(data)

    with open(os.path.join(run_dir, 'run.prototext'), 'w') as f:
        f.write(run_prototext(run_id))

    with open(os.path.join(run_dir, 'file-list.txt'), 'wb') as f:
        file_list = check_output(['tree', '-ahv', os.path.join(run_dir, 'output')])
        f.write(file_list)

    with open(os.path.join(run_dir, 'size.txt'), 'wb') as f:
        f.write(check_output(['bash', '-c', '(du -sb "' + run_dir + '" && du -hs "' +  run_dir + '") | cut -f1']))
        f.write(check_output(['bash', '-c', 'find "' + os.path.join(run_dir, 'output') + '" -type f -exec cat {} + | wc -l']))
        f.write(check_output(['bash', '-c', 'find "' + os.path.join(run_dir, 'output') + '" -type f | wc -l']))
        f.write(check_output(['bash', '-c', 'find "' + os.path.join(run_dir, 'output') + '" -type d | wc -l']))

    check_output(['chmod', '775', '-R', os.path.join(OUT_DIR, vm)])
    
def run_prototext(run_id):
    return '''softwareId: "ManualRun"
runId: "'''+ run_id + '''"
inputDataset: "scai-qrecc21-toy-dataset-2021-05-15"
inputRun: "none"
downloadable: true
deleted: false
taskId: "scai-qrecc"
accessToken: "manual-run-no-access-token"'''

@app.route('/run-upload-scai-qrecc21/upload',methods=['POST'])
def upload_file():
    vm = vm_name(request)
    if not vm:
        return NOT_REGISTERED
    if not request.files or 'file' not in request.files:
        raise ValueError('There is no file submitted to the server.')

    #touche-2021-task1/macbeth/2021-05-06-08-39-13/output
    data = request.files['file'].read()

    build_run(data, run_id(), vm)

    return "Short message: it was successful.<br><br>Add name of run file, link to the evaluator, and link to the task page/page for additional submits"

