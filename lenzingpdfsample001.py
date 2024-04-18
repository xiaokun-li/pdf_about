# _*_ coding:utf-8 _*_

import PyPDF2

pdf_filepath = r'C:\Users\TERRYLI2\Desktop\IntelPLIN2\Lenzingpodsample001.pdf'
pdfdocs = PyPDF2.PdfReader(pdf_filepath)
pdftext = ''

for pdfdoc in pdfdocs.pages:
    pdftext += pdfdoc.extract_text()

print(pdftext)