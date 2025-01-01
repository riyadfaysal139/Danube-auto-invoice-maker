import imp


class dateTimeHandler:
    def __init__(self):
        self=self
    
    def hanleDateTime(temporr):
        import datetime
        import calendar
        today=datetime.date.today()
        #yesterday = datetime.date.today() + datetime.timedelta(-1)
        #tomorrow = datetime.date.today() + datetime.timedelta(1)
        last_day_of_month = calendar.monthrange(today.year, today.month)[1]
        print(last_day_of_month)
        
        date_string=str(datetime.date.today()+datetime.timedelta(temporr))

        print('Looking Po for date: '+str(date_string))
        parsingdates = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        invoicedates=(parsingdates)+ datetime.timedelta(days=1)

        for z in str(parsingdates).split():
            parsingdate=z
            break
        for z in str(invoicedates).split():
            invoicedate=z
            break

        c=str(datetime.datetime.now().strftime("%H%M%S"))
        isprintTime=False
        statementTime=False
        print(datetime.date(today.year, today.month, last_day_of_month))
        if int(c)>=180000 :
            isprintTime=True
            if date_string == str(datetime.date(today.year, today.month, last_day_of_month)):
                statementTime=True
                print('its statement and printing time')
            else:
                statementTime=False
        statementTexLoc=datetime.datetime.now()+ datetime.timedelta(0)
        statementTexLoc=statementTexLoc.strftime("%B-%Y")
        statementTexLoc=f'C:/pdfInvoiceMaker/statement-{statementTexLoc}.txt'

        with open(statementTexLoc, 'a+') as f:
            print(statementTexLoc)
        
        return date_string,parsingdates,parsingdate,invoicedates,invoicedate,isprintTime,statementTime,statementTexLoc