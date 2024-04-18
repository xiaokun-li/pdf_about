#  _*_ coding:utf-8 _*_

import os
from write2exceltest3 import *

if __name__ == '__main__':
    
    targetdirectory = r'C:\Users\TERRYLI2\Desktop\IntelPLIN2'
    fileslist = [filename for filename in os.listdir(targetdirectory) if filename.lower().endswith('.pdf') and (not PDFExtractor.check_filename_for_done(filename))] 
    
    # newpdfspath=[]
    
    for i in fileslist:
        os.path.join(targetdirectory,i)
        ext = COOIntelInvoicePDFExtractor(os.path.join(targetdirectory,i))
        # ext.stamp_data_on_pdf()
        # ext.export_excel_from_pdf(ext.extract_text_from_pdf_by_regions())
        ext.export_excel_from_pdf(ext.extract_data_from_pdf_by_re())   
        ext.close()


