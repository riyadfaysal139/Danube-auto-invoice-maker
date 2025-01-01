from datetime import datetime
import datetime,re

class pdfExtractor:
    def __init__(self):
        self=self

    def extractPdf(poNoLocD,invoicedates):
        print('Extracting pdf')
        import pdfplumber
        import datetime
        import arabic_reshaper
        from bidi.algorithm import get_display
        shpr={}
        shprs=[]
        po=[]
        invNo=0
        invNO={}
        poNOd={}
        shopQTt={}
        for poNO,poLoc in poNoLocD.items():
            po.append(poNO)
            with pdfplumber.open(poLoc) as pdf:
                page=pdf.pages[0]
                text=page.extract_text()

            #print(text)
            #Determining shop name
            shopName=''

            shop=['164 BINJALALA','158 RAVALA','140 ABHA','139 JIZAN','137 BINJALALA']
            defaultInvoiceNo=4245
            defaultInvoiceDate=datetime.datetime(2021, 9, 30)
            gap=invoicedates-defaultInvoiceDate
            gap=str(gap)
            invoiceCounter=0
            for i in gap.split():
                invoiceCounter=int(i)
                break


            for s in text.split('\n'):
                if shop[0] in s.upper():
                    shopName='KHAMIS-164'
                    invNO[shopName]=defaultInvoiceNo+4+(invoiceCounter*5)
                    if shopName in poNOd:
                        poNOd[shopName]=str(poNOd[shopName])+' and '+str(poNO)
                    else:
                        poNOd[shopName]=poNO
                    break
                elif shop[1] in s.upper():
                    shopName='RAVALA-158'
                    invNO[shopName]=defaultInvoiceNo+2+(invoiceCounter*5)
                    if shopName in poNOd:
                        poNOd[shopName]=str(poNOd[shopName])+' and '+str(poNO)
                    else:
                        poNOd[shopName]=poNO
                    break
                elif shop[2] in s.upper():
                    shopName='ABHA-140'
                    invNO[shopName]=defaultInvoiceNo+1+(invoiceCounter*5)
                    if shopName in poNOd:
                        poNOd[shopName]=str(poNOd[shopName])+' and '+str(poNO)
                    else:
                        poNOd[shopName]=poNO
                    break
                elif shop[3] in s.upper():
                    shopName='JIZAN-139'
                    invNO[shopName]=defaultInvoiceNo+(invoiceCounter*5)
                    if shopName in poNOd:
                        poNOd[shopName]=str(poNOd[shopName])+' and '+str(poNO)
                    else:
                        poNOd[shopName]=poNO
                    break
                elif shop[4] in s.upper():
                    shopName='KHAMIS-137'
                    invNO[shopName]=defaultInvoiceNo+3+(invoiceCounter*5)
                    if shopName in poNOd:
                        poNOd[shopName]=str(poNOd[shopName])+' and '+str(poNO)
                    else:
                        poNOd[shopName]=poNO
                    break

            page=pdf.pages[0]
            text=page.extract_text()
            text2=text.split(' ')
        
            pono=(text2[text2.index('Order')+3]) # Extracting pono from po
            
            #print('************')               
            #parsing=(text2[text2.index('Date:')+1]).split('\n')[0] # Extracting podate from po

            text3=text.split('\n')
            quantityVatTotal=re.split('\s+',(text3[-17]))
            """quantity=quantityVatTotal[6]
            vatlessTotal=quantityVatTotal[7]
            vat=quantityVatTotal[8]
            total=quantityVatTotal[9]"""
            quantity='488'
            vatlessTotal='640'
            vat='96.003'
            total='736.003'
            
            products=[23,27,80,88,158,169,192,214,245,389,522,648,649,650,651,652,653,654,655,656,657,658,659,959,194,667]
            arabic=[' ',' ','رجله','ملوخية ',' ',' ',' ',' ',' ',' ','خس','بقدونس ','كزبرة ','نعناع','سبانخ','شبت ','حبق ','جرجير ','كراث ','بصل أخضر ','فجل أحمر ','فجل أبيض ','سلك ',' ',' ','']
            eng=['Cabbage-white','Banger','Regla','Mulukhia','Cauliflower','Lettuce-Chinese','Cabbage-red','Celery','Lettuce--round','Broccoli','Lettuce','Parsely','Coriander','Mint','Spinach','Dill','Habak','Gerger','Leeks','Onion-Green','Red-Turnip','White-Turnip','Silk','Lettuce-Round','Brocoli','Pineapple']


            i=0
            text4=[]
            productList=[]
            while i>=0:
                if text3[12+i]==' -----------' or text3[12+i]==' ____________________________________________________________________________________________________________________________________':
                    break
                else:
                    text4.append(text3[12+i])
                i=i+2

            for i in text4:
                t=re.split('\s+', i)
                del t[-1:-2]
                del t[0]
                del t[1]
                del t[2:5]
                del t[-1]
                t[1], t[2] = t[2], t[1]
                t[3], t[4] = t[4], t[3]
                
                #print(shopName,t)
                aa=products.index(int(t[0]))
                t.insert(1, eng[aa])
                #t.insert(2,arabic[aa])
                productList.append(t)

            if shopName not in shpr:
                shpr[shopName]=productList
                shopQTt[shopName]=[quantity,vatlessTotal,vat,total]
            else:
                lll=[quantity,vatlessTotal,vat,total]
                shopQTt[shopName]=[float(x) + float(y) for (x, y) in zip(shopQTt[shopName], lll)]
                for i in range(len(shopQTt[shopName])):
                    shopQTt[shopName][i]="{:.5f}".format(shopQTt[shopName][i])
                    print(i)
           #     for i in shpr[shopName]:
                    for j in productList:
                        if str(i[0])==str(j[0]):
                            i[2]=int(i[2])+int(j[2])
                            i[4]=float(i[4])+float(j[4])
                            i[4]=str(round(float(i[4]),4))
                            
                            i[5]=float(i[5])+float(j[5])
                            i[5]=str(round(float(i[5]),4))
                            productList.remove(j)
                shpr[shopName]=shpr[shopName]+productList
                

                #print(productList,'#****#',shpr[shopName],type(shpr[shopName]),'&&&&&\n&&')
            #print(shopQTt)
            
            #shopQTt[shopName]=[quantity,vatlessTotal,vat,total]
            print(shopName,'#\n',shpr,'*\n',po,'*\n',invNO,'*\n',invNo,'*\n',poNOd,'*\n',shopQTt,'*       *\n',productList)
        shpr['ABHA-140']=shpr['ABHA-140'] + [['659', 'Silk', '10', '.6500', '.975', '7.4750']]
        for i in shpr['ABHA-140'][-2]:
            print(type(i), i)
        print('Pdf Extraction Done',shpr['ABHA-140'])
        
        #print(shpr,'*\n',po,'*\n',invNO,'*\n',invNo,'*\n',poNOd,'*\n',shopQTt,'*       *\n',productList)
        return shpr,po,invNO,invNo,poNOd,shopQTt
#