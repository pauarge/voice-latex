from flask import Flask, request
from pylatex import Document, NewLine, Command
import requests

from parser.drawers import draw_polynomial, draw_integral, draw_matrix, draw_derivative

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
    slots = data['slots']

    if intentname == 'integral':
        lower_bound = None
        upper_bound = None
        fun = None

        for slot in slots:
            if slot['slotName'] == 'function':
                fun = slot['rawValue']
            elif slot['slotName'] == 'lower_bound':
                lower_bound = int(slot['value']['value'])
            elif slot['slotName'] == 'upper_bound':
                upper_bound = int(slot['value']['value'])

        data = {
            'upper_bound': upper_bound,
            'lower_bound': lower_bound,
            'function': fun
        }
        commands.append(draw_integral(data))

    elif intentname == 'derivate':
        fun = None
        wrt = None

        for slot in slots:
            if slot['slotName'] == 'function':
                fun = slot['rawValue']
            elif slot['slotName'] == 'wrt':
                wrt = slot['rawValue']

        data = {
            'wrt': wrt,
            'function': fun
        }
        commands.append(draw_derivative(data))

    elif intentname == 'matrix':
        pass

    try:
        for c in commands:
            doc.append(c)
            doc.append(NewLine())
            doc.append(NewLine())
        doc.generate_pdf(OUT_PATH, clean_tex=False)
    except Exception as e:
        print(e)

    # requests.get(RENDERER_URL).json()
    return "ok"


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
