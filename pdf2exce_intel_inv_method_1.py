import PyPDF2
import pandas as pd
import re
import os
import sys


def has_invoice_digits(s):
    pattern = re.compile(r'\d{8,10}')
    match = pattern.search(s)
    return bool(match)


def get_invoice_digits(s):
    pattern = re.compile(r'\d{8,10}')
    match = pattern.search(s)
    if bool(match):
        return match.group()
    else:
        return ""


def check_for_done(filename):
    if 'Done' in filename:
        return True
    else:
        return False


def update_filename(file_pathname):
    directory = os.path.dirname(file_pathname)
    filename = os.path.basename(file_pathname)
    new_file_name = filename.split('.')[0] + '_done.' + filename.split('.')[1]
    new_file_path = os.path.join(directory, new_file_name)

    try:
        os.rename(file_pathname, new_file_path)
        print(f"File renamed successfully from {filename} to {new_file_name}")
    except OSError as e:
        print(f"Error: {e.strerror}")


def get_excel_from_pdf_001(pdf_path_filename):
    pathname = os.path.dirname(pdf_path_filename)
    filename = os.path.basename(pdf_path_filename)

    if check_for_done(filename):
        sys.exit()

    # 打开PDF文件
    pdf_file_obj = open(pdf_path_filename, 'rb')
    #  pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj) # DeprecationWarning
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)  # DeprecationWarning

    # 初始化一个列表来保存提取的文本
    extracted_text = []

    # 遍历PDF的每一页
    #  for page_num in range(pdf_reader.numPages):  ## DeprecationWarning
    for page_num in range(len(pdf_reader.pages)):
        #  page_obj = pdf_reader.getPage(page_num) ## DeprecationWarning
        page_obj = pdf_reader.pages[page_num]
        # text = page_obj.extractText()  ## DeprecationWarning
        text = page_obj.extract_text()
        if text:
            extracted_text.append(text)

        # 关闭PDF文件
    pdf_file_obj.close()

    textlist = []
    analysis_text = []
    #  print(extracted_text[0].count('\n'))
    all_text = extracted_text[0].replace('\n', '^^')
    aa = all_text.split('^^')

    #  print(len(aa))
    for ss in aa:
        analysis_text.append(ss.strip())
    #    print(ss.strip())

    # [print(analysis_text[i]) for i in range(0, len(analysis_text)) if
    # (i == 3 or i == 23 or i == 32 or i == 34 or i == 39 or i == 40 or i == 41 or i == 49 or i == 50 or i == 53)]

    invoice_number = get_invoice_digits(analysis_text[3])
    consignee = analysis_text[23].strip()[-1:-11:-1][::-1]
    bill_of_loading = analysis_text[32].strip()
    customer_po = analysis_text[34].strip()[:10]
    qty_cartons = analysis_text[39].strip()
    gi_date = analysis_text[41].strip()
    hp_pn = analysis_text[49].strip()
    coo = analysis_text[50].strip().split(r'COO:')[1][:8:].strip()
    qty = analysis_text[50].strip().split(r'QTY:')[1][:11:].strip()
    unit_price = analysis_text[53].strip()[2::].strip()
    gross_wgt = analysis_text[63].split(' ')[0].strip()
    net_wgt = analysis_text[65].split(' ')[0].strip()

    extract_data = {
        "invoice_number": [invoice_number],
        "consignee": [consignee],
        "bill_of_loading": [bill_of_loading],
        "customer_po": [customer_po],
        "qty_cartons": [qty_cartons],
        "gi_date": [gi_date],
        "hp_pn": [hp_pn],
        "coo": [coo],
        "qty": [qty],
        "unit_price": [unit_price],
        "gross_wgt": [gross_wgt],
        "net_wgt": [net_wgt]
    }
    # xfact = 0.4535921
    # print(net_wgt)

    df = pd.DataFrame(extract_data)

    # 将DataFrame保存到Excel文件
    # df.to_excel(r'C:\Users\ggg\Desktop\invs\0811235374_CI_PDF2EXC.xlsx', index=False)

    df.to_excel(pathname + '\\' + filename.split('.')[0] + '.xlsx', index=False, engine='openpyxl')

    update_filename(pdf_path_filename)

    print("PDF content has been extracted and saved to Excel file.")


if __name__ == '__main__':
    targetdirectory = r'C:\Users\ggg\Desktop\invs2'
    get_excel_from_pdf_001(os.path.join(targetdirectory, '1917867_0811264902_CI_EC.pdf'))
