from flask import Flask, redirect
from flask import request
import datetime
from util import vm_name, build_run
app = Flask(__name__)

HEADER='''<!DOCTYPE html>
<html>
<head>
<title>Page Title</title>
</head>
<body>

<h1>Run File Submissions for SCAI QReCC 21: Conversational Question Answering Challenge</h1>

'''

FOOTER='''</body>
</html>
'''

NOT_REGISTERED=HEADER +  'Your TIRA account is currently not registered for the shared task "SCAI QReCC 21: Conversational Question Answering Challenge".<br><br> Please contact us to register.' + FOOTER


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
  <label for="dataset">Dataset:</label>
  <select name="dataset" id="dataset">
    <option value="scai-qrecc21-test-dataset-2021-05-15">scai-qrecc21-test-dataset-2021-05-15</option>
    <option value="scai-qrecc21-toy-dataset-2021-05-15">scai-qrecc21-toy-dataset-2021-05-15</option>
  </select><br>
  <label for="file">Run-File:</label>
  <input type="file" id="file" name="file"><br>
  <input type="submit" value="Submit">
</form>''' + FOOTER

    
@app.route('/run-upload-scai-qrecc21/upload',methods=['POST'])
def upload_file():
    vm = vm_name(request)

    if not vm:
        return NOT_REGISTERED
    if not request.files or 'file' not in request.files:
        raise ValueError('There is no file submitted to the server.')
    if not request.form or 'dataset' not in request.form:
        raise ValueError('There is dataset submitted to the server.')

    data = request.files['file'].read()
    input_dataset = request.form['dataset']
    if input_dataset not in ['scai-qrecc21-test-dataset-2021-05-15', 'scai-qrecc21-toy-dataset-2021-05-15']:
        raise ValueError('Unknown dataset: ' + str(input_dataset))

    build_run(data, vm, datetime.datetime.now(), input_dataset)

    ret = redirect('/task/scai-qrecc/user/' + str(vm) + '/', code=303)
    ret.autocorrect_location_header = False

    return ret

