# _*_ coding:utf-8 _*_

import PyPDF2
import pandas as pd
import re
import os
import sys
import time
import fitz
from fitz import Rect


class PDFExtractor(object):
    
    @classmethod
    def check_filename_for_done(cls, filename):
        if 'Done' in filename:
            return True
        else:
            return False
    
    def __init__(self, pdf_filepath ,obj_list=list(), obj_dict=dict()):
        self._pdf_filepath = pdf_filepath
        self._objective_list = obj_list
        self._objective_data_items = obj_dict
        self._pdf_obj = fitz.open(self._pdf_filepath)
        self._pages = self.get_pages()
        
        
    def get_pages(self):
        pages=[]
        for i in range(self._pdf_obj.page_count):
            pages.append(self._pdf_obj[i])
        return pages


    def stamp_data_on_pdf(self, data_dict):
        for k,v in data_dict.items():
            for page in self._pages:
                page.add_rect_annot(v)
                # page.add_redact_annot(v)
                # page.add_circle_annot(v)
                # page.add_highlight_annot(v)
                # page.add_squiggly_annot(v)
                # page.add_stamp_annot(v)
                # page.add_strikeout_annot(v)
                # page.add_underline_annot(v)
        self._pdf_obj.save(self._pdf_filepath.replace('.pdf', '_Done.pdf'))
        print("PDF content has been signed and saved to new PDF file~")
        #self._pdf_obj.close()


    def extract_text_from_pdf_by_regions(self, rects):
        pass


    def export_excel_from_pdf(self, data_dict_filtered):
        pass


class InvoicePDFExtractor(PDFExtractor):
    pass


class IntelInvoicePDFExtractor(InvoicePDFExtractor):
    pass


