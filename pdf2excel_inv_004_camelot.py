from camelot import read_pdf
import camelot

# 读取PDF文件  stream
tables = read_pdf(r'C:\Users\xman\Desktop\invs1\1917867_0811264885_CI_EC.pdf', pages='all', flavor='stream')

for i, table in enumerate(tables):
    # 根据需要，可以选择不同的表单提取策略
    # 'lattice'适用于规则但不一定是完全对齐的表格
    df = table.df
    print(i, df)
    # 如果你知道要提取的具体内容位置，可以通过列名或索引定位
    # 假设你要提取某一列名为'ColumnOfInterest'的内容
    specified_content = df[:]

    # specified_column = df.iloc[:].values.tolist()
    # print(specified_column)


    # 或者根据内容匹配提取
    # 假设你需要提取包含特定字符串'string_to_match'的所有单元格内容
    # matched_rows = df[df.applymap(lambda x: 'string_to_match' in str(x)).any(axis=1)]  ##DataFrame.map
# matched_rows = df[df.map(lambda x: 'SUBTOTAL' in str(x)).any(axis=1)]
# print(matched_rows)
# 将提取出的数据保存或进一步处理
# ...

# 若表格结构复杂，可能需要结合额外逻辑判断和清洗数据

# 输出到CSV或其他格式
# specified_content.to_csv(r'C:\Users\xman\Desktop\invs1\extracted_data.csv', index=True)
# df.to_excel(f'table_{i+1}.xlsx', index=False)
