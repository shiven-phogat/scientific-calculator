# calculator.py
import math

def sqrt(x):
    if x < 0:
        raise ValueError("Square root undefined for negative numbers")
    return math.sqrt(x)

def factorial(n):
    # Accept integers only
    if not (isinstance(n, int) or (isinstance(n, float) and n.is_integer())):
        raise ValueError("Factorial requires an integer")
    n = int(n)
    if n < 0:
        raise ValueError("Factorial undefined for negative numbers")
    return math.factorial(n)

def ln(x):
    if x <= 0:
        raise ValueError("Natural log undefined for non-positive numbers")
    return math.log(x)

def power(x, b):
    return math.pow(x, b)
