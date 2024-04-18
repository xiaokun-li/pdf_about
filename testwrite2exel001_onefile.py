#  _*_ coding:utf-8 _*_

import os
from write2exceltest3 import *

if __name__ == '__main__':
    
    targetdirectory = r'C:\Users\TERRYLI2\Desktop\IntelPLIN2'
    fileslist = [filename for filename in os.listdir(targetdirectory) if filename.lower().endswith('.pdf') and (not PDFExtractor.check_filename_for_done(filename))] 
    newpdfspath=[]
   
    allext = {        
            "pdf_file_name":        [], 
            "invoice_number":       [],
            "consignee":            [],
            "bill_of_loading":      [],
            "customer_po":          [],
            "qty_cartons":          [],
            "gi_date":              [],
            "hp_pn":                [],
            "coo":                  [],
            "qty":                  [],
            "unit_price":           [],
            "gross_wgt":            [],
            "net_wgt":              []
        }
    
    for i in fileslist:
        os.path.join(targetdirectory,i)
        ext = COOIntelInvoicePDFExtractor(os.path.join(targetdirectory,i))
        # ext.stamp_data_on_pdf()
        vv = ext.extract_text_from_pdf_by_regions()
        #print(vv)
        
        for j in range(ext.coo_count):
            allext['pdf_file_name'].append(i)
            
        allext['invoice_number'].extend(vv['invoice_number'])
        allext['consignee'].extend(vv['consignee'])
        allext['bill_of_loading'].extend(vv['bill_of_lading'])
        allext['customer_po'].extend(vv['po'])
        allext['qty_cartons'].extend(vv['carton_number'])
        allext['gi_date'].extend(vv['gi_date'])
        allext['hp_pn'].extend(vv['sku'])
        allext['coo'].extend(vv['coo'])
        allext['qty'].extend(vv['qty'])
        allext['unit_price'].extend(vv['unit_price'])
        allext['gross_wgt'].extend(vv['gross'])
        allext['net_wgt'].extend(vv['net'])
        
        # ext.export_excel_from_pdf(vv)
        ext.close()

    
    # print(len(allext['pdf_file_name']))
    # print(len(allext['invoice_number']))
    # print(len(allext['consignee']))
    # print(len(allext['bill_of_loading']))
    # print(len(allext['customer_po']))
    # print(len(allext['qty_cartons']))
    # print(len(allext['gi_date']))
    # print(len(allext['hp_pn']))
    # print(len(allext['coo']))
    # print(len(allext['qty']))
    # print(len(allext['unit_price']))
    # print(len(allext['gross_wgt']))
    # print(len(allext['net_wgt']))

    df = pd.DataFrame(allext)
    ddatetime = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime())
    #print(ddatetime)
    df.to_excel(r'C:\Users\TERRYLI2\Desktop\IntelPLIN2\\' + f'IntelINV{ddatetime}.xlsx', index=False, engine='openpyxl')
    # update_filename(pdf_path_filename)
    print("PDF content has been extracted and saved to one Excel file~")
    
    
    
    

