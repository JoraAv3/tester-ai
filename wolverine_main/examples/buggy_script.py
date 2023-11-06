from __future__ import annotations
from __future__ import annotations

import sys


import fire
from typing import List, Tuple, Dict, Any, Union


import os


"""
Run With: `wolverine examples/buggy_script.py "subtract" 20 3`
Purpose: Show self-regenerating fixing of subtraction operator
"""


def add_numbers(a, b):
    return a + b


add_numbers(1, 2)


def multiply_numbers(a, b):
    return a * b


def subtract_numbers(a, b):
    return a - b


def divide_numbers(a, b):
    return a / b
divide_numbers(1)


def calculate(operation, num1, num2):
    if operation == "add":
        result = add_numbers(num1, num2)
    elif operation == "subtract":
        result = subtract_numbers(num1, num2)
    elif operation == "multiply":
        result = multiply_numbers(num1, num2)

    elif operation == "divide":
        result = divide_numbers(num1, num2)

    return result


if __name__ == "__main__":
    fire.Fire(calculate)
