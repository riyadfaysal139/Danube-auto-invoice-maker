import os
import pdfplumber
import pandas as pd
from datetime import datetime
import numpy as np

def is_valid_pdf(file_path):
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)
            return header == b'%PDF'
    except Exception:
        return False

def load_name_mapping(file_path):
    name_mapping = {}
    with open(file_path, 'r') as f:
        for line in f:
            key, value = line.strip().split(':')
            name_mapping[key.strip()] = value.strip()
    return name_mapping

def extract_data_from_pdfs(po_date):
    po_date_directory = os.path.join('PO', po_date)
    if not os.path.exists(po_date_directory):
        print(f"No directory found for PO date: {po_date}")
        return

    name_mapping = load_name_mapping('name_mapping.txt')
    dataframes = {}
    po_numbers = {}

    for file_name in os.listdir(po_date_directory):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(po_date_directory, file_name)
            if not is_valid_pdf(file_path):
                print(f"Skipping invalid PDF file: {file_path}")
                continue
            print(f"Processing file: {file_path}")
            all_data = []
            po_number = file_name.split('337337_')[1].split('_JED')[0]  # Extract PO number from filename
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

            df = pd.DataFrame(all_data)
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

            # Rename columns
            df.columns = ["SKU", "Description", "Unit Price", "Quantity", "Price", "Vat", "Amount"]

            # Replace name based on mapping
            replaced = False
            for key, value in name_mapping.items():
                if key in file_name:
                    file_name = value
                    replaced = True
                    break
            if not replaced:
                # Keep only JED_**** part if no mapping is found
                file_name = 'JED_' + file_name.split('JED_')[1].split('_')[0]

            dataframes[file_name] = df
            po_numbers[file_name] = po_number

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', None)
    print(dataframes)
    return dataframes, po_numbers