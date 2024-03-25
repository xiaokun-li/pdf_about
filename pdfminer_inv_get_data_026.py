from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from io import StringIO


def search_value_in_pdf(pdf_path, search_value):
    positions = []
    resource_manager = PDFResourceManager()
    fake_file_handle = StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,caching=True,check_extractable=True):
            page_interpreter.process_page(page)
            text = fake_file_handle.getvalue()
            #print(page.doc)  # <pdfminer.pdfdocument.PDFDocument object at 0x000001784DF5EB70>
            #print(page.annots)  #PDFObjRef:13
            #print(page.attrs)   #Annots': [<PDFObjRef:13>,
            #print(page.beads)   #None

            #print(page.contents) #<PDFStream(40): len=10800, {'Filter': /'FlateDecode', 'Length': 3543}>]
            #print(page.cropbox) # [0, 0, 609, 791]
            #print(page.INHERITABLE_ATTRS) #{'Rotate', 'CropBox', 'Resources', 'MediaBox'}
            #print(page.lastmod) #None
            #print(page.mediabox) #[0, 0, 609, 791]
            #print(page.pageid) #9
            #print(page.resources) #{'ExtGState': {'GS0': <PDFObjRef:41>}, 'Font': {'F0': <PDFObjRef:42>, 'F1': <PDFObjRef:43>, 'F2': <PDFObjRef:44>, 'F3': <PDFObjRef:45>}, 'XObject': {'Im0': <PDFObjRef:46>}}
            #print(page.rotate) #0



            # 在页面文本中搜索值
            start_idx = text.find(search_value)
            # print(start_idx)

            while start_idx != -1:
                # 这里只是简单记录文本位置，并没有与页面中的具体布局信息关联
                # 要获取精确位置，需要分析PDF页面的布局对象
                positions.append((page, start_idx, start_idx + len(search_value)))

                # 继续搜索下一个匹配项（如果有的话）
                start_idx = text.find(search_value, start_idx + len(search_value))

                # 关闭并重置文本转换器
            fake_file_handle.seek(0)
            fake_file_handle.truncate()

    converter.close()
    return positions


# 使用函数搜索值
pdf_path = r'C:\Users\ggg\Desktop\invs\0811235374_CI.pdf'
search_value = "811235374"
positions = search_value_in_pdf(pdf_path, search_value)
for pos in positions:
    print(f"找到 '{search_value}' 在页面 {pos[0]} 的位置 {pos[1]} 到 {pos[2]}（基于文本字符串的索引）")
    print(pos)