class COOIntelInvoicePDFExtractor(IntelInvoicePDFExtractor):
    
    def __init__(self, pdf_filepath, obj_list=list(), obj_dict=dict()):
        super().__init__(pdf_filepath, obj_list, obj_dict)
        self.coo_count = 0

    intel_invoice_1coo_data_rects = {
        'invoice_number':   Rect(397, 19, 530, 30),
        'consignee':        Rect(303, 174, 458, 185),
        'bill_of_lading':   Rect(303, 276, 458, 299),
        'po':               Rect(303, 301, 458, 325),
        'carton_number':    Rect(512, 314, 575, 350),
        'gi_date':          Rect(512, 353, 575, 376),
        'unit_price':       Rect(435, 378, 508, 450),
        'sku_coo_qty':      Rect(51, 442, 234, 490),
        'gross_net':        Rect(311, 599, 422, 669)
    }
    
    
    def extract_text_from_pdf_by_regions(self, rects=intel_invoice_1coo_data_rects):
           
        r_invoice_number = self._pages[0].get_textbox(rects.get("invoice_number"))    # CI NBR
        r_consignee = self._pages[0].get_textbox(rects.get("consignee"))       # ULTIMATE CONSIGNEE: 6100212675
        r_bill_of_lading = self._pages[0].get_textbox(rects.get("bill_of_lading"))  # BILL OF LADING  1917867
        r_po = self._pages[0].get_textbox(rects.get("po"))              # CUSTOMER PO NBR  9500244280
        r_carton_number = self._pages[0].get_textbox(rects.get("carton_number"))   # NBR CTN     8
        r_gi_date = self._pages[0].get_textbox(rects.get("gi_date"))         # GI DATE  03/11/2024
        r_unit_price = self._pages[0].get_textbox(rects.get("unit_price"))      # UNIT PRICE  285.00
        r_sku_coo_qty = self._pages[0].get_textbox(rects.get("sku_coo_qty"))      # N25852-N08    COO: Vietnam     QTY: 1,200
        r_gross_net = self._pages[0].get_textbox(rects.get("gross_net"))       # TOTAL WEIGHT GROSS  124.430 LB 56.440 KG NET 93.832 LB 42.561 KG

        data_dict = {
            'invoice_number': r_invoice_number,
            'consignee': r_consignee,
            'bill_of_lading': r_bill_of_lading,
            'po': r_po,
            'carton_number': r_carton_number,
            'gi_date': r_gi_date,
            'unit_price': r_unit_price,
            'sku_coo_qty': r_sku_coo_qty,
            'gross_net': r_gross_net
        }

        for k, v in data_dict.items():
            data_dict[k] = v.replace('\n', '^')

        data_dict['invoice_number'] = [data_dict.get("invoice_number")[7:],]
        data_dict['consignee'] = [data_dict.get("consignee")[20:].split('^')[0],]
        data_dict['bill_of_lading'] = [data_dict.get("bill_of_lading")[15:],]
        data_dict['po'] = [data_dict.get("po")[16:],]

        cartonqty = ''
        for i in data_dict['carton_number']:
            if i.isdigit():
                cartonqty = cartonqty+i
                
        data_dict['carton_number'] = [float(cartonqty.replace(',', '').strip()),]

        data_dict['gi_date'] = data_dict.get("gi_date")[8:].split('/')
        data_dict['gi_date'] = [data_dict['gi_date'][2] + '-' + data_dict['gi_date'][0] + '-' + data_dict['gi_date'][1],]
        data_dict['unit_price'] = data_dict.get("unit_price").split('^')[1].strip()
        data_dict['unit_price'] = [float(data_dict['unit_price'].replace(',', '').strip()),]

        gross = data_dict.get("gross_net").split('KG')[0].split('LB')[1].replace('^', '').strip()
        data_dict['gross'] = [float(gross.replace(',', '').strip()),]
        net = data_dict.get("gross_net").split('KG')[1].split('LB')[1].replace('^', '').strip()
        data_dict['net'] = [float(net.replace(',', '').strip()),]

        sku_coo_qty_str = data_dict.get("sku_coo_qty")
        self.coo_count = sku_coo_qty_str.count('COO')
        
        if self.coo_count==1:
            sku = data_dict.get("sku_coo_qty").split('^')[1].strip()
            coo = data_dict.get("sku_coo_qty").split(':')[1].strip().split(' ')[0].strip()
            qty = data_dict.get("sku_coo_qty").split('QTY:')[1]

            data_dict['sku'] = [sku,]
            data_dict['coo'] = [coo,]
            data_dict['qty'] = [float(qty.replace(',', '').strip()),]
            
        elif self.coo_count==2:
            # print(sku_coo_qty_str)
            sku = data_dict.get("sku_coo_qty").split('^')[2].strip()
            data_dict['sku']= [sku,sku]
            coo1 = coo = data_dict.get("sku_coo_qty").split(':')[1].strip().split(' ')[0].strip() 
            qty1 = data_dict.get("sku_coo_qty").split('QTY:')[1].strip().split(' ')[0]
            coo2 = data_dict.get("sku_coo_qty").split(':')[3].strip().rsplit(' ',2)[0].strip()
            qty2 = data_dict.get("sku_coo_qty").split(':')[4].strip()
            # print(qty2)
            data_dict['coo']=[coo1,coo2]
            data_dict['qty']=[float(qty1.replace(',', '').strip()), float(qty2.replace(',', '').strip())]   
            
            data_dict['invoice_number'].append(data_dict.get("invoice_number")[0])
            data_dict['consignee'].append(data_dict.get("consignee")[0])
            data_dict['bill_of_lading'].append(data_dict.get("bill_of_lading")[0])
            data_dict['po'].append(data_dict.get("po")[0])           
            data_dict['carton_number'].append(data_dict.get("carton_number")[0])
            data_dict['gi_date'].append(data_dict.get("gi_date")[0])
            data_dict['unit_price'].append(data_dict.get("unit_price")[0])
            
            ttgross=data_dict['gross'][0]
            ttnet = data_dict['net'][0]
            data_dict['gross'][0]=ttgross/(data_dict['qty'][0]+data_dict['qty'][1])*data_dict['qty'][0]
            data_dict['gross'].append(ttgross/(data_dict['qty'][0]+data_dict['qty'][1])*data_dict['qty'][1])
            data_dict['net'][0]=ttnet/(data_dict['qty'][0]+data_dict['qty'][1])*data_dict['qty'][0] 
            data_dict['net'].append(ttnet/(data_dict['qty'][0]+data_dict['qty'][1])*data_dict['qty'][1])
            

        data_dict.pop('sku_coo_qty')
        data_dict.pop('gross_net')  
              
        return data_dict
    
    
    def export_excel_from_pdf(self, data_dict_filtered):
            
        pathname = os.path.dirname(self._pdf_filepath)
        filename = os.path.basename(self._pdf_filepath)
        
        filenames = []
        if check_for_done(filename):
            sys.exit()
        
        rows = len(data_dict_filtered.get('invoice_number'))
        for i in range(rows):
           filenames.append(filename)
                
                
        export_data_item = {
            "pdf_file_name":        filename, 
            "invoice_number":       data_dict_filtered.get("invoice_number"),
            "consignee":            data_dict_filtered.get("consignee"),
            "bill_of_loading":      data_dict_filtered.get('bill_of_lading'),
            "customer_po":          data_dict_filtered.get('po'),
            "qty_cartons":          data_dict_filtered.get('carton_number'),
            "gi_date":              data_dict_filtered.get('gi_date'),
            "hp_pn":                data_dict_filtered.get('sku'),
            "coo":                  data_dict_filtered.get('coo'),
            "qty":                  data_dict_filtered.get('qty'),
            "unit_price":           data_dict_filtered.get('unit_price'),
            "gross_wgt":            data_dict_filtered.get('gross'),
            "net_wgt":              data_dict_filtered.get('net')
        }

        # print(extract_data)
        df = pd.DataFrame(export_data_item)
        df.to_excel(pathname + '\\' + filename.split('.')[0] + '.xlsx', index=False, engine='openpyxl')
        # update_filename(pdf_path_filename)
        print("PDF content has been extracted and saved to Excel file~")

    
    def close(self):
        self._pdf_obj.close()
    
    
    def stamp_data_on_pdf(self, data_dict = intel_invoice_1coo_data_rects):
        # return IntelInvoicePDFExtractor.stamp_data_on_pdf(self, data_dict)
        return super().stamp_data_on_pdf(data_dict)
    
    
    
    def extract_data_from_pdf_by_re(self):

        pdfdoc = PyPDF2.PdfReader(self._pdf_filepath)
        pdftext = pdfdoc.pages[0].extract_text()
        pdftext2 = pdftext.replace('\n', ' ')

        invoice = re.search(r'\d{8,10}', re.search(r'WAREHOU\s*\d{8,10}\s*', pdftext2).group().strip()).group().strip()
        consignee = re.search(r'\d{8,10}', re.search(r'CONSIGNEE:\s*(\d{8,10})\s*', pdftext2).group().strip()).group().strip()
        bill_of_lading = re.search(r'\d{6,10}', re.search(r'BILL\s*OF\s*LADING\s*(\d{6,10})\s*', pdftext2).group().strip()).group().strip()
        po = re.search(r'\d{8,12}', re.search(r'CUSTOMER\s*PO\s*NBR\s*(\d{8,12})\s*', pdftext2).group().strip()).group().strip()
        carton_number = float(re.search(r'\d{1,4}', re.search(r'CTN\s*(\d{1,4})\s*', pdftext2).group().strip()).group().strip())
        gi_date = re.search(r'\d{2}\/\d{2}\/\d{4}', re.search(r'GI\s*DATE\s*(\d{2}\/\d{2}\/\d{4})\s*', pdftext2).group().strip()).group().strip()
        gi_date = gi_date.split('/')
        gi_date = gi_date[2] + '-' + gi_date[0] + '-' + gi_date[1]
        sku = re.search(r'\b\w{6}-\w{3}\b', pdftext2).group().strip()
        # coos = re.findall(r'COO:\s*(\w{1,10})\s*', pdftext2)
        coos = [i.strip() for i in re.findall(r'COO:\s*(\w{1,10}\s?\w{0,10})', pdftext2)]
        qtys=[float(i.group().strip().split(':')[1].strip().replace(',','')) for i in re.finditer(r'QTY:\s*(\w{0,6},?\w{0,6})*\s*', pdftext2)]
        unit_price = float(re.search(r'\d{1,7}\.?\d{0,4}', re.search(r'PC\s*\d{1,7}\.?\d{0,4}', pdftext2).group().strip()).group().strip())
        gross = float(re.search(r'\d{1,7}\.?\d{0,4}\s+KG', re.search(r'GROSS\s+\d{1,7}\.?\d{0,4}\s+LB\s+\d{1,7}\.?\d{0,4}\s+KG', pdftext2).group().strip()).group().strip().split(' ')[0])
        net = float(re.search(r'\d{1,7}\.?\d{0,4}\s+KG', re.search(r'NET\s+\d{1,7}\.?\d{0,4}\s+LB\s+\d{1,7}\.?\d{0,4}\s+KG', pdftext2).group().strip()).group().strip().split(' ')[0])

        allext = {        
                "pdf_file_name":        [os.path.basename(self._pdf_filepath)], 
                "invoice_number":       [invoice],
                "consignee":            [consignee],
                "bill_of_lading":       [bill_of_lading],
                "po":                   [po],
                "carton_number":          [carton_number],
                "gi_date":              [gi_date],
                "sku":                [sku],
                "coo":                  coos,
                "qty":                  qtys,
                "unit_price":           [unit_price],
                "gross":            [gross],
                "net":              [net]
            }

        if len(coos) == 2 and len(qtys) == 2:
            
            allext["pdf_file_name"].append(os.path.basename(self._pdf_filepath))
            allext["invoice_number"].append(invoice)
            allext["consignee"].append(consignee)
            allext["bill_of_lading"].append(bill_of_lading)
            allext["po"].append(po)
            allext["carton_number"].append(carton_number)
            allext["gi_date"].append(gi_date)
            allext["sku"].append(sku)
            allext['unit_price'].append(unit_price)
            allext['gross'].append(gross)
            allext['gross'][0] = allext['gross'][0] / sum(allext['qty']) * allext['qty'][0]
            allext['gross'][1] = allext['gross'][1] / sum(allext['qty']) * allext['qty'][1]
            allext['net'].append(net)
            allext['net'][0] = allext['net'][0] / sum(allext['qty']) * allext['qty'][0]
            allext['net'][1] = allext['net'][1] / sum(allext['qty']) * allext['qty'][1]
            
            
        return allext
    
    

# Others


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


if __name__ == '__main__':
    pdf_filepath = r'C:\Users\TERRYLI2\Desktop\IntelPLIN\1917867_0811264885_CI_EC.pdf'  
    dd = extract_text_from_pdf_by_regions(pdf_filepath)
    get_excel_from_pdf_001(pdf_filepath, dd)
   
