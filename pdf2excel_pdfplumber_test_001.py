import pdfplumber
import pandas as pd

# 打开PDF文件
with pdfplumber.open(r'C:\Users\ggg\Desktop\invs\0811235374_CI.pdf') as pdf:
    # 遍历每一页
    for i, page in enumerate(pdf.pages):
        # 提取当前页的所有表格
        tables = page.extract_tables()

        # 遍历当前页的每个表格
        for table in tables:
            # 将表格内容转换为DataFrame
            df = pd.DataFrame(table[:], columns=table[0])

            # 打印或处理DataFrame
            print(f"Page {i + 1} Table:")
            print(df)
            print("\n")

            # 如果你需要将数据保存到CSV文件
            # df.to_csv(f'page_{i+1}_table.csv', index=False)