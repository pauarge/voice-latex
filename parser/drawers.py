from pylatex import Math, Matrix, NoEscape
import numpy as np
from sympy import latex, Integral

from parser.Polynomial import Polynomial


def draw_polynomial(doc, data):
    raise NotImplementedError


def draw_integral(doc, data):
    poly = Polynomial(data['function'])
    eq, sym = poly.parse()
    equation = Integral(eq, (sym, data['lower_bound'], data['upper_bound']))
    doc.append(NoEscape(latex(equation)))


def draw_derivative(doc, data):
    raise NotImplementedError


def draw_matrix(doc, data):
    M = np.matrix(data['numbers']).reshape([data['n'], data['m']])
    doc.append(Math(data=[Matrix(M)]))
