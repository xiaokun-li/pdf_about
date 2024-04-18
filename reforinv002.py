# _*_ coding:utf-8 _*_

import PyPDF2
import re
import os

samplefile = r'C:\Users\TERRYLI2\Desktop\IntelPLIN2\1752772_0811254742_CI_EC_MIX_COO.pdf'
# samplefile = r'C:\Users\TERRYLI2\Desktop\IntelPLIN2\1917867_0811264885_CI_EC.pdf'

pdfdoc = PyPDF2.PdfReader(samplefile)
pdftext = pdfdoc.pages[0].extract_text()

pdftext2 = pdftext.replace('\n', ' ')
# print(pdftext2)

invoice = re.search(r'\d{8,10}', re.search(r'WAREHOU\s*\d{8,10}\s*', pdftext2).group().strip()).group().strip()
consignee = re.search(r'\d{8,10}', re.search(r'CONSIGNEE:\s*(\d{8,10})\s*', pdftext2).group().strip()).group().strip()
bill_of_loading = re.search(r'\d{6,10}', re.search(r'BILL\s*OF\s*LADING\s*(\d{6,10})\s*', pdftext2).group().strip()).group().strip()
customer_po = re.search(r'\d{8,12}', re.search(r'CUSTOMER\s*PO\s*NBR\s*(\d{8,12})\s*', pdftext2).group().strip()).group().strip()
qty_cartons = float(re.search(r'\d{1,4}', re.search(r'CTN\s*(\d{1,4})\s*', pdftext2).group().strip()).group().strip())
gi_date = re.search(r'\d{2}\/\d{2}\/\d{4}', re.search(r'GI\s*DATE\s*(\d{2}\/\d{2}\/\d{4})\s*', pdftext2).group().strip()).group().strip()
gi_date = gi_date.split('/')
gi_date = gi_date[2] + '-' + gi_date[0] + '-' + gi_date[1]
hp_pn = re.search(r'\b\w{6}-\w{3}\b', pdftext2).group().strip()
coos = [i.strip() for i in re.findall(r'COO:\s*(\w{1,10}\s?\w{0,10})', pdftext2)]
qtys=[float(i.group().strip().split(':')[1].strip().replace(',','')) for i in re.finditer(r'QTY:\s*(\w{0,6},?\w{0,6})*\s*', pdftext2)]
unit_price = float(re.search(r'\d{1,7}\.?\d{0,4}', re.search(r'PC\s*\d{1,7}\.?\d{0,4}', pdftext2).group().strip()).group().strip())
gross_wgt = float(re.search(r'\d{1,7}\.?\d{0,4}\s+KG', re.search(r'GROSS\s+\d{1,7}\.?\d{0,4}\s+LB\s+\d{1,7}\.?\d{0,4}\s+KG', pdftext2).group().strip()).group().strip().split(' ')[0])
net_wgt = float(re.search(r'\d{1,7}\.?\d{0,4}\s+KG', re.search(r'NET\s+\d{1,7}\.?\d{0,4}\s+LB\s+\d{1,7}\.?\d{0,4}\s+KG', pdftext2).group().strip()).group().strip().split(' ')[0])



allext = {        
        "pdf_file_name":        [os.path.basename(samplefile)], 
        "invoice_number":       [invoice],
        "consignee":            [consignee],
        "bill_of_loading":      [bill_of_loading],
        "customer_po":          [customer_po],
        "qty_cartons":          [qty_cartons],
        "gi_date":              [gi_date],
        "hp_pn":                [hp_pn],
        "coo":                  coos,
        "qty":                  qtys,
        "unit_price":           [unit_price],
        "gross_wgt":            [gross_wgt],
        "net_wgt":              [net_wgt]
    }

if len(coos) == 2 and len(qtys) == 2:
    
    allext["pdf_file_name"].append(os.path.basename(samplefile))
    allext["invoice_number"].append(invoice)
    allext["consignee"].append(consignee)
    allext["bill_of_loading"].append(bill_of_loading)
    allext["customer_po"].append(customer_po)
    allext["qty_cartons"].append(qty_cartons)
    allext["gi_date"].append(gi_date)
    allext["hp_pn"].append(hp_pn)
    allext['unit_price'].append(unit_price)
    allext['gross_wgt'].append(gross_wgt)
    allext['gross_wgt'][0] = allext['gross_wgt'][0] / sum(allext['qty']) * allext['qty'][0]
    allext['gross_wgt'][1] = allext['gross_wgt'][1] / sum(allext['qty']) * allext['qty'][1]
    allext['net_wgt'].append(net_wgt)
    allext['net_wgt'][0] = allext['net_wgt'][0] / sum(allext['qty']) * allext['qty'][0]
    allext['net_wgt'][1] = allext['net_wgt'][1] / sum(allext['qty']) * allext['qty'][1]
    
    
for k,v in allext.items():
    print(k,v)