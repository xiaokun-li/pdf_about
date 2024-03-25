import camelot
import pandas as pd

# 指定PDF文件路径
pdf_path = r'C:\Users\ggg\Desktop\invs\0811235374_CI.pdf'

tables = camelot.read_pdf(pdf_path, pages='1', flavor='stream')

# 获取第一个表格的DataFrame
df = tables[0].df

# 打印表格内容
print(df)