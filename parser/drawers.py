from pylatex import Math


def draw_integral(doc, data):
    doc.append(Math(data=['2*3', '=', 9]))


def draw_derivative(doc, data):
    raise NotImplementedError


def draw_matrix(doc, data):
    raise NotImplementedError
