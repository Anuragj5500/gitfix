import pytest

def reverse_text(text):
    # Correctly reverse the text
    return text[::-1]

def test_reverse_text():
    # This test will now PASS
    assert reverse_text("hello") == "olleh"
    assert reverse_text("Python") == "nohtyP"