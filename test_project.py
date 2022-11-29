# cmd /K python "$(FULL_CURRENT_PATH)"

# pip install pygame

import pygame
import sys
import random
from project import useless_function_one, useless_function_two, useless_function_three


def test_useless_function_one():
	assert useless_function_one(1, 1, 1) == 1
	assert useless_function_one(1, 1, 1) != 2
	
def test_useless_function_two():
	assert useless_function_two(0, 0, 10) == 10
	assert useless_function_two(0, 0, 11) != 10
	
def test_useless_function_three():
	assert useless_function_three(1, 1, 0) == 1
	assert useless_function_three(2, 2, 1) == 5