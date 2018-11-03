from pylatex import Math, Matrix
import numpy as np


def draw_integral(doc, data):
    doc.append(Math(data=['2*3', '=', 9]))


def draw_derivative(doc, data):
    raise NotImplementedError


def draw_matrix(doc, data):
    M = np.matrix(data['numbers']).reshape([data['n'], data['m']])
    doc.append(Math(data=[Matrix(M)]))
