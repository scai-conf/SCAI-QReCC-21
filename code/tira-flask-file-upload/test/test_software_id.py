from util import next_software_num

def test_next_software_num_for_non_existing_user_1():
    expected = 1
    actual = next_software_num(vm_id='does-not-exist-1')
    assert expected == actual

def test_next_software_num_for_non_existing_user_2():
    expected = 1
    actual = next_software_num(vm_id='does-not-exist-2')
    assert expected == actual

def test_next_sotware_num_for_existing_user_1():
    expected = 2
    actual = next_software_num(vm_id='scai-qrecc21-simple-baseline')
    assert expected == actual

def test_next_sotware_num_for_existing_user_2():
    expected = 6
    actual = next_software_num(vm_id='test-user')
    print(actual)
    assert expected == actual

