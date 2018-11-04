from pylatex import Math, Matrix, NoEscape
import numpy as np
from sympy import latex, Integral, Symbol


def draw_polynomial(data):
    return NoEscape('\\begin{{equation}}{} = 0\\end{{equation}'.format(latex(data)))


def draw_integral(data, fn, render=True):
    x = Symbol('x')
    equation = Integral(fn, (x, data.get('lower_bound'), data.get('upper_bound')))
    if render:
        return NoEscape('\\begin{{equation}}{}\\end{{equation}'.format(latex(equation)))
    else:
        return NoEscape('\\begin{{equation}}{}\\end{{equation}'.format(equation))


def draw_derivative(data, fn, render=True):
    if render:
        return NoEscape('\\begin{{equation}}\\frac{{d}}{{d{}}} ({})\\end{{equation}}'.format(data.get('wrt'), latex(fn)))
    else:
        return NoEscape('\\begin{{equation}}\\frac{{d}}{{d{}}} {}\\end{{equation}}'.format(data.get('wrt'), fn))


def draw_matrix(data):
    M = np.matrix(data['numbers']).reshape([data['n'], data['m']])
    return Math(data=[Matrix(M)])


def draw_random_matrix(data):
    M = np.random.randint(1, 99, size=(data['n'], data['m']))
    return Math(data=[Matrix(M)])


def draw_trig(data):
    return NoEscape('\\begin{{equation}}{}\\end{{equation}'.format(data))
