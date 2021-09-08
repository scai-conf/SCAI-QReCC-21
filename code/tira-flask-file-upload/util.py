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

def run_id(current_time):
    return current_time.strftime('%Y-%m-%d-%H-%M-%S')

def next_software_num(vm_id):
    from pathlib import Path
    if Path('/mnt/ceph/tira/model/softwares/scai-qrecc/' + vm_id + '/softwares.prototext').is_file():
        max_num = 0
        with open('/mnt/ceph/tira/model/softwares/scai-qrecc/' + vm_id + '/softwares.prototext', 'r') as f:
            for l in f:
                if 'count: "' in l:
                    l = l.split('count: "')[1]
                    if '"' in l:
                        l = int(l.split('"')[0])
                        if l > max_num:
                            max_num = l
        return max_num +1
    return 1

def run_prototext(run_id, input_dataset, software_id):
    return '''softwareId: "software''' + str(software_id) + '''"
runId: "'''+ run_id + '''"
inputDataset: "''' + input_dataset + '''"
inputRun: "none"
downloadable: true
deleted: false
taskId: "scai-qrecc"
accessToken: "manual-run-no-access-token"'''

def run_software(current_time, dataset, num, run_name):
    current_time = current_time.strftime('%a %b %d %H:%M:%S UTC %Y')
    return '''softwares {
  id: "software''' + str(num) + '''"
  count: "''' + str(num) + '''"
  command: "# This software documents a manual upload of a run file named ''' + run_name + ''' on ''' + current_time + '''"
  workingDirectory: ""
  dataset: "''' + dataset + '''"
  run: "none"
  creationDate: "''' + current_time + '''"
  lastEditDate: "''' + current_time + '''"
  deleted: false
}
'''

def build_run(data, vm, current_time, input_dataset, run_name):
    from subprocess import check_output
    import os
    
    out_dir = '/mnt/ceph/tira/data/runs/' + input_dataset
    run_dir = os.path.join(out_dir, vm, run_id(current_time))
    os.makedirs(os.path.join(run_dir, 'output'), exist_ok=True)
    os.makedirs(os.path.join('/mnt/ceph/tira/model/softwares/scai-qrecc/', vm), exist_ok=True)
    output_file = os.path.join(run_dir, 'output', 'run.json')

    with open(os.path.join(run_dir, 'output', 'run.json'), 'wb') as f:
        f.write(data)

    with open(os.path.join(run_dir, 'run.prototext'), 'w') as f:
        f.write(run_prototext(run_id(current_time), input_dataset, next_software_num(vm)))

    with open(os.path.join(run_dir, 'file-list.txt'), 'wb') as f:
        file_list = check_output(['tree', '-ahv', os.path.join(run_dir, 'output')])
        f.write(file_list)

    with open(os.path.join('/mnt/ceph/tira/model/softwares/scai-qrecc/', vm, 'softwares.prototext'), 'a+') as f:
        f.write('\n\n' + run_software(current_time, input_dataset, next_software_num(vm), run_name))

    with open(os.path.join(run_dir, 'stdout.txt'), 'wb') as f:
        f.write('This software was not executed in TIRA and documents a manual upload of a run file named "' + run_name + '" on ' + current_time.strftime('%a %b %d %H:%M:%S UTC %Y') + '.\n')

    with open(os.path.join(run_dir, 'size.txt'), 'wb') as f:
        f.write(check_output(['bash', '-c', '(du -sb "' + run_dir + '" && du -hs "' +  run_dir + '") | cut -f1']))
        f.write(check_output(['bash', '-c', 'find "' + os.path.join(run_dir, 'output') + '" -type f -exec cat {} + | wc -l']))
        f.write(check_output(['bash', '-c', 'find "' + os.path.join(run_dir, 'output') + '" -type f | wc -l']))
        f.write(check_output(['bash', '-c', 'find "' + os.path.join(run_dir, 'output') + '" -type d | wc -l']))

    check_output(['chmod', '775', '-R', os.path.join(out_dir, vm)])

