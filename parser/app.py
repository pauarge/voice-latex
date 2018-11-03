from flask import Flask, request
from pylatex import Document
import requests

from parser.drawers import draw_polynomial, draw_integral, draw_matrix

RENDERER_URL = 'http://127.0.0.1:3000/update'
OUT_PATH = '../renderer/public/generated'

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello():
    data = request.get_json()
    doc = Document()

    user, intentname = data['intent']['intentName'].split(':')
    if intentname == 'integral':
        slots = data['slots']
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
        draw_integral(doc, data)

    elif intentname == 'derivate':
        pass
    elif intentname == 'matrix':
        pass

    try:
        doc.generate_pdf(OUT_PATH, clean_tex=False)
    except:
        pass

    # requests.get(RENDERER_URL).json()
    return "ok"


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
