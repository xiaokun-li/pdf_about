# _*_ coding:utf-8 _*_
import PyPDF2

pdffile = r'C:\Users\xman\Desktop\invs1\1917867_0811264885_CI_EC.pdf'

pdf = PyPDF2.PdfReader(open(pdffile, 'rb'))
page = pdf.pages[0]
text = page.extract_text()

print(text)
