'''
file: test_helpers.py
contains test for the helpers functions
'''
from pizstrip.helpers import count_matrix_pixels, cursor


def test_count_matrix_pixels():
    expected = 10
    result = count_matrix_pixels(2, 5)
    assert result == expected

def test_set_cursor_position(capsys):
    cursor(x=1, y=10, data="test")
    out, err = capsys.readouterr()
    expected = '\033[1;10Htest\n'
    assert out == expected
