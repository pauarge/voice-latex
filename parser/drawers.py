from pylatex import Math, Matrix, NoEscape
import numpy as np
from sympy import latex, Integral, Symbol


def draw_polynomial(doc, data):
    raise NotImplementedError


def draw_integral(doc, data):
    x = Symbol(data['function'])
    equation = Integral(x, (x, data['lower_bound'], data['upper_bound']))
    doc.append(NoEscape(latex(equation)))


def draw_derivative(doc, data):
    raise NotImplementedError


def draw_matrix(doc, data):
    M = np.matrix(data['numbers']).reshape([data['n'], data['m']])
    doc.append(Math(data=[Matrix(M)]))
