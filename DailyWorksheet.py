from colorama import Style
import pdfplumber,os,re
from os import path
from fpdf import FPDF
#shopnames=['KHAMIS-137','JIZAN-139','ABHA-140','RAVALA-137','KHAMIS-164']
defaultPrintData={23:'Cabbage-white',27:'Banger',80:'Regla',88:'Mulukhia',158:'Cauliflower',169:'Lettuce-Chinese',192:'Cabbage-Red',194:'Brocoli',214:'Celery',245:'Lettuce-round',389:'Broccoli',522:'Lettuce',648:'Parsely',649:'Coriander',650:'Mint',651:'Spinach',652:'Dill',653:'Habak',654:'Gerger',655:'Leeks',656:'Onion-Green',657:'Red-Turnip',658:'White-Turnip',659:'Silk',959:'Lettuce-Round',667:'PineApple'}
#skuDictionary={23:0,27:0,80:0,88:0,158:0,169:0,192:0,214:0,245:0,389:0,522:0,648:0,649:0,650:0,651:0,652:0,653:0,654:0,655:0,656:0,657:0,658:0,659:0,959:0}
shpr={}
printingDictionary={}
class DailyWorksheet:
    def __init__(self):
        self=self

    def createSheet(shpr,invoicedate,ifNewPo,polinks,poNOd):
        
        for item in os.listdir(f"C:/pdfInvoiceMaker/Invoices/{invoicedate}/"):
           # print(item)
            if item.endswith(f".pdf"):
                skuDictionary={23:0,27:0,80:0,88:0,158:0,169:0,192:0,194:0,214:0,245:0,389:0,522:0,648:0,649:0,650:0,651:0,652:0,653:0,654:0,655:0,656:0,657:0,658:0,659:0,959:0,667:0}

                with pdfplumber.open(f"C:/pdfInvoiceMaker/Invoices/{invoicedate}/{item}") as pdf:
                    page=pdf.pages[0]
                    text=page.extract_text()
                    shopname=text.split('\n')[1]
                    lines=text.split('\n')
                    del lines[0:9]
                    del lines[-3:-1]
                    del lines[-1]
                    #print(lines)
                    
                    for line in lines:
                        line=line.split(' ')
                        #print(line[0])
                        if shopname not in shpr.keys():
                            print('A')
                            
                            skuDictionary[int(line[0])]=int(line[-4])
                        else:
                            #print('B')
                            #skuDictionary=shpr[shopname]
                            #print(skuDictionary,line)
                            skuDictionary[int(line[0])]=int( skuDictionary[int(line[0])] ) + int(line[-4])
                        #print(skuDictionary)

                shpr[shopname]=skuDictionary                            
            
#-----------------------Data extraction done-----------------------------------------

        for k,v in shpr.items():
            for kk,vv in v.items():
                if kk not in printingDictionary.keys():
                    printingDictionary[kk]=[kk,defaultPrintData[kk],vv]
                    
                else:
                    printingDictionary[kk]=printingDictionary[kk]+[vv]
                    
        #print(printingDictionary)

#---------------------Data processing done -------------------------------------------

        pdf = FPDF(format='A3')
        pdf.add_page()
        pdf.set_font("Helvetica", size = 16,style='B')
        pdf.set_font_size(30)
        pdf.cell(275,10,f'{invoicedate}',ln=1,align='C')

        pdf.set_font_size(12)
        TABLE_COL_NAMES = ('Sku','Product', *shpr.keys(),'Total')
        line_height = 10
        col_width = pdf.epw /(3+len(shpr.keys()))
        pdf.set_font_size(15)
        def render_table_header():
            
            pdf.set_fill_color(230,230,230)
            pdf.set_font(style="B")
            for col_name in TABLE_COL_NAMES:
                if col_name=='Product':
                    col_width=45
                elif col_name=='Sku' or col_name=='Total':
                    col_width=30
                else:
                    col_width = pdf.epw /(3+len(shpr.keys()))
                pdf.cell(col_width,line_height,col_name, border=2,align='C',fill=True)
            pdf.ln(line_height)
        render_table_header()
        

        for i in printingDictionary.values():
            i=i+[sum(i[2::])]
            c=0
            for j in i:
                c=c+1
                #print(j)
                if j==0:
                    j=''
                if j in defaultPrintData.values():
                    col_width=45
                elif j in defaultPrintData.keys():
                    col_width=30
                elif c==len(i):
                    col_width=30                    
                else:
                    col_width = pdf.epw /(3+len(shpr.keys()))
                pdf.cell(col_width,line_height,f'{j}', border=2,align='C',fill=False)
            pdf.ln(line_height)
        pdf.output(f'C:/pdfInvoiceMaker/Invoices/{invoicedate} worksheet.pdf')
        
        if ifNewPo==True :
            os.startfile(f'C:/pdfInvoiceMaker/Invoices/{invoicedate} worksheet.pdf','print')
        
        #for item in os.listdir(f'C:/pdfInvoiceMaker/Invoices/{invoicedate}/'):
        #    if item.endswith('.pdf'):
        #        print('')
                #os.startfile(f'C:/pdfInvoiceMaker/Invoices/{tomorrow}/{item}','print')
                #os.startfile(f'C:/pdfInvoiceMaker/Invoices/{tomorrow}/{item}','print')

