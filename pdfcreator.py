from fpdf import FPDF
import pandas as pd
from datetime import datetime
import qrcode
import codecs
import arabic_reshaper
from bidi.algorithm import get_display
import os

class PDFCreator:
    def create_pdf(self, dataframes_dict, po_numbers, output_path="", po_date="", invoicedate=""):
        pdf = FPDF(format='A3')
        self.setup_fonts(pdf)
        
        base_invoice_numbers = self.load_base_invoice_numbers('name_mapping.txt')
        description_mapping = self.load_english_description_mapping('description_mapping.txt')
        arabic_description_mapping = self.load_arabic_description_mapping('arabic_description_mapping.txt')
        increment = self.calculate_increment(invoicedate)

        for title, dataframe in dataframes_dict.items():
            print(f"Processing key: {title}")  # Print the dictionary key
            pdf.add_page()
            pdf.set_font("Amiri", '', 14)

            # Add tax invoice, title, and buyer-supplier info
            self.add_invoice_header(pdf, title, base_invoice_numbers, po_numbers, po_date, invoicedate, increment)

            pdf.set_font("Amiri", '', 14)

            # Add dataframe data
            self.add_dataframe_data(pdf, dataframe, description_mapping, arabic_description_mapping)

            # Print the dataframe in table format
            print(dataframe.to_string(index=False))

            # Generate and add QR code
            self.add_qr_code(pdf, title, invoicedate, dataframe)

        pdf.output(output_path, 'F')

    def setup_fonts(self, pdf):
        pdf.add_font('Amiri', '', 'Amiri-Regular.ttf', uni=True)
        pdf.add_font('Amiri', 'B', 'Amiri-Bold.ttf', uni=True)

    def calculate_increment(self, invoicedate):
        base_date = datetime.strptime("2024-12-24", "%Y-%m-%d")
        current_date = datetime.strptime(invoicedate.split()[0], "%Y-%m-%d")
        days_difference = (current_date - base_date).days
        return (days_difference // 1) * 5  # Increment by 5 for each day

    def add_invoice_header(self, pdf, title, base_invoice_numbers, po_numbers, po_date, invoicedate, increment):
        pdf.set_font("Amiri", 'B', 16)
        pdf.cell(0, 10, 'TAX INVOICE', 0, 1, 'C')
        pdf.ln(10)

        pdf.cell(0, 10, title, 0, 1, 'C')
        pdf.ln(10)

        self.add_supplier_buyer_info(pdf)

        invoice_number = self.determine_invoice_number(base_invoice_numbers, title, increment)
        po_link = f"https://bindawoodapps.com/DANPO/337337_{po_numbers[title]}_JED_00{title.split('-')[-1]}.pdf"
        pdf.cell(0, 10, f'Po No: {po_numbers[title]}', 0, 0, 'L', link=po_link)
        pdf.cell(0, 10, f'Invoice NO: {invoice_number}', 0, 1, 'R')

        pdf.cell(0, 10, f'Po Date: {po_date}', 0, 0, 'L')
        pdf.cell(0, 10, f'Invoice Date: {invoicedate}', 0, 1, 'R')
        pdf.ln(10)

    def add_supplier_buyer_info(self, pdf):
        pdf.set_font("Amiri", '', 14)
        pdf.cell(0, 10, 'Supplier: 337337 FAKHR ALTASHYEED EST.', 0, 0, 'L')
        pdf.cell(0, 10, 'Buyer: SOU Vegetable for South', 0, 1, 'R')
        pdf.cell(0, 10, 'Tax Reg. Number: 301308065300003', 0, 0, 'L')
        pdf.cell(0, 10, 'Tax Reg. Number: 310072568710003', 0, 1, 'R')
        pdf.cell(0, 10, 'Phone: 0501212591-0507006855', 0, 0, 'L')
        pdf.cell(0, 10, '-----------------------------', 0, 1, 'R')

    def determine_invoice_number(self, base_invoice_numbers, title, increment):
        location_code = title.split('_')[1] if '_' in title else title
        base_invoice_number = base_invoice_numbers.get(location_code, 0)
        return base_invoice_number + increment

    def add_dataframe_data(self, pdf, dataframe, description_mapping, arabic_description_mapping):
        num_columns = len(dataframe.columns) + 1  # Adding one for the new column
        col_widths = [30 if i == 1 else (280 - 30) / (num_columns - 1) for i in range(num_columns)]

        pdf.set_fill_color(230, 230, 230)  # Set grey color
        pdf.set_font("Amiri", 'B', 14)
        for i, column in enumerate(dataframe.columns):
            pdf.cell(col_widths[i], 10, column, 1, 0, 'C', fill=True)
            if i == 1:
                pdf.cell(col_widths[i], 10, "Arabic Desc.", 1, 0, 'C', fill=True)
        pdf.ln()
        pdf.set_font("Amiri", '', 14)

        row_height = 10  # Fixed row height
        for index, row in dataframe.iterrows():
            for i, item in enumerate(row):
                if i == 1:
                    sku = row[0]
                    description = description_mapping.get(str(sku), "") if str(sku) in description_mapping else str(item)
                    reshaped_text = arabic_reshaper.reshape(description)
                    bidi_text = get_display(reshaped_text)
                    pdf.cell(col_widths[i], row_height, bidi_text, 1)  # Replace description from mapping
                    arabic_description = arabic_description_mapping.get(str(sku), "") if str(sku) in arabic_description_mapping else ""
                    reshaped_arabic_text = arabic_reshaper.reshape(arabic_description)
                    bidi_arabic_text = get_display(reshaped_arabic_text)
                    pdf.cell(col_widths[i], row_height, bidi_arabic_text, 1)  # Add Arabic description from mapping
                else:
                    pdf.cell(col_widths[i], row_height, str(item), 1)
            pdf.ln(row_height)

        # Set last row's columns 1, 2, 3, and 7 to null
        if not dataframe.empty:
            last_row_index = dataframe.index[-1]
            dataframe.at[last_row_index, 'Description'] = None
            dataframe.at[last_row_index, 'Unit Price'] = None
            dataframe.at[last_row_index, 'Quantity'] = None
            dataframe.at[last_row_index, 'Amount'] = None

    def add_qr_code(self, pdf, title, invoicedate, dataframe):
        seller_name = "337337 FAKHR ALTASHYEED EST."
        tax_number = "301308065300003"
        invoice_date = invoicedate.split()[0]
        total_amount = dataframe.iloc[-1, 5]  # Get the total amount from the last row, column 5
        vat_amount = dataframe.iloc[-1, 4]  # Get the VAT amount from the last row, column 4

        tlv1 = f"01{len(seller_name):02x}{seller_name.encode().hex()}"
        tlv2 = f"02{len(tax_number):02x}{tax_number.encode().hex()}"
        tlv3 = f"03{len(invoice_date):02x}{invoice_date.encode().hex()}"
        tlv4 = f"04{len(str(total_amount)):02x}{str(total_amount).encode().hex()}"
        tlv5 = f"05{len(str(vat_amount)):02x}{str(vat_amount).encode().hex()}"

        tlv = f"{tlv1}{tlv2}{tlv3}{tlv4}{tlv5}"
        b64 = codecs.encode(codecs.decode(tlv, 'hex'), 'base64').decode().replace('\n', '')

        qr = qrcode.QRCode(
            version=1,
            box_size=3,
            border=0.1
        )
        qr.add_data(b64)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        img_path = f"image_{title}.png"
        img.save(img_path)

        pdf.cell(0, 10, txt="", ln=1, align='L')
        pdf.image(img_path, x=120, y=None, w=0, h=0, type='', link='')

        # Delete the QR code image after adding it to the PDF
        if os.path.exists(img_path):
            os.remove(img_path)

    def load_base_invoice_numbers(self, file_path):
        base_invoice_numbers = {}
        with open(file_path, 'r') as f:
            lines = f.readlines()
            start_reading = False
            for line in lines:
                if line.strip() == "base_invoice_numbers:":
                    start_reading = True
                    continue
                if start_reading:
                    key, value = line.strip().split(':')
                    base_invoice_numbers[key.strip()] = int(value.strip())
        return base_invoice_numbers

    def load_english_description_mapping(self, file_path):
        description_mapping = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    sku, description = parts
                    description_mapping[sku] = description
        return description_mapping

    def load_arabic_description_mapping(self, file_path):
        arabic_description_mapping = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    sku, description = parts
                    arabic_description_mapping[sku] = description
        return arabic_description_mapping
