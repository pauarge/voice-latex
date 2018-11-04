from pylatex import Math, Matrix, NoEscape
import numpy as np
from sympy import latex, Integral, Symbol


def draw_polynomial(data):
    return NoEscape('\\[{}\\]'.format(latex(data)))


def draw_integral(data):
    x = Symbol('x')
    equation = Integral(data['function'], (x, data['lower_bound'], data['upper_bound']))
    return NoEscape('\\[{}\\]'.format(latex(equation)))


def draw_derivative(data):
    return NoEscape('\\[\\frac{{d}}{{d{}}} ({})\\]'.format(data['wrt'], latex(data['function'])))


def draw_matrix(data):
    M = np.matrix(data['numbers']).reshape([data['n'], data['m']])
    return Math(data=[Matrix(M)])


def draw_random_matrix(data):
    M = np.random.randint(1, 99, size=(data['n'], data['m']))
    return Math(data=[Matrix(M)])
