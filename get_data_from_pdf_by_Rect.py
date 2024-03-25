# _*_ coding:utf-8 _*_
import fitz

filepath = r'C:\Users\ggg\Desktop\invs\0811235374_CI.pdf'


def extract_text_from_region(pdf_path, rect1):
    doc = fitz.open(pdf_path)
    page = doc[0]  # 假设我们只对第一页感兴趣
    text1 = page.get_textbox(rect1)
    doc.close()
    return text1


rect = (485, 20, 609, 20)  # 811235374   # 这应该是左上角点位，和右下角点位吧？
text = extract_text_from_region(filepath, rect)
print(text)
