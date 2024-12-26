from playwright.sync_api import sync_playwright
import os
import requests
import pdfplumber
from datetime import datetime
import platform
import subprocess
import time
import sqlite3

class PODownloader:
    def login():
        url = 'https://bindawoodapps.com/BDS/'
        username = '337337'
        password = '12345678'
        db_path = 'Files/DB/downloaded_files.db'

        # Ensure the directory for the database file exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Initialize the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS downloaded_files (file_name TEXT PRIMARY KEY, po_release_date TEXT)''')
        conn.commit()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=50)
            page = browser.new_page()
            page.goto(url)
            
            # Select 'DANUBE' in the first dropdown
            page.click('input[class=search]')
            page.click("div[data-value='DANUBE']")

            # Click on the specified element before entering 'JED'
            page.click('//*[@id="signinform"]/div[2]/div/i')
            time.sleep(1)  # Wait for 1 second
            page.click('//*[@id="signinform"]/div[2]/div/input[1]')

            # Select 'JED' in the second dropdown
            page.click("div[data-value='JED']")

            # Ensure the value is set correctly
            page.evaluate("document.querySelector('#signinform > div:nth-child(2) > div > input:nth-child(1)').value = 'JED';")

            # Fill in username and password
            page.fill('input[name=inputName]', username)
            page.fill('input[name=inputPassword]', password)
            
            # Submit the form
            page.click('button[type=submit]')
            page.wait_for_selector("div.ui.five.doubling.centered.cards")

            # Navigate directly to the elpo page
            page.goto('https://bindawoodapps.com/BDS/elpo.php')
            page.wait_for_selector('//*[@id="tablemargins"]/div/div[1]/a[2]', state='visible')
            page.click('//*[@id="tablemargins"]/div/div[1]/a[2]')

            # Check if the new tab has some files
            new_tab_files = page.query_selector_all("table.ui.table tbody tr")
            if new_tab_files:
                # Process files in the new tab
                pdf_links = [
                    f'https://bindawoodapps.com/DANPO/337337_{row.query_selector_all("td")[1].inner_text().strip()}_JED_00{row.query_selector_all("td")[3].inner_text().strip().split(" ")[0]}.pdf'
                    for row in new_tab_files
                    if len(row.query_selector_all("td")) >= 4
                ]

                # Download all PDF files and check the date mentioned in the PDF
                for link in pdf_links:
                    download_path = os.path.basename(link)
                    if not is_file_downloaded(download_path, cursor):
                        try:
                            print(f"Downloading: {link}")
                            response = requests.get(link)
                            print(f"Response status code: {response.status_code}")
                            response.raise_for_status()  # Raise an exception for HTTP errors
                            with open(download_path, 'wb') as f:
                                f.write(response.content)

                            with pdfplumber.open(download_path) as pdf:
                                text = "".join(page.extract_text() for page in pdf.pages)
                                po_release_date = datetime.strptime(text.split('PO Released Date:')[1].split()[0], '%d/%m/%y').strftime('%Y-%m-%d')
                                # Debugging statement to check po_release_date
                                print(f"Extracted po_release_date: {po_release_date}")
                                # Ensure po_release_date is correctly extracted
                                if po_release_date:
                                    po_release_day = datetime.strptime(po_release_date, '%Y-%m-%d').strftime('%A')
                                    po_date_directory = os.path.join('Files', 'PO', po_release_date)
                                    os.makedirs(po_date_directory, exist_ok=True)
                                    final_path = os.path.join(po_date_directory, download_path)

                                    if not os.path.exists(final_path):
                                        os.rename(download_path, final_path)
                                        print(f"Downloaded and saved: {final_path}")
                                        log_downloaded_file(download_path, po_release_date, cursor, conn)
                                        # print_file(final_path)  # Comment out this line if printing is not required
                                    else:
                                        os.remove(download_path)
                                        print(f"The PO has already been downloaded for date {po_release_date} {po_release_day}")
                                else:
                                    print(f"Failed to extract po_release_date from {download_path}")
                        except Exception as e:
                            print(f"Failed to download {link}: {e}")
            else:
                print("No new PO found")

            # Go to the viewed section
            page.wait_for_selector('//*[@id="tablemargins"]/div/div[3]/div[2]/a[1]', state='visible')
            page.click('//*[@id="tablemargins"]/div/div[3]/div[2]/a[1]')

            # Process files in the viewed section
            viewed_files = page.query_selector_all("table.ui.table tbody tr")
            if viewed_files:
                pdf_links = [
                    f'https://bindawoodapps.com/DANPO/337337_{row.query_selector_all("td")[1].inner_text().strip()}_JED_00{row.query_selector_all("td")[3].inner_text().strip().split(" ")[0]}.pdf'
                    for row in viewed_files
                    if len(row.query_selector_all("td")) >= 4
                ]

                for link in pdf_links[:8]:  # Download only the first two files from the viewed section
                    download_path = os.path.basename(link)
                    if not is_file_downloaded(download_path, cursor):
                        try:
                            print(f"Downloading: {link}")
                            response = requests.get(link)
                            print(f"Response status code: {response.status_code}")
                            response.raise_for_status()  # Raise an exception for HTTP errors
                            with open(download_path, 'wb') as f:
                                f.write(response.content)

                            with pdfplumber.open(download_path) as pdf:
                                text = "".join(page.extract_text() for page in pdf.pages)
                                po_release_date = datetime.strptime(text.split('PO Released Date:')[1].split()[0], '%d/%m/%y').strftime('%Y-%m-%d')
                                # Debugging statement to check po_release_date
                                print(f"Extracted po_release_date: {po_release_date}")
                                # Ensure po_release_date is correctly extracted
                                if po_release_date:
                                    po_release_day = datetime.strptime(po_release_date, '%Y-%m-%d').strftime('%A')
                                    po_date_directory = os.path.join('Files', 'PO', po_release_date)
                                    os.makedirs(po_date_directory, exist_ok=True)
                                    final_path = os.path.join(po_date_directory, download_path)

                                    if not os.path.exists(final_path):
                                        os.rename(download_path, final_path)
                                        print(f"Downloaded and saved: {final_path}")
                                        log_downloaded_file(download_path, po_release_date, cursor, conn)
                                        # print_file(final_path)  # Comment out this line if printing is not required
                                    else:
                                        os.remove(download_path)
                                        print(f"The PO has already been downloaded for date {po_release_date} & day {po_release_day}")
                                else:
                                    print(f"Failed to extract po_release_date from {download_path}")
                        except Exception as e:
                            print(f"Failed to download {link}: {e}")

            browser.close()
            conn.close()

def is_file_downloaded(file_name, cursor):
    cursor.execute("SELECT 1 FROM downloaded_files WHERE file_name = ?", (file_name,))
    return cursor.fetchone() is not None

def log_downloaded_file(file_name, po_release_date, cursor, conn):
    cursor.execute("INSERT INTO downloaded_files (file_name, po_release_date) VALUES (?, ?)", (file_name, po_release_date))
    conn.commit()

def print_file(file_path):
    if platform.system() == 'Windows':
        os.startfile(file_path, 'print')
    elif platform.system() == 'Darwin':  # macOS
        subprocess.run(['lp', file_path])
    else:
        print("Printing is not supported on this OS")