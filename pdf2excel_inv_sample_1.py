# _*_ coding:utf-8 _*_

import PyPDF2
import pandas as pd
import re
import os
import sys
import time
import fitz
from fitz import Rect


# print(fitz.__doc__)

def extract_text_from_pdf_by_regions(pdf_filepath):
    pdffile = pdf_filepath
    docs = fitz.open(pdffile)
    text = docs[0].get_textpage().extractTEXT()

    # print(docs.page_count)
    # print(docs.metadata)
    # print(docs.get_toc())
    # print(docs[0].get_links())
    # print(docs[0].annots())
    # print(docs[0].widgets())

    # pix = docs[0].get_pixmap()
    # pix.save('1.png')

    # dd = docs[0].get_text('rawdict')  # 'text', 'blocks', 'words', 'html' , 'dict/json','xml', 'rawdict/rawjson', 'xhtml'
    # print(dd)

    # print(len(text))
    # print(text)

    # areas = docs[0].search_for('811264888')
    # for i in areas:print(i)

    '''
    text_items = docs[0].get_text_blocks()
    for block in text_items:
        for line in block:
            print(line)
    '''

    # print(docs[0].get_textbox(Rect(486, 19, 522, 30)))
    # print(docs[0].get_textpage(Rect(486, 19, 522, 30)).extractTEXT())

    print(docs[0].get_textbox(Rect(400, 20, 520, 30)))  # CI NBR...ORDER DATE
    print(docs[0].get_textbox(Rect(305, 170, 458, 180)))  # ULTIMATE CONSIGNEE: 6100212675
    print(docs[0].get_textbox(Rect(305, 280, 458, 300)))  # BILL OF LADING  1917867
    print(docs[0].get_textbox(Rect(305, 300, 458, 320)))  # CUSTOMER PO NBR  9500244280
    print(docs[0].get_textbox(Rect(510, 310, 600, 330)))  # NBR CTN     8
    print(docs[0].get_textbox(Rect(510, 350, 600, 370)))  # GI DATE  03/11/2024
    print(docs[0].get_textbox(Rect(450, 380, 520, 430)))  # UNIT PRICE  285.00
    print(docs[0].get_textbox(Rect(50, 450, 200, 490)))  # N25852-N08    COO: Vietnam     QTY: 1,200
    print(docs[0].get_textbox(
        Rect(310, 590, 420, 650)))  # TOTAL WEIGHT GROSS  124.430 LB 56.440 KG NET 93.832 LB 42.561 KG


if __name__ == '__main__':
    pdf_filepath = r'C:\Users\xman\Desktop\invs1\1752808_0811268644_CI_EC.pdf'
    extract_text_from_pdf_by_regions(pdf_filepath)
