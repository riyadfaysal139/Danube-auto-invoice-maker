from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import subprocess
import sqlite3
import os
from dateTimeHandler import get_date
import df_editor  # Import df_editor to handle DataFrame modifications
from pdfExtractor import PDFExtractor  # Import PDFExtractor class

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    default_date = get_date()  # Get the default date from get_date function
    po_files = []
    all_po_files = []
    invoice_file = None
    po_date = None
    if request.method == 'POST':
        if 'show_all_po' in request.form:
            # Show all PO files
            for root, dirs, files in os.walk('Files/PO'):
                for file in files:
                    relative_path = os.path.relpath(os.path.join(root, file), 'Files/PO')
                    all_po_files.append(relative_path)
                    print(relative_path)
        else:
            po_date = request.form['po_date']
            # Run the main.py script with the selected po_date and capture the output
            result = subprocess.run(['python', 'main.py', po_date], capture_output=True, text=True)
            invoice_file = result.stdout.strip()
            
            # Fetch the list of POs for the selected date
            db_path = 'Files/DB/downloaded_files.db'
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT file_name FROM downloaded_files WHERE po_release_date = ?", (po_date,))
            po_files = cursor.fetchall()
            conn.close()
        
    return render_template('index.html', default_date=default_date, po_files=po_files, all_po_files=all_po_files, po_date=po_date, invoice_file=invoice_file)

@app.route('/edit_file', methods=['POST'])
def edit_file():
    file_name = request.form['file_name']
    po_date = request.form['po_date']
    file_path = os.path.join('Files', 'PO', po_date, file_name)
    pdf_extractor = PDFExtractor(po_date)  # Create an instance of PDFExtractor
    name_mapping = pdf_extractor.load_mapping('Files/Texts/name_mapping.txt', {"example_key": "example_value"})
    df = pdf_extractor.extract_text_from_pdf(file_path)
    df = pdf_extractor.clean_dataframe(df)
    df_html = df.to_html(classes='dataframe', header="true", index=False)
    return render_template('edit.html', file_name=file_name, po_date=po_date, df_html=df_html)

@app.route('/update_file', methods=['POST'])
def update_file():
    file_name = request.form['file_name']
    po_date = request.form['po_date']
    action = request.form['action']
    sku = request.form.get('sku')
    description = request.form.get('description')
    unit_price = request.form.get('unit_price')
    quantity = request.form.get('quantity')

    file_path = os.path.join('Files', 'PO', po_date, file_name)
    pdf_extractor = PDFExtractor(po_date)  # Create an instance of PDFExtractor
    name_mapping = pdf_extractor.load_mapping('Files/Texts/name_mapping.txt', {"example_key": "example_value"})

    # Call the process_pdf function from pdfExtractor to get the DataFrame
    df = pdf_extractor.extract_text_from_pdf(file_path)
    df = pdf_extractor.clean_dataframe(df)

    # Perform the action on the DataFrame
    df = df_editor.handle_dataframe(df, action, sku, description, float(unit_price), int(quantity))

    # Update the totals
    df = pdf_extractor.calculate_totals(df)

    df_html = df.to_html(classes='dataframe', header="true", index=False)
    return render_template('edit.html', file_name=file_name, po_date=po_date, df_html=df_html)

@app.route('/Files/PO/<po_date>/<filename>')
def download_file(po_date, filename):
    po_directory = os.path.join('Files', 'PO', po_date)
    return send_from_directory(po_directory, filename)

@app.route('/Files/Invoices/<filename>')
def download_invoice(filename):
    invoice_directory = os.path.join('Files', 'Invoices')
    return send_from_directory(invoice_directory, filename)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
