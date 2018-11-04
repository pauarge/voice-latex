from pylatex import Math, Matrix, NoEscape
import numpy as np
from sympy import latex, Integral, Symbol


def draw_polynomial(data):
    return NoEscape('\\[{} = 0\\]'.format(latex(data)))


def draw_integral(data, render=True):
    x = Symbol('x')
    equation = Integral(data['function'], (x, data['lower_bound'], data['upper_bound']))
    if render:
        return NoEscape('\\[{}\\]'.format(latex(equation)))
    else:
        return NoEscape('\\[{}\\]'.format(equation))


def draw_derivative(data, render=True):
    lt = latex(data['function']) if render else data['function']
    return NoEscape('\\[\\frac{{d}}{{d{}}} ({})\\]'.format(data['wrt'], lt))


def draw_matrix(data):
    M = np.matrix(data['numbers']).reshape([data['n'], data['m']])
    return Math(data=[Matrix(M)])


def draw_random_matrix(data):
    M = np.random.randint(1, 99, size=(data['n'], data['m']))
    return Math(data=[Matrix(M)])


def draw_trig(data):
    return NoEscape('\\[{}\\]'.format(data))
