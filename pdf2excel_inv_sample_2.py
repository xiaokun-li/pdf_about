# _*_ coding:utf-8 _*_

# import PyPDF2
# import pandas as pd
# import re
# import os
# import sys
# import time
import fitz
from fitz import Rect

def extract_text_from_pdf_by_regions(pdf_filepath):

    data_dict = {}
    pdffile = pdf_filepath
    docs = fitz.open(pdffile)

    # invoice_number = docs[0].get_textbox(Rect(400, 20, 520, 30))    # CI NBR
    # consignee = docs[0].get_textbox(Rect(305, 170, 458, 180))       # ULTIMATE CONSIGNEE: 6100212675
    # bill_of_lading = docs[0].get_textbox(Rect(305, 280, 458, 300))  # BILL OF LADING  1917867
    # po = docs[0].get_textbox(Rect(305, 300, 458, 320))              # CUSTOMER PO NBR  9500244280
    # carton_number = docs[0].get_textbox(Rect(510, 310, 600, 330))   # NBR CTN     8
    # gi_date = docs[0].get_textbox(Rect(510, 350, 600, 370))         # GI DATE  03/11/2024
    # unit_price = docs[0].get_textbox(Rect(450, 380, 520, 430))      # UNIT PRICE  285.00
    # sku_coo_qty = docs[0].get_textbox(Rect(50, 450, 200, 490))      # N25852-N08    COO: Vietnam     QTY: 1,200
    # gross_net = docs[0].get_textbox(Rect(310, 590, 420, 650))       # TOTAL WEIGHT GROSS  124.430 LB 56.440 KG NET 93.832 LB 42.561 KG

    invoice_number = docs[0].get_textbox(Rect(397, 19, 530, 30))    # CI NBR
    consignee = docs[0].get_textbox(Rect(303, 174, 458, 185))       # ULTIMATE CONSIGNEE: 6100212675
    bill_of_lading = docs[0].get_textbox(Rect(303, 276, 458, 299))  # BILL OF LADING  1917867
    po = docs[0].get_textbox(Rect(303, 301, 458, 325))              # CUSTOMER PO NBR  9500244280
    carton_number = docs[0].get_textbox(Rect(512, 314, 575, 350))   # NBR CTN     8
    gi_date = docs[0].get_textbox(Rect(512, 353, 575, 376))         # GI DATE  03/11/2024
    unit_price = docs[0].get_textbox(Rect(435, 378, 508, 450))      # UNIT PRICE  285.00
    sku_coo_qty = docs[0].get_textbox(Rect(51, 442, 234, 490))      # N25852-N08    COO: Vietnam     QTY: 1,200
    gross_net = docs[0].get_textbox(Rect(311, 599, 422, 669))       # TOTAL WEIGHT GROSS  124.430 LB 56.440 KG NET 93.832 LB 42.561 KG

    data_dict = {
        'invoice_number': invoice_number,
        'consignee': consignee,
        'bill_of_lading': bill_of_lading,
        'po': po,
        'carton_number': carton_number,
        'gi_date': gi_date,
        'unit_price': unit_price,
        'sku_coo_qty': sku_coo_qty,
        'gross_net': gross_net
    }

    for k, v in data_dict.items():
        data_dict[k] = v.replace('\n', '^')

    data_dict['invoice_number'] = data_dict.get("invoice_number")[7:]
    data_dict['consignee'] = data_dict.get("consignee")[20:].split('^')[0]
    data_dict['bill_of_lading'] = data_dict.get("bill_of_lading")[15:]
    data_dict['po'] = data_dict.get("po")[16:]

    cartonqty = ''
    for i in data_dict['carton_number']:
        if i.isdigit():
            cartonqty = cartonqty+i
    data_dict['carton_number'] = cartonqty

    data_dict['gi_date'] = data_dict.get("gi_date")[8:]
    data_dict['unit_price'] = data_dict.get("unit_price").split('^')[1].strip()

    sku = data_dict.get("sku_coo_qty").split('^')[1].strip()
    coo = data_dict.get("sku_coo_qty").split(':')[1].strip().split(' ')[0].strip()
    qty = data_dict.get("sku_coo_qty").split('QTY:')[1]

    data_dict['sku'] = sku
    data_dict['coo'] = coo
    data_dict['qty'] = qty

    data_dict.pop('sku_coo_qty')

    gross = data_dict.get("gross_net").split('KG')[0].split('LB')[1].replace('^', '').strip()
    data_dict['gross'] = gross
    net = data_dict.get("gross_net").split('KG')[1].split('LB')[1].replace('^', '').strip()
    data_dict['net'] = net

    data_dict.pop('gross_net')

    return data_dict

if __name__ == '__main__':
    pdf_filepath = r'C:\Users\xman\Desktop\invs1\1917867_0811264894_CI_EC.pdf'
    for k, v in extract_text_from_pdf_by_regions(pdf_filepath).items():
        print(k+" : "+v)
