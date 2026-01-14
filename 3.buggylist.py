import pytest

def get_last_item(my_list):
    return my_list

def test_get_last_item():
    data = [10, 20, 30]
    assert get_last_item(data) == 30