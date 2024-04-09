import fitz

def draw_red_rectangle_on_pdf(page_num, _rect, pdf_path, output_path):
  
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    page.add_rect_annot(_rect)
    doc.save(output_path)
    doc.close()

pdf_path = r'C:\Users\ggg\Desktop\invs2\1917867_0811264885_CI_EC.pdf'  
output_path = r'C:\Users\ggg\Desktop\invs2\1917867_0811264885_CI_EC2.pdf'  
page_num = 0 
x0 = 200  
y0 = 200  
x1 = 300  
y1 = 300 

rect = fitz.Rect(x0, y0, x1, y1)
draw_red_rectangle_on_pdf(page_num, rect, pdf_path, output_path)