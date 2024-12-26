from flask import Flask, render_template, request, redirect, url_for
import subprocess
from datetime import datetime
from dateTimeHandler import get_date

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    default_date = get_date()  # Get the default date from get_date function
    if request.method == 'POST':
        po_date = request.form['po_date']
        # Run the main.py script with the selected po_date
        subprocess.run(['python', 'main.py', po_date])
        return redirect(url_for('index'))
    return render_template('index.html', default_date=default_date)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
