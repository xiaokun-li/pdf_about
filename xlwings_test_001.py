# _*_ coding:utf-8 _*_

import xlwings as xw

app = xw.App(visible=False, add_book=None)

for i in range(1, 11):
    workbook = app.books.add()
    workbook.save(f"c:\\users\\ggg\\desktop\\kkk{i}.xlsx")
    workbook.close()

app.quit()


