import numpy as np

def solution(num):
    remainder = num
    squares = list()
    while remainder > 0:
        nearest_square, remainder = nearest_smaller_square(remainder)
        squares.append(np.square(nearest_square))
    return squares

def nearest_smaller_square(num):
    nearest_square = np.int(np.floor(np.sqrt(num)))
    remainder = num - np.square(nearest_square)
    return nearest_square, remainder
