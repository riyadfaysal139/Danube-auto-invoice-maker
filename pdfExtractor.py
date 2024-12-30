import os
import pdfplumber
import pandas as pd
from datetime import datetime
import numpy as np
import df_editor  # Import df_editor to handle DataFrame modifications

class PDFExtractor:
    def __init__(self, po_date):
        self.po_date = po_date
        self.po_date_directory = os.path.join('Files', 'PO', po_date)
        self.name_mapping = self.load_mapping('Files/Texts/name_mapping.txt', {"example_key": "example_value"})
        self.dataframes = {}
        self.po_numbers = {}

    def extract_data_from_pdfs(self):
        if not os.path.exists(self.po_date_directory):
            print(f"No directory found for PO date: {self.po_date}")
            return {}, {}

        for file_name in os.listdir(self.po_date_directory):
            if file_name.endswith('.pdf'):
                self.process_pdf_file(file_name)

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_colwidth', None)
        print(self.dataframes)
        return self.dataframes, self.po_numbers

    def is_valid_pdf(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                header = f.read(4)
                return header == b'%PDF'
        except Exception:
            return False

    def create_default_file(self, file_path, default_content):
        with open(file_path, 'w') as f:
            for key, value in default_content.items():
                f.write(f"{key}: {value}\n")

    def load_mapping(self, file_path, default_content):
        if not os.path.exists(file_path):
            self.create_default_file(file_path, default_content)
        mapping = {}
        with open(file_path, 'r') as f:
            for line in f:
                key, value = line.strip().split(':')
                mapping[key.strip()] = value.strip()
        return mapping

    def extract_text_from_pdf(self, file_path):
        all_data = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    lines = text.split('\n')
                    # Extract data from row 10 till the row containing the word "Notes"
                    start_collecting = False
                    for i, line in enumerate(lines):
                        if "Notes" in line:
                            break
                        if start_collecting:
                            if '-----------' not in line:
                                all_data.append(line.split())
                        if i >= 10:
                            start_collecting = True
        return pd.DataFrame(all_data)

    def clean_dataframe(self, df):
        # Ensure each row has 7 elements
        for i in range(len(df)):
            if len(df.iloc[i]) < 7:
                df.iloc[i] = df.iloc[i].tolist() + [None] * (7 - len(df.iloc[i]))

        # Delete columns 3, 4, 5 if they exist, except for the last row
        if len(df.columns) > 5:
            df.iloc[:-1, 3] = None
            df.iloc[:-1, 4] = None
            df.iloc[:-1, 5] = None

        # Merge data from each odd row, column 0 & 1, and paste them to the previous row's column 1
        for i in range(1, len(df), 2):
            if i < len(df):
                df.iloc[i-1, 1] = f"{df.iloc[i, 0]} {df.iloc[i, 1]}"
        # Drop the odd rows after merging, except the last one
        df = df.drop(df.index[1::2][:-1])
        # Drop the second last row
        if len(df) > 1:
            df = df.drop(df.index[-2])

        # Delete columns 3, 4, 5
        if len(df.columns) > 5:
            df = df.drop(df.columns[[3, 4, 5]], axis=1)

        # Delete the last row
        if len(df) > 0:
            df = df[:-1]

        # Rename columns
        df.columns = ["SKU", "Description", "Unit Price", "Quantity", "Price", "Vat", "Amount"]

        return df

    def calculate_totals(self, df):
        # Calculate Price, Vat, and Amount
        df["Unit Price"] = pd.to_numeric(df["Unit Price"], errors='coerce').round(3)
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors='coerce').fillna(0).astype(int)
        df["Price"] = (df["Unit Price"] * df["Quantity"]).round(4)
        df["Vat"] = (df["Price"] * 0.15).round(4)
        df["Amount"] = (df["Price"] + df["Vat"]).round(4)


        # Calculate totals and add a new row
        total_quantity = int(df["Quantity"].dropna().astype(int).sum())
        total_price = round(df["Price"].dropna().astype(float).sum(), 4)
        total_vat = round(df["Vat"].dropna().astype(float).sum(), 4)
        total_amount = round(df["Amount"].dropna().astype(float).sum(), 4)
        total_row = pd.DataFrame([["", "Total", "", total_quantity, total_price, total_vat, total_amount]], columns=df.columns)
        df = df.append(total_row, ignore_index=True)

        return df

    def process_pdf_file(self, file_name):
        file_path = os.path.join(self.po_date_directory, file_name)
        if not self.is_valid_pdf(file_path):
            print(f"Skipping invalid PDF file: {file_path}")
            return

        print(f"Processing file: {file_path}")
        po_number = file_name.split('337337_')[1].split('_JED')[0]  # Extract PO number from filename
        df = self.extract_text_from_pdf(file_path)
        df = self.clean_dataframe(df)

        # Pass the cleaned DataFrame to df_editor for editing if required
        df = df_editor.edit_dataframe(df)

        # Pass the modified DataFrame back to pdfExtractor for total calculation
        df = self.calculate_totals(df)

        # Replace name based on mapping
        replaced = False
        for key, value in self.name_mapping.items():
            if key in file_name:
                file_name = value
                replaced = True
                break
        if not replaced:
            # Keep only JED_**** part if no mapping is found
            file_name = 'JED_' + file_name.split('JED_')[1].split('_')[0]

        self.dataframes[file_name] = df
        self.po_numbers[file_name] = po_number