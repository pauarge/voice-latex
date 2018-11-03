from pylatex import Math, Matrix, NoEscape, NewLine
import numpy as np
from sympy import latex, Integral

from parser.Polynomial import Polynomial


def draw_polynomial(doc, data):
    poly = Polynomial(data['function'])
    eq, sym = poly.parse()
    doc.append(NoEscape(latex(eq)))
    doc.append(NewLine())
    doc.append(NewLine())


def draw_integral(doc, data):
    poly = Polynomial(data['function'])
    eq, sym = poly.parse()
    equation = Integral(eq, (sym, data['lower_bound'], data['upper_bound']))
    doc.append(NoEscape(latex(equation)))
    doc.append(NewLine())
    doc.append(NewLine())


def draw_derivative(doc, data):
    poly = Polynomial(data['function'])
    doc.append(NewLine())
    doc.append(NewLine())


def draw_matrix(doc, data):
    M = np.matrix(data['numbers']).reshape([data['n'], data['m']])
    doc.append(Math(data=[Matrix(M)]))
    doc.append(NewLine())
    doc.append(NewLine())
