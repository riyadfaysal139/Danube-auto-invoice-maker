class pdfMerger:
    def __init__(self):
        self=self
    def mergePdf(invoicedate,isprintTime,statementTime,parsingdate):
        import datetime
        import time as tim
        print('Merging pdf')
        import os,time
        from PyPDF2 import PdfFileMerger
        import win32api
        
        source_dir = "C:/pdfInvoiceMaker/Invoices/"+str(invoicedate)+'/'
        merger = PdfFileMerger()

        for item in os.listdir(source_dir):
            if item.endswith('pdf'):
                #print(item)
                merger.append(source_dir + item)
        print(merger)

        
        #if ifnew==True:
            #win32api.ShellExecute(0, "print", 'C:/pdfInvoiceMaker/MergedInvoice/'+str(invoicedate)+'.pdf' , None, ".", 0)
            #tim.sleep(10)
            #win32api.ShellExecute(0, "print", 'C:/pdfInvoiceMaker/MergedInvoice/'+str(invoicedate)+'.pdf' , None, ".", 0)
            #tim.sleep(50)
            #os.startfile('C:/pdfInvoiceMaker/MergedInvoice/'+str(invoicedate)+'.pdf','print')
            #tim.sleep(5)
            #os.startfile('C:/pdfInvoiceMaker/MergedInvoice/'+str(invoicedate)+'.pdf','print')
            
        merger.append('C:/pdfInvoiceMaker/Invoices/'+str(invoicedate)+' worksheet.pdf')
        source_dir="C:/pdfInvoiceMaker/PO/"+str(parsingdate)+'/'
        for item in os.listdir(source_dir):
            if item.endswith('pdf'):
                #print(item)
                merger.append(source_dir + item)

        #merger.write( 'C:/pdfInvoiceMaker/MergedInvoice/'+str(invoicedate)+'with sheet.pdf')
        #else:
        merger.write( 'C:/pdfInvoiceMaker/MergedInvoice/'+str(invoicedate)+'.pdf')
        print('Merging pdf Done')  
        #merger.close()
        #if isprintTime==True and statementTime==True:#
        #    import monthlyStatementxl
        #    monthlyStatementxl.makestatement(parsingdate)

