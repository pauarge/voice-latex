import numpy as np

from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat
from pylatex.utils import italic
import os


OUT_PATH = '../out/generated'


def main():
    geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
    doc = Document(geometry_options=geometry_options)

    with doc.create(Section('The simple stuff')):
        doc.append('Some regular text and some')
        doc.append(italic('italic text. '))
        doc.append('\nAlso some crazy characters: $&#{}')

    doc.generate_pdf(OUT_PATH, clean_tex=False)


if __name__ == '__main__':
    main()
