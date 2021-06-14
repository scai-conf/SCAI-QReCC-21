from util import vm_name

def test_vm_name_example_1():
    request = DummyRequest({'X-Disraptor-Groups': 'tira_vm_example1'})
    expected = 'example1'
    actual = vm_name(request)

    assert expected == actual

def test_vm_name_is_none_1():
    request = DummyRequest({'X-Disraptor-Groups': 'tira_m_example1'})
    expected = None
    actual = vm_name(request)

    assert expected == actual


class DummyRequest():
    def __init__(self, headers):
        self.headers = headers

