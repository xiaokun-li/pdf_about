# _*_ coding: utf-8 _*_

# import tabula 
# pdf_filepath = "1917867_0811264885_CI_EC.pdf"
# table = tabula.read_pdf(pdf_filepath)
# print(type(table[0]))

import fitz
from fitz import Rect

# invoice_number = docs[0].get_textbox(Rect(400, 20, 520, 30))    # CI NBR
# consignee = docs[0].get_textbox(Rect(305, 170, 458, 180))       # ULTIMATE CONSIGNEE: 6100212675
# bill_of_lading = docs[0].get_textbox(Rect(305, 280, 458, 300))  # BILL OF LADING  1917867
# po = docs[0].get_textbox(Rect(305, 300, 458, 320))              # CUSTOMER PO NBR  9500244280
# carton_number = docs[0].get_textbox(Rect(510, 310, 600, 330))   # NBR CTN     8
# gi_date = docs[0].get_textbox(Rect(510, 350, 600, 370))         # GI DATE  03/11/2024
# unit_price = docs[0].get_textbox(Rect(450, 380, 520, 430))      # UNIT PRICE  285.00
# sku_coo_qty = docs[0].get_textbox(Rect(50, 450, 200, 490))      # N25852-N08    COO: Vietnam     QTY: 1,200
# gross_net = docs[0].get_textbox(Rect(310, 590, 420, 650))       # TOTAL WEIGHT GROSS  124.430 LB 56.440 KG NET 93.832 LB 42.561 KG

data_dict = {
    'invoice_number':   Rect(397, 19, 530, 30),
    'consignee':        Rect(303, 174, 458, 185),
    'bill_of_lading':   Rect(303, 276, 458, 299),
    'po':               Rect(303, 301, 458, 325),
    'carton_number':    Rect(512, 314, 575, 350),
    'gi_date':          Rect(512, 353, 575, 376),
    'unit_price':       Rect(435, 378, 508, 450),
    'sku_coo_qty':      Rect(51, 442, 234, 490),
    'gross_net':        Rect(311, 599, 422, 669)
}


def draw_red_rectangle_on_pdf(page_num, _rect):
    page = doc[page_num]
    page.add_rect_annot(_rect)


pdf_path = r'C:\Users\xman\Desktop\invs1\1917867_0811264894_CI_EC.pdf'  
output_path = r'C:\Users\xman\Desktop\invs1\1917867_0811264894_CI_EC_2.pdf'  
page_num = 0 
x0 = 200  
y0 = 200  
x1 = 300  
y1 = 300 

doc = fitz.open(pdf_path)

for k,v in data_dict.items():
    draw_red_rectangle_on_pdf(0, v)

doc.save(output_path)
doc.close()