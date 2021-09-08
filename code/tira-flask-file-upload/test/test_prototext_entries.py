from util import run_software, run_prototext, run_id
from approvaltests.approvals import verify
from datetime import datetime

def test_run_prototext():
    current_time = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
    verify(run_prototext(run_id(current_time), 'scai-qrecc21-test-dataset-2021-05-15', 1))

def test_run_software_1():
    current_time = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
    verify(run_software(current_time, 'my-test-dataset-1', 23, 'my-run-tag'))

