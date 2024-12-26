import os
import platform
import subprocess
from datetime import datetime
from flask import Flask, request, render_template

app = Flask(__name__)

def print_invoice(invoice_date=None):
    # Path to the text file that tracks printed invoices
    track_file = 'printed_invoices.txt'
    
    # Read the already printed invoices
    if os.path.exists(track_file):
        with open(track_file, 'r') as file:
            printed_invoices = file.read().splitlines()
    else:
        printed_invoices = []

    # Get the list of invoices
    invoices = get_invoices(invoice_date)

    for invoice in invoices:
        if invoice['date'] not in printed_invoices:
            print_invoice_file(invoice['file'])
            printed_invoices.append(invoice['date'])

    # Update the track file
    with open(track_file, 'w') as file:
        file.write('\n'.join(printed_invoices))

def get_invoices(invoice_date=None):
    # This function should return a list of invoices
    # Each invoice should be a dictionary with 'date' and 'file' keys
    # For example: [{'date': '2024-10-01', 'file': 'invoice1.pdf'}, ...]
    # Here we use a placeholder implementation
    invoices = [
        {'date': '2024-10-01', 'file': 'invoice1.pdf'},
        {'date': '2024-10-02', 'file': 'invoice2.pdf'},
        {'date': '2024-10-03', 'file': 'invoice3.pdf'}
    ]
    if invoice_date:
        invoices = [invoice for invoice in invoices if invoice['date'] == invoice_date]
    return invoices

def print_invoice_file(file_path):
    if platform.system() == 'Windows':
        os.startfile(file_path, 'print')
    elif platform.system() == 'Darwin':  # macOS
        subprocess.run(['lp', file_path])
    else:
        print(f"Unsupported OS: {platform.system()}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        invoice_date = request.form['invoice_date']
        try:
            datetime.strptime(invoice_date, '%Y-%m-%d')
            print_invoice(invoice_date)
            message = f"Invoices for {invoice_date} have been printed."
        except ValueError:
            message = "Invalid date format. Please enter date in YYYY-MM-DD format."
        return render_template('index.html', message=message)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)