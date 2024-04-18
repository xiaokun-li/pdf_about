# _*_ coding:utf-8 _*_

import PyPDF2
import re
import os

samplefile = r'C:\Users\TERRYLI2\Desktop\IntelPLIN2\1752772_0811254742_CI_EC_MIX_COO.pdf'
# samplefile = r'C:\Users\TERRYLI2\Desktop\IntelPLIN2\1917867_0811264885_CI_EC.pdf'

pdfdoc = PyPDF2.PdfReader(samplefile)
pdftext = pdfdoc.pages[0].extract_text()

pdftext2 = pdftext.replace('\n', ' ')
print(pdftext2)

invoice = re.search(r'\d{8,10}', re.search(r'WAREHOU\s*\d{8,10}\s*', pdftext2).group().strip()).group().strip()
# print(invoice)
consignee = re.search(r'\d{8,10}', re.search(r'CONSIGNEE:\s*(\d{8,10})\s*', pdftext2).group().strip()).group().strip()
# print(consignee)
bill_of_loading = re.search(r'\d{6,10}', re.search(r'BILL\s*OF\s*LADING\s*(\d{6,10})\s*', pdftext2).group().strip()).group().strip()
# print(bill_of_loading)
customer_po = re.search(r'\d{8,12}', re.search(r'CUSTOMER\s*PO\s*NBR\s*(\d{8,12})\s*', pdftext2).group().strip()).group().strip()
# print(customer_po)
qty_cartons = re.search(r'\d{1,4}', re.search(r'CTN\s*(\d{1,4})\s*', pdftext2).group().strip()).group().strip()
# print(qty_cartons)
gi_date = re.search(r'\d{2}\/\d{2}\/\d{4}', re.search(r'GI\s*DATE\s*(\d{2}\/\d{2}\/\d{4})\s*', pdftext2).group().strip()).group().strip()
# print(gi_date)
hp_pn = re.search(r'\b\w{6}-\w{3}\b', pdftext2).group().strip()
# print(hp_pn)
coo = re.search(r'\s+\w{1,10}', re.search(r'COO:\s*(\w{1,10})\s*', pdftext2).group().strip()).group().strip()
# print(coo)
qty = re.search(r'QTY:\s*(\d{0,7},?\d{0,7})*\s*', re.search(r'COO:\s*(\w{1,10})\s*QTY:\s*(\d{0,7},?\d{0,7})*\s*', pdftext2).group().strip()).group().strip()
qty=qty.split(':')[1].strip()
#print(qty)
unit_price = re.search(r'\d{1,7}\.?\d{0,4}', re.search(r'PC\s*\d{1,7}\.?\d{0,4}', pdftext2).group().strip()).group().strip()
# print(unit_price)
gross_wgt = re.search(r'\d{1,7}\.?\d{0,4}\s+KG', re.search(r'GROSS\s+\d{1,7}\.?\d{0,4}\s+LB\s+\d{1,7}\.?\d{0,4}\s+KG', pdftext2).group().strip()).group().strip()
gross_wgt = gross_wgt.split(' ')[0]
# print(gross_wgt)
net_wgt = re.search(r'\d{1,7}\.?\d{0,4}\s+KG', re.search(r'NET\s+\d{1,7}\.?\d{0,4}\s+LB\s+\d{1,7}\.?\d{0,4}\s+KG', pdftext2).group().strip()).group().strip()
net_wgt = net_wgt.split(' ')[0]
# print(net_wgt)

allext = {        
        "pdf_file_name":        [os.path.basename(samplefile)], 
        "invoice_number":       [invoice],
        "consignee":            [consignee],
        "bill_of_loading":      [bill_of_loading],
        "customer_po":          [customer_po],
        "qty_cartons":          [qty_cartons],
        "gi_date":              [gi_date],
        "hp_pn":                [hp_pn],
        "coo":                  [coo],
        "qty":                  [qty],
        "unit_price":           [unit_price],
        "gross_wgt":            [gross_wgt],
        "net_wgt":              [net_wgt]
    }



for k,v in allext.items():
    print(k,v)