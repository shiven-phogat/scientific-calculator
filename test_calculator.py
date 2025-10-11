# tests/test_calculator.py
import pytest
import math
import calculator


def test_sqrt_valid():
    assert calculator.sqrt(4) == 2.0
    assert calculator.sqrt(0) == 0.0


def test_sqrt_invalid():
    with pytest.raises(ValueError):
        calculator.sqrt(-1)


def test_factorial_valid():
    assert calculator.factorial(5) == 120
    assert calculator.factorial(0) == 1


def test_factorial_invalid():
    with pytest.raises(ValueError):
        calculator.factorial(-3)
    with pytest.raises(ValueError):
        calculator.factorial(2.5)


def test_ln_valid():
    assert math.isclose(calculator.ln(math.e), 1.0, rel_tol=1e-7)


def test_ln_invalid():
    with pytest.raises(ValueError):
        calculator.ln(0)


def test_power():
    assert math.isclose(calculator.power(2, 3), 8.0, rel_tol=1e-7)
    assert math.isclose(calculator.power(9, 0.5), 3.0, rel_tol=1e-7)
