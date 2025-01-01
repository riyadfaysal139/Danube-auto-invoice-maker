class invoiceDownloader:
    def downloadPo(parsingdate,invoicedate):
        poNoLocD={}
        polinks=[]
        ifNewPo=False
        polinks
        from playwright.sync_api import sync_playwright
        from os import path
        import os
        #from playwright.async_api import async_playwright
        url='https://bindawoodapps.com/BDS/'
        username='337337'
        password='12345678'

        with sync_playwright() as p:
            browser=p.chromium.launch(headless=False,slow_mo=50)
            page=browser.new_page()
            page.goto(url)
            
            page.fill('input[class=search]','DANUBE')
            #time.sleep(1)
            page.click("//*[@id='signinform']/div[1]/div/div[2]/div[2]")

            page.click("//*[@id='signinform']/div[2]/div/i")
            #time.sleep(1)
            page.fill("//*[@id='signinform']/div[2]/div/input[1]",'JED')
            page.click("//*[@id='autodropdownfill']/div[1]")

            page.fill('input[name=inputName]',username)
            page.fill('input[name=inputPassword]',password)
            
            page.click('button[type=submit]')

            page.click("//*[@id='cardmargins']/div[4]/div[3]/span/a")

            page.click("//*[@id='tablemargins']/div/div[3]/div[1]/a[2]")#finding new po
            #//*[@id="tablemargins"]/table/tbody/tr[1]/td[7]/div[2]/a[2]
            #page.click("//*[@id='tablemargins']/div/div[3]/div[2]/a[1]")#finding Old po
            import time
            time.sleep(2)
            a=page.locator('tr').count()
            a=a-2

            #a=0
            print(a)
            #page.pause()
            if a<1:
                ponoS=[]
                for item in os.listdir(f'C:/pdfInvoiceMaker/PO/{parsingdate}/'):
                    if item.endswith('.pdf'):
                        polink=item.split('__')[0]
                        polinks.append(polink)
                        fileno=item.split('_')[1]
                        #filename=fileno.split('_')[2]
                        ponoS.append(fileno)
                        poNoLocD[fileno]=f'C:/pdfInvoiceMaker/PO/{parsingdate}/{item}'
                print(polinks,'**\n',ponoS,'***',poNoLocD)
                with open("C:/pdfInvoiceMaker/pocounter.txt") as f:
                    lines=f.readlines()
                    #print(lines)
                    for k,pono in poNoLocD.items():                        
                        if pono in lines or f'{pono}\n' in lines:
                            print(f'Invoice already created for po: {pono}')
                        else:
                            ifNewPo=True
                            print(f'Invoice not generated for Po: {pono}')
                print('No po found but checking if invoice created successfully')
            
            else:
                ifNewPo=True
                print(f'po found for {parsingdate}')

                for i in range(a):
                    page.click("//*[@id='tablemargins']/div/div[3]/div[1]/a[2]")##Selecting new po again and again
                    #elements = page.query_selector("//*[@id='tablemargins']/table/tbody/tr[1]/td[5]/div[2]/h4/div")
                    #poUploadDate=(str(elements.inner_text()).split('\n'))[0]
                    #print(poUploadDate)
                    paths=f"C:/pdfInvoiceMaker/PO/{parsingdate}/"
                    """if path.exists(paths):
                        print('')
                    else:
                        os.mkdir(paths)"""
                    with page.expect_download() as download_info:
                        page.click("//*[@id='tablemargins']/table/tbody/tr[1]/td[7]/div[2]/a[2]")
                        #page.click("//*[@id='tablemargins']/table/tbody/tr[1]/td[7]/div[2]/a")#oldPO
                    
                    download = download_info.value
                    path = download.path()

                    filename=str(download).split('/')[8]
                    
                    filename=filename.split("'")[0]

                    #polinks.append(filename)

                    filename=filename.split('.')[0]
                    #fileno=filename.split('_')[1]
                    
                    
                    filename=f'C:/pdfInvoiceMaker/PO/{parsingdate}/{filename}.pdf'
                    download.save_as(path=filename)
                    #poNoLocD[fileno]=filename

                    #with open(f'C:/pdfInvoiceMaker/PO/{parsingdate}/{parsingdate}_{filename}.txt', 'a+') as f:
                    #    f.write(f'{poNoLocD}\n{ifNewPo}\n{polinks}')
                ponoS=[]
                for item in os.listdir(f'C:/pdfInvoiceMaker/PO/{parsingdate}/'):
                    if item.endswith('.pdf'):
                        polink=item.split('__')[0]
                        polinks.append(polink)
                        fileno=item.split('_')[1]
                        #filename=fileno.split('_')[2]
                        ponoS.append(fileno)
                        poNoLocD[fileno]=f'C:/pdfInvoiceMaker/PO/{parsingdate}/{item}'
                print(polinks,'**\n',ponoS,'***',poNoLocD)
                with open("C:/pdfInvoiceMaker/pocounter.txt") as f:
                    lines=f.readlines()
                    #print(lines)
                    for k,pono in poNoLocD.items():                        
                        if pono in lines or f'{pono}\n' in lines:
                            print(f'Invoice already created for po: {pono}')
                        else:
                            ifNewPo=True
                            print(f'Invoice not generated for Po: {pono}')
                print('Po found and checking if invoice created successfully')
                    
        #**********************Printing unprinted pos'***************************#

        for k,v in poNoLocD.items():
            with open("C:/pdfInvoiceMaker/pocounter.txt") as f:
                lines=f.readlines()
                #print(lines)
                            
                if v in lines or f'{v}\n' in lines:
                    print(f'Invoice already created for po: {v}')
                else:
                    os.startfile(v,'print')
                    with open("C:/pdfInvoiceMaker/pocounter.txt",'a') as f:
                        f.write(f'\n{v}')
        #*****************Deleting all invoices created earlier*******************************#
        
        return poNoLocD,ifNewPo,polinks