# _*_ coding: utf-8 _*
import fitz  # PyMuPDF


# Get the rects of substrings
def get_dict_of_rects_by_substr(pdf_filepath, target_substr):
    pages = fitz.open(pdf_filepath)
    page = pages[0]  # Process the first page of the PDF file.
    rects_of_substr = {}  # Store the rects of substrings
    blocks = page.search_for(target_substr)  # Use search_for to get a list of blocks object(rects of substrings)

    for block in blocks:  # Process each blocks
        if bool(block):  # If returned block has contents:
            rects_of_substr.setdefault(block, target_substr)

    pages.close()
    return rects_of_substr





if __name__ == '__main__':
    pdf_path = r'C:\Users\xman\Desktop\invs1\1917867_0811264885_CI_EC.pdf'
    targetstr1 = "1917867"
    text = get_dict_of_rects_by_substr(pdf_path, targetstr1)
    for k, v in text.items():
        print(k, v)
