from flask import Flask, redirect, render_template
from flask import request
import datetime
from util import vm_name, build_run
app = Flask(__name__)


@app.route('/run-upload-scai-qrecc21')
def hello_world():
    vm = vm_name(request)

    if not vm:
        return render_template('not-registered.html')
    
    return render_template('run-file-upload.html',
        href_link = '<a href="https://www.tira.io/task/scai-qrecc/user/' + vm + '">https://www.tira.io/task/scai-qrecc/user/' + vm + '</a>',
        vm = vm
    )


@app.route('/run-upload-scai-qrecc21/upload',methods=['POST'])
def upload_file():
    vm = vm_name(request)

    if not vm:
        return NOT_REGISTERED
    if not request.files or 'file' not in request.files:
        raise ValueError('There is no file submitted to the server.')
    if not request.form or 'dataset' not in request.form:
        raise ValueError('There is dataset submitted to the server.')
    if not request.form or 'run_name' not in request.form:
        raise ValueError('Run name not submitted.')


    data = request.files['file'].read()
    input_dataset = request.form['dataset']
    run_name = request.form['run_name']
    if input_dataset not in ['scai-qrecc21-toy-dataset-2021-07-20', 'scai-qrecc21-toy-dataset-rewritten-2021-07-20', 'scai-qrecc21-toy-dataset-2021-05-15', 'scai-qrecc21-test-dataset-2021-05-15', 'scai-qrecc21-test-dataset-2021-07-20', 'scai-qrecc21-test-dataset-rewritten-2021-07-20']:
        raise ValueError('Unknown dataset: ' + str(input_dataset))

    build_run(data, vm, datetime.datetime.now(), input_dataset, run_name)

    ret = redirect('/task/scai-qrecc/user/' + str(vm) + '/', code=303)
    ret.autocorrect_location_header = False

    return ret

