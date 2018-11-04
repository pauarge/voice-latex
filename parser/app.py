from flask import Flask, request
from pylatex import Document, NewLine, Command, NoEscape
import requests

from parser.Polynomial import Polynomial
from parser.drawers import draw_polynomial, draw_integral, draw_matrix, draw_derivative, draw_random_matrix

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
        m_data = {
            'n': data.get('first_dim'),
            'm': data.get('second_dim'),
            'numbers': data.get('vals'),
        }
        commands.append(draw_matrix(m_data))

    elif intentname == 'random-matrix':
        m_data = {
            'n': data.get('first_dim'),
            'm': data.get('second_dim'),
        }
        commands.append(draw_random_matrix(m_data))

    elif intentname == 'polynomial':
        f = Polynomial(data.get('coef'))
        op = data.get('operation')
        if op == 'integral':
            commands.append(draw_integral({
                'upper_bound': data.get('upper_bound'),
                'lower_bound': data.get('lower_bound'),
                'function': f.parse()
            }))
        elif op == 'derivate':
            commands.append(draw_derivative({
                'wrt': data.get('wrt'),
                'function': f.parse(),
            }))
        else:
            commands.append(draw_polynomial(f.parse()))

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
