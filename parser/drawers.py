from pylatex import Math, Matrix, NoEscape
import numpy as np
from sympy import latex, Integral

from parser.Polynomial import Polynomial


def draw_polynomial(data):
    poly = Polynomial(data['function'])
    eq, sym = poly.parse()
    return NoEscape('\\[{}\\]'.format(latex(eq)))


def draw_integral(data):
    poly = Polynomial(data['function'])
    eq, sym = poly.parse()
    equation = Integral(eq, (sym, data['lower_bound'], data['upper_bound']))
    return NoEscape('\\[{}\\]'.format(latex(equation)))


def draw_derivative(data):
    poly = Polynomial(data['function'])
    eq, _ = poly.parse()
    return NoEscape('\\[\\frac{{d}}{{d{}}} {}\\]'.format(data['wrt'], latex(eq)))


def draw_matrix(data):
    M = np.matrix(data['numbers']).reshape([data['n'], data['m']])
    return Math(data=[Matrix(M)])


def draw_random_matrix(data):
    M = np.random.randint(5, size=(data['n'], data['m']))
    return Math(data=[Matrix(M)])
