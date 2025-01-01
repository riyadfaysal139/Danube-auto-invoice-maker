import imp


class pdfCreator:
    def __init__(self):
        self=self
    def createPdf(shpr,po,invNO,invNo,poNOd,shopQTts,parsingdates,invoicedates,invoicedate,parsingdate,polinks,isprintTime,statementTexLoc,poNoLocD,ifNewPo):
        
        import os,re
        import arabic_reshaper
        from bidi.algorithm import get_display
        from os import path
        paths="C:/pdfInvoiceMaker/Invoices/"+str(invoicedate)+'/'
        if path.exists(paths):
            print('Path Already Exist')
        else:
            os.mkdir(paths)
        print('Creating pdf')
        c=0
        for k,v in shpr.items():
            shopQTt=shopQTts[k]
            from tkinter.ttk import Style
            from turtle import fillcolor
            from fpdf import FPDF
            import codecs
            import calendar
            import qrcode
            pdf = FPDF(format='A3')
            
            # Add a page
            pdf.add_page()
            #================================ add another cell ================================
            def anotherline(thext,info):
                pdf.set_font("Helvetica", size = 12)
                pdf.cell(0, 10, txt = str(thext), align = 'L')
                pdf.cell(0,10,txt=str(info),ln=1,align='R')

            #================================ adding products and all ================================
            def anotherline(thext,info):
                pdf.set_font("Helvetica", size = 12)
                pdf.cell(0, 10, txt = str(thext), align = 'L')
                pdf.cell(0,10,txt=str(info),ln=1,align='R')


            #================================Default Lines================================
            pdf.set_font("Helvetica",'B', size = 18)
            pdf.cell(0, 30, txt = 'TAX INVOICE',ln=1, align = 'C')
            pdf.cell(0, 10, txt = str(k),ln=1, align = 'C')

            pdf.set_font("Helvetica", size = 12)
            pdf.cell(0, 10, txt = 'Supplier: 337337 FAKHR ALTASHYEED EST.', align = 'L')
            pdf.cell(0,10,txt='Buyer : SOU Vegetable for South',ln=1,align='R')

            pdf.cell(0, 10, txt = 'Tax Reg. Number: 310308065300003', align = 'L')
            pdf.cell(0, 10 ,txt='Tax Reg. Number: 310072568710003',ln=1, align= 'R')

            pdf.cell(0, 10, txt = 'Phone: 0501212591-0507006855', align = 'L')
            pdf.cell(0,10,txt='-------------------------',ln=1,align='R')

            
            pdf.cell(0, 10, txt = 'Po No: '+str(poNOd[k]),link='www.bindawoodapps.com/DANPO/'+str((polinks[c]).split('/')[-1]), align = 'L')
            c=c+1
            pdf.cell(0,10,txt='Invoice No: '+str(invNO[k]),ln=1,align='R')

            pdf.cell(0, 10, txt = 'Po Date:'+str(parsingdate) + ' ('+str(calendar.day_name[(parsingdates).weekday()])+')' , align = 'L')
            pdf.cell(0,10,txt='Invoice Date: '+str(invoicedate) + ' ('+str(calendar.day_name[(invoicedates).weekday()])+')' ,ln=1,align='R')


            #================================ Sku,description, price tab ================================
            pdf.set_font("Helvetica", size = 12)
            pdf.set_fill_color(230,230,230)
            #pdf.cell(0, 20, txt = ' SKU                                                 Description                                           Qty.        Unit Price        Vat 15%            Amount',border=1,fill=True,ln=1, align = 'L')


            TABLE_COL_NAMES = ("Sku", "Description","Description", "Qty", "Unit Price","Vat 15%","Amount")
            tarabic=("كود تعريف", "الصنف 	","الصنف 	", "الكمية ", "سعر الوحدة ","الضريبة ","القيمة ")
            tarabictouple=[]
            line_height = pdf.font_size * 1.6
            col_width = pdf.epw / 7 
            for i in tarabic:
                expression = r"^[a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p-q-r-s-t-u-v-w-x-y-z-A-B-C-D-E-F-G-H-I-J-K-L-M-N-O-P-Q-R-S-T-U-V-W-X-Y-Z]"
                if (re.search(expression,' ' ) is None):
                    #pdf.add_page()
                    pdf.add_font('DejaVu', '', 'C:/pdfInvoiceMaker/DejaVuSans.ttf', uni=True)
                    pdf.set_font('DejaVu', '', 12)
                    i = arabic_reshaper.reshape(i)
                    
                    i = i[::-1]
                    pdf.add_font('DejaVu', '', 'C:/pdfInvoiceMaker/DejaVuSans.ttf', uni=True)
                    pdf.set_font('DejaVu', '', 14)
                    pdf.cell(col_width, line_height, i, border=2,fill=True)
                    tarabictouple.append(i)
                    w = pdf.get_string_width(i) + 6
            pdf.ln(line_height)
            TABLE_DATA = v

 # distribute content evenly
            pdf.set_font("Helvetica", size = 12)
            pdf.set_font_size(16)
            def render_table_header():
                pdf.set_font(style="B")  # enabling bold text
                for col_name in TABLE_COL_NAMES:
                    pdf.cell(col_width, line_height, col_name, border=2,fill=True)
                pdf.ln(line_height)
                pdf.set_font(style="")  # disabling bold text
            render_table_header()
        # repeat data rows
            for column in TABLE_DATA:
                eng=['Cabbage-white','Banger','Regla','Mulukhia','Cauliflower','Lettuce-Chinese','Cabbage-red','Celery','Lettuce-round','Broccoli','Lettuce','Parsely','Coriander','Mint','Spinach','Dill','Habak','Gerger','Leeks','Onion-Green','Red-Turnip','White Turnip','Silk','Lettuce-Round','Brocoli']
                arabic=['-','-','رجله','ملوخية ','-','-','-','-','-','-','خس','بقدونس ','كزبرة ','نعناع','سبانخ','شبت ','حبق ','جرجير ','كراث ','بصل أخضر ','فجل أحمر ','فجل أبيض ','سلك ','-',' -']
                if column[1] in eng:
                    #print(column[1])
                    arabic_string=arabic[eng.index(column[1])]
                    expression = r"^[a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p-q-r-s-t-u-v-w-x-y-z-A-B-C-D-E-F-G-H-I-J-K-L-M-N-O-P-Q-R-S-T-U-V-W-X-Y-Z]"
                    if (re.search(expression,' ' ) is None):                            #pdf.add_page()
                        pdf.add_font('DejaVu', '', 'C:/pdfInvoiceMaker/DejaVuSans.ttf', uni=True)
                        pdf.set_font('DejaVu', '', 12)
                        arabic_string = arabic_reshaper.reshape(arabic_string)
                        arabic_string = arabic_string[::-1]
                        w = pdf.get_string_width(arabic_string) + 6
                    column.insert(2, arabic_string)
                    #print(column)
                else:
                    column.insert(2, '')

            for column in TABLE_DATA:
                if pdf.will_page_break(line_height):
                    render_table_header()
                for datum in column:
                    pdf.cell(col_width, line_height, str(datum), border=1)
                    #print(type(datum))
                    #print(datum)
                pdf.ln(line_height)

            #----------------------------------------------------------------------Table Done


            pdf.set_font("Helvetica", size = 12)
            pdf.cell(0, 10, txt = "" ,ln=1, align = 'L')

            TABLE_COL_NAMES=(
                ("","",'Total Quantity: ',f'{shopQTt[0]}',"",'Total (ex. vat): ',f'{shopQTt[1]} SAR') ,
            ("","","","","",'Total Vat (15%): 'f'{shopQTt[2]} SAR') ,
            ("","","","","",'Total (inc.vat): ',f'{shopQTt[3]} SAR')
            )
            pdf.set_font(style='B')
            pdf.set_font_size(16)
            for row in TABLE_COL_NAMES:
                if pdf.will_page_break(line_height):
                    render_table_header()
                for datum in row:
                    pdf.cell(col_width, line_height, datum, border=0,fill=True)
                pdf.ln(line_height)

            tlv1='011d416d656e6168204b68616c6f6f66616820536f726f7269204173697269'
            tlv2='020f333130333038303635333030303033'
            f=str(invoicedate)
            #print(f,len(f))
            g='T08:00:00'
            tlv3='0313'+f.encode().hex()+g.encode().hex()
            #print(tlv3)
            tlv4='040'+f'{len(shopQTt[3])}'+(f'{shopQTt[3]}').encode().hex()
            tlv5='050'+f'{len(shopQTt[2])}'+(f'{shopQTt[2]}').encode().hex()
            tlv=f"{tlv1}{tlv2}{tlv3}{tlv4}{tlv5}"
            
            #print('########',tlv)
            b64 = codecs.encode(codecs.decode(tlv, 'hex'), 'base64').decode()
            #b64=b64.replace('\n','')
            #b64=' \n'+f'{b64}'
            print('*',b64,"*",len(b64),b64.index('\n'))
            b64=b64.replace('\n','',1)
            print('*',b64,"*",len(b64),b64.index('\n'))
            

            #play_data = wb[str(shopName)]
            qr=qrcode.QRCode(
            version=1,
            box_size=3,
            border=0.1
            )
            qr.add_data(str(b64[:-1]))
            qr.make(fit=True)
            img=qr.make_image(fill_color='black', back_color='white')
            img.save("C:/pdfInvoiceMaker/Invoices/"+str(invoicedate)+'/'+'image.png')

            pdf.cell(0, 10, txt = "" ,ln=1, align = 'L')
            pdf.image("C:/pdfInvoiceMaker/Invoices/"+str(invoicedate)+'/'+'image.png', x = 120, y = None, w = 0, h = 0, type = '', link = '')
            pdfOutput="C:/pdfInvoiceMaker/Invoices/"+str(invoicedate)+'/'+str(poNOd[k])+'_'+str(k)+'_'+str(invoicedate)+".pdf"
            pdf.output(pdfOutput)
            with open("C:/pdfInvoiceMaker/invoiceCounter.txt") as f:
                lines=f.readlines()
                #print(lines)
                            
                if pdfOutput in lines or f'{pdfOutput}\n' in lines:
                    print(f'Invoice already created: {pdfOutput}')
                else:
                    os.startfile(pdfOutput,'print')
                    os.startfile(pdfOutput,'print')
                    with open("C:/pdfInvoiceMaker/invoiceCounter.txt",'a') as f:
                        f.write(f'\n{pdfOutput}')
            
            #if path.exists(statementTexLoc):
            #    print('statement Path Already Exist')
            #else:
            #   f= open(statementTexLoc,"w+")
                #os.mkdir(f"C:/pdfInvoiceMaker/statement-{ccc}.txt")
            """            def replace_line(file_name, line_num, text):
                lines = open(file_name, 'r').readlines()
                lines[line_num] = text
                out = open(file_name, 'w')
                out.writelines(lines)
                out.close()
            
            with open (statementTexLoc,'r') as f:
                lines=f.readlines()
                for ind,line in enumerate(lines):
                    if f"{invNo}" in line:
                        replace_line(statementTexLoc, ind, f'{invoicedate},{invNo},{shopQTt[1]},{shopQTt[2]},0,0,{shopQTt[3]}\n')
                #print(lines,ind)
            # save the pdf with name .pdf"""

            
            import datetime
            ccc=datetime.datetime.now()+ datetime.timedelta(+1)
            ccc=ccc.strftime("%B-%Y")
            from os import path
            if path.exists(f"C:/pdfInvoiceMaker/statement-{ccc}.txt"):
                print('Path Already Exist')
            else:
                f= open(f"C:/pdfInvoiceMaker/statement-{ccc}.txt","w+")
                #os.mkdir(f"C:/pdfInvoiceMaker/statement-{ccc}.txt")
            

            def replace_line(file_name, line_num, text):
                lines = open(file_name, 'r').readlines()
                lines[line_num] = text
                out = open(file_name, 'w')
                out.writelines(lines)
                out.close()
            ttt=False
            with open (statementTexLoc,'r') as f:
                lines=f.readlines()
                
                for ind,line in enumerate(lines):
                    if f"{invNO[k]}" in line:
                        replace_line(statementTexLoc, ind, f'{invoicedate},{invNO[k]},{shopQTt[1]},{shopQTt[2]},0,0,{shopQTt[3]}\n')
                        ttt=True
                        
            if ttt==False:
                with open(f"C:/pdfInvoiceMaker/statement-{ccc}.txt",'a') as f:
                    f.write(f'\n{invoicedate},{invNO[k]},{shopQTt[1]},{shopQTt[2]},0,0,{shopQTt[3]}')               
                #print(lines,ind)
        print('Creating pdf Done')