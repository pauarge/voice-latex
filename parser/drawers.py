from pylatex import Math, Matrix, NoEscape
import numpy as np
from sympy import latex, Integral, Symbol


def draw_polynomial(data):
    return NoEscape('\\begin{{equation}}{} = 0\\end{{equation}}'.format(latex(data)))


def draw_integral(data, fn, render=True):
    x = Symbol('x')
    if render:
        if data.get('lower_bound') and data.get('upper_bound'):
            equation = Integral(fn, (x, data.get('lower_bound'), data.get('upper_bound')))
            return NoEscape('\\begin{{equation}}{}\\end{{equation}}'.format(latex(equation)))
        else:
            return NoEscape('\\begin{{equation}}int {} dx\\end{{equation}}'.format(latex(fn)))
    else:
        if data.get('lower_bound') and data.get('upper_bound'):
            return NoEscape(
                '\\begin{{equation}}\int_{{{}}}^{{{}}} {} dx\\end{{equation}}'.format(data.get('lower_bound'),
                                                                                      data.get('upper_bound'),
                                                                                      fn))
        else:
            return NoEscape('\\begin{{equation}}\int {} dx\\end{{equation}}'.format(fn))


def draw_derivative(data, fn, render=True):
    if render:
        return NoEscape(
            '\\begin{{equation}}\\frac{{d}}{{d{}}} ({})\\end{{equation}}'.format(data.get('wrt'), latex(fn)))
    else:
        return NoEscape('\\begin{{equation}}\\frac{{d}}{{d{}}} {}\\end{{equation}}'.format(data.get('wrt'), fn))


def draw_matrix(data):
    M = np.matrix(data['vals']).reshape([data['first_dim'], data['second_dim']])
    return Math(data=[Matrix(M)])


def draw_multiply_matrix(data):
    M1 = np.matrix(data['vals']).reshape([data.get('first_dim'), data.get('second_dim')])
    M2 = np.random.randint(1, 99, size=(data.get('second_dim'), data.get('third_dim')))
    return Math(data=[Matrix(M1), Matrix(M2), '=', Matrix(M1.dot(M2))])


def draw_random_matrix(data):
    M = np.random.randint(1, 99, size=(data.get('first_dim'), data.get('second_dim')))
    return Math(data=[Matrix(M)])


def draw_random_multiply_matrix(data):
    M1 = np.random.randint(1, 99, size=(data.get('first_dim'), data.get('second_dim')))
    M2 = np.random.randint(1, 99, size=(data.get('second_dim'), data.get('third_dim')))
    return Math(data=[Matrix(M1), Matrix(M2), '=', Matrix(M1.dot(M2))])


def draw_inverse_matrix(data):
    M = np.matrix(data['vals']).reshape([data['first_dim'], data['second_dim']])
    return Math(data=['inv', Matrix(M), '=', Matrix(np.linalg.pinv(M))])


def draw_trig(data):
    return NoEscape('\\begin{{equation}}{}\\end{{equation}}'.format(data))
