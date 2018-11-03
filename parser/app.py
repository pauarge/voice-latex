from pylatex import Document

from parser.drawers import draw_integral

OUT_PATH = '../renderer/public/generated'


def main():
    geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
    doc = Document(geometry_options=geometry_options)

    data = {
        'upper_bound': 1,
        'lower_bound': 2,
        'function': 'x squared'
    }
    draw_integral(doc, data)

    doc.generate_pdf(OUT_PATH, clean_tex=False)


if __name__ == '__main__':
    main()
