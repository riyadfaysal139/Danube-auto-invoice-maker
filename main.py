import sys
from dateTimeHandler import get_date, get_day
import poDownloader, os, pdfExtractor
from pdfcreator import PDFCreator
from invoiceprinter import print_invoice  # Import the print function

# Get po_date from command-line argument or use default
po_date = sys.argv[1] if len(sys.argv) > 1 else get_date()
invoicedate = get_date(days=1, specific_date=str(po_date))

# Create directories for po_date and invoicedate
po_date_directory = os.path.join('Files', 'PO', str(po_date))
invoice_date_directory = os.path.join('Files', 'Invoices', str(invoicedate))

os.makedirs(po_date_directory, exist_ok=True)
os.makedirs(invoice_date_directory, exist_ok=True)

# Download all PO
poDownloader.PODownloader.login()

"""
dataframes_dict, po_numbers = pdfExtractor.extract_data_from_pdfs(str(po_date))

# Create an instance of PDFCreator
pdf_creator = PDFCreator()

# Get the day for po_date and invoicedate
po_day = get_day(po_date)
invoice_day = get_day(invoicedate)

# Call create_pdf method with the dataframe dictionary, po_numbers, output file path, po_date, and invoicedate
pdf_creator.create_pdf(dataframes_dict, po_numbers, os.path.join(invoice_date_directory, f"{invoicedate}.pdf"), po_date=f"{po_date} ({po_day})", invoicedate=f"{invoicedate} ({invoice_day})")

# Print the invoices
print_invoice(invoicedate)


DailyWorksheet.createSheet(shpr,invoicedate,ifNewPo,polinks,poNOd)

pdfMerger.mergePdf(invoicedate,isprintTime,statementTime,parsingdate)#Merge all the created pdf's into one file(Don't move it anywhere else)
#t.sleep(5)
DriveUploader.uploadToDrive(invoicedate,isprintTime,statementTime,ifNewPo)#Upload the pdf's to google drive
"""