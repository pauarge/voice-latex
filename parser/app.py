from flask import Flask, request
from pylatex import Document, NewLine, Command, TikZ, Axis, Plot
import requests

from parser.Polynomial import Polynomial
from parser.Trig import Trig
from parser.drawers import draw_polynomial, draw_integral, draw_matrix, draw_derivative, draw_random_matrix, draw_trig, \
    draw_multiply_matrix, draw_random_multiply_matrix, draw_inverse_matrix

RENDERER_URL = 'http://127.0.0.1:3000/update'
OUT_PATH = '../renderer/public/generated'

app = Flask(__name__)

commands = []


@app.route("/", methods=['GET', 'POST'])
def draw():
    data = request.get_json()
    doc = Document()
    doc.append(Command('fontsize', arguments=['15', '12']))
    doc.append(Command('selectfont'))

    user, intentname = data['intent']['intentName'].split(':')

    if intentname == 'matrix':
        if data.get('operation') == 'matrix_mult':
            commands.append(draw_multiply_matrix(data))
        elif data.get('operation') == 'matrix_inverse':
            commands.append(draw_inverse_matrix(data))
        else:
            commands.append(draw_matrix(data))

    elif intentname == 'random-matrix':
        if data.get('operation') == 'matrix_mult':
            commands.append(draw_random_multiply_matrix(data))
        else:
            commands.append(draw_random_matrix(data))

    elif intentname == 'polynomial':
        f = Polynomial(data.get('coef'))
        op = data.get('operation')
        if op == 'integral':
            commands.append(draw_integral(data, f.parse()))
        elif op == 'derivate':
            commands.append(draw_derivative(data, f.parse()))
        elif op == 'plot':
            with doc.create(TikZ()):
                plot_options = 'height=10cm, width=10cm'
                with doc.create(Axis(options=plot_options)) as plot:
                    plot.append(Plot(func=f.toPlot()))
        else:
            commands.append(draw_polynomial(f.parse()))

    elif intentname == 'trigfunc':
        f = Trig(data.get('trigfunc'), data.get('var'), data.get('auxoper'))
        op = data.get('operation')
        if op == 'integral':
            commands.append(draw_integral(data, f.parse(), render=False))
        elif op == 'derivate':
            commands.append(draw_derivative(data, f.parse(), render=False))
        else:
            commands.append(draw_trig(f.parse()))

    try:
        for c in commands:
            doc.append(c)
            doc.append(NewLine())
            doc.append(NewLine())
        doc.generate_pdf(OUT_PATH, clean_tex=False)
    except Exception as e:
        print(e)

    try:
        requests.get(RENDERER_URL).json()
    except:
        pass

    return "ok"


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
