import pytest
from gaussed.temp import double, halve


def test_double():
    assert double(2) == 4


def test_halve():
    assert halve(4) == 2