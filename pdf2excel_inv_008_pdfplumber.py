import pdfplumber

file_path = r'C:\Users\xman\Desktop\invs1\1917867_0811264885_CI_EC.pdf'

pdf = pdfplumber.open(file_path)
# print(pdf.pages)
# print(pdf.pages[0])
# print(pdf.pages[0].extract_text())

# for i in range(0, len(pdf.pages)):
    # page = pdf.pages[i]
    # print(page.extract_text())



# pdfplumber.open -> pdf object.
# pdf.pages -> the object which inherited from list.
# pdf.pages[0] -> the first page of the pdf file.
# pdf.pages[0].extract_text()
# pdf.pages[0].extract_table()
# pdf.pages[0].extract_tables()


for page in pdf.pages:
    table = page.extract_tables() # But this method can not retrieve all data!!!
    for rows in table:
        for row in rows:
            print(row)

#     text = page.extract_text() # this method can retrieve all data.
#     print(text)
