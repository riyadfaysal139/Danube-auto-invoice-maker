import time as t
from dateTimeHandler import dateTimeHandler
import invoiceDownloader,os,pdfExtractor
from pdfCreator import pdfCreator
from DriveUploader import DriveUploader
from pdfMerger import pdfMerger
from DailyWorksheet import DailyWorksheet
import sys
for i in range(1):
    date_string,parsingdates,parsingdate,invoicedates,invoicedate,isprintTime,statementTime,statementTexLoc=dateTimeHandler.hanleDateTime(-1)#Return all necessary date and time data
    isdir = os.path.isdir(f'C:/pdfInvoiceMaker/Invoices/{invoicedate}/')
    if isdir==True:
        for f in os.listdir(f'C:/pdfInvoiceMaker/Invoices/{invoicedate}/'):
            os.remove(os.path.join(f'C:/pdfInvoiceMaker/Invoices/{invoicedate}/', f))
    
    poNoLocD,ifNewPo,polinks=invoiceDownloader.invoiceDownloader.downloadPo(parsingdate,invoicedate)#return po No and it's local file location after downloading the po's based on dateTimeHandler return data
    if len(polinks)<1:
        isprintTime=False
    print(isprintTime)
    #isprintTime=True
    #statementTime=True
    #if ifNewPo==False and isprintTime==False:
    #    sys.exit()
    #poNoLocD={'0021141552': 'C:/pdfInvoiceMaker/PO/337337_0021141552_JED_00139_2022-07-07.pdf', '0021141695': 'C:/pdfInvoiceMaker/PO/337337_0021141695_JED_00137_2022-07-07.pdf', '0021141696': 'C:/pdfInvoiceMaker/PO/337337_0021141696_JED_00139_2022-07-07.pdf', '0021141697': 'C:/pdfInvoiceMaker/PO/337337_0021141697_JED_00140_2022-07-07.pdf', '0021141698': 'C:/pdfInvoiceMaker/PO/337337_0021141698_JED_00158_2022-07-07.pdf', '0021142180': 'C:/pdfInvoiceMaker/PO/337337_0021142180_JED_00164_2022-07-07.pdf'}
    #ifNewPo=False
    #polinks=['337337_0021141552_JED_00139.pdf', '337337_0021141695_JED_00137.pdf', '337337_0021141696_JED_00139.pdf', '337337_0021141697_JED_00140.pdf', '337337_0021141698_JED_00158.pdf', '337337_0021142180_JED_00164.pdf']

    shpr,po,invNO,invNo,poNOd,shopQTt=pdfExtractor.pdfExtractor.extractPdf(poNoLocD,invoicedates)#return all necessary data from po and for invoice generating
    with open("C:/pdfInvoiceMaker/Invoices/readme.txt", 'w') as f:
        f.write(f'{shpr}')
    pdfCreator.createPdf(shpr,po,invNO,invNo,poNOd,shopQTt,parsingdates,invoicedates,invoicedate,parsingdate,polinks,isprintTime,statementTexLoc,poNoLocD,ifNewPo)#Create invoice with Qr code

    DailyWorksheet.createSheet(shpr,invoicedate,ifNewPo,polinks,poNOd)

    pdfMerger.mergePdf(invoicedate,isprintTime,statementTime,parsingdate)#Merge all the created pdf's into one file(Don't move it anywhere else)
    #t.sleep(5)
    DriveUploader.uploadToDrive(invoicedate,isprintTime,statementTime,ifNewPo)#Upload the pdf's to google drive