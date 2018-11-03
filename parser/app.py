from pylatex import Document
import requests

from parser.drawers import draw_polynomial, draw_integral, draw_matrix

RENDERER_URL = 'http://127.0.0.1:3000/update'
OUT_PATH = '../renderer/public/generated'


def main():
    doc = Document()

    data = {
        'function': '2 x squared'
    }
    draw_polynomial(doc, data)

    # data = {
    #     'upper_bound': 1,
    #     'lower_bound': 2,
    #     'function': 'x squared'
    # }
    # draw_integral(doc, data)

    # data = {
    #     'n': 3,
    #     'm': 2,
    #     'numbers': [1, 2, 3, 4, 5, 6]
    # }
    # draw_matrix(doc, data)

    doc.generate_pdf(OUT_PATH, clean_tex=False)
    requests.get(RENDERER_URL).json()


if __name__ == '__main__':
    main()
