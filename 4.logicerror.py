import pytest

def calculate_sum(a, b):
    # Fixed the bug: Changed subtraction to addition
    return a + b

def test_calculate_sum():
    # This test will now pass
    assert calculate_sum(5, 3) == 8
    assert calculate_sum(10, 10) == 20

if __name__ == "__main__":
    pytest.main(["-v"])