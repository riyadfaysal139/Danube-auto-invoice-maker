from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import subprocess
import sqlite3
import os
from dateTimeHandler import get_date

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    default_date = get_date()  # Get the current date in the KSA timezone
    default_date = '2024-12-25'
    po_files = []
    all_po_files = []
    invoice_file = None
    po_date = None
    selected_flag = "skip all"  # Default flag value
    if request.method == 'POST':
        selected_flag = request.form.get('flag', "skip all")
        if 'show_all_po' in request.form:
            # Show all PO files
            for root, dirs, files in os.walk('Files/PO'):
                for file in files:
                    relative_path = os.path.relpath(os.path.join(root, file), 'Files/PO')
                    all_po_files.append(relative_path)
                    print(relative_path)
        else:
            po_date = request.form['po_date']
            # Run the main.py script with the selected po_date and selected_flag
            result = subprocess.run(['python', 'main.py', po_date, selected_flag], capture_output=True, text=True)
            invoice_file = result.stdout.strip()
            
            # Fetch the list of POs for the selected date
            db_path = 'Files/DB/downloaded_files.db'
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT file_name FROM downloaded_files WHERE po_release_date = ?", (po_date,))
            po_files = cursor.fetchall()
            conn.close()
        
    return render_template('home.html', default_date=default_date, po_files=po_files, all_po_files=all_po_files, po_date=po_date, invoice_file=invoice_file, selected_flag=selected_flag)

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
