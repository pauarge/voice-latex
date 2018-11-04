from pylatex import Math, Matrix, NoEscape
import numpy as np
from sympy import latex, Integral

from parser.Polynomial import Polynomial


def draw_polynomial(data):
    coefs = data['coefs']
    k = len(coefs) - 1
    res = coefs[0] ** (k)
    for i in range(1, len(coefs) - 1):
        k = k - 1
        res = res + coefs[i] ** k
    return NoEscape('\\[{}\\]'.format(latex(res)))


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
    M = np.random.randint(1, 99, size=(data['n'], data['m']))
    return Math(data=[Matrix(M)])
