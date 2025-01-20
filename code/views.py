from flask import Blueprint, render_template , request, redirect , jsonify
import pandas as pd
import sqlServer as db
import logWriter as lw
import serverData as sd
import sqlServer as sq
import jsonGen as jg
from copy import copy
import requests
import json
import numpy as np
from tqdm import tqdm
import time
import decimal
import os , datetime

#views = Blueprint(__name__,"views")
#JSON Encoder
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, decimal.Decimal):
            return str(obj)   
        return super(NpEncoder, self).default(obj)

#POST data for eninvoicing
def postRequest(header,payLoad):
    url         = sd.invoiceUrl
    headerData  = header
    dat         = json.dumps(payLoad, cls=NpEncoder) 
    #print(dat)
    postData    = dat.encode('utf-8')
    resp = requests.post(url,headers=headerData,data=postData)
    # print(json.loads(resp.text))
    return json.loads(resp.text)

#Handle Response from server
def requestHandler(payLoad,resp,filterHeader):
    lw.logBackUpRecord(str(resp))
    #If Error
    if len(resp['ErrorList']) >0:
        last_update_date = (datetime.datetime.now()).strftime("%Y-%m-%d")
        last_updated_by = "Python Code"
        Request_Payload = str(payLoad).replace("'",'"')
        Response_Payload = str(resp).replace("'",'"')
        device_id = str(payLoad['DeviceId'])
        db.updateDataSQL(['error_message',
                          'last_update_date',
                          'last_updated_by',
                          'Request_Payload',
                          'Response_Payload',
                          'device_id'],
                          
                          sd.headerTable,filterHeader,

                          (resp['ErrorList'],
                           last_update_date,
                           last_updated_by,
                           Request_Payload,
                           Response_Payload,
                           device_id))
    else:
        zatca_status = str(resp['InvoiceStatus'])
        warning_message = str(resp['WarningList'])
        zatca_qr_status = str(resp['QrCodeStatus'])
        zatca_qr_code = str(resp['QRCode'])
        zatca_issue_date = str(resp['IssueDate'])
        # zatca_invoice_xml = str(resp['InvoiceXml'])
        zatca_uuid = str(resp['UUID'])
        last_update_date = (datetime.datetime.now()).strftime("%Y-%m-%d")
        last_updated_by = "Python Code"
        Request_Payload = str(payLoad).replace("'",'"')
        # Response_Payload = str(resp).replace("'",'"')
        device_id = str(payLoad['DeviceId'])

        db.updateDataSQL(['zatca_status',
                            'warning_message',
                            'zatca_qr_status',
                            'zatca_qr_code',
                            'zatca_issue_date',
                            # 'zatca_invoice_xml',
                            'zatca_uuid',
                            'last_update_date',
                            'last_updated_by',
                            'Request_Payload',
                            # 'Response_Payload',
                            'device_id'],
                            
                            sd.headerTable,filterHeader,
                            
                            (zatca_status,
                            warning_message,
                            zatca_qr_status,
                            zatca_qr_code,
                            zatca_issue_date,
                            # zatca_invoice_xml,
                            zatca_uuid,
                            last_update_date,
                            last_updated_by,
                            Request_Payload,
                            # Response_Payload,
                            device_id))
    
def mainProcess():
    # filterHeader = "header_id = '162'"
    # invoData = db.SelectData(sd.outInvoCol, sd.invoiceTable, filterHeader, sd.outInvoCol)
    # taxData = db.SelectData(sd.inTaxCol, sd.taxTable, filterHeader, sd.outTaxCol)
    #Try dbConnection 
    try:
        dataSelecter = "(CONVERT(varchar,ZATCA_STATUS) NOT IN('REPORTED', 'CLEARED', 'ACCEPTED_WITH_WARNING')) AND (error_message IS NULL or CONVERT(varchar,error_message) = '') AND BatchNo>=162" 
        headerData = db.SelectData(sd.outHeadCols, sd.headerTable,dataSelecter, sd.inHeadCols)
        lw.logBackUpRecord("No of New Records:"+str(len(headerData)))
    except Exception as e: 
        lw.logRecord("Invoice Status Loading Failed :"+str(e))
        return False
    
    # zHeader = jg.head_json()
    print(len(headerData))
    
    for ind , row in headerData.iterrows():
        # if str(row['header_id']) == '983':
        try:
            filterHeader = "header_id = '"+str(row['header_id'])+"'"
            filterHeader_line = "header_id= '"+str(row['order_id_en'])+"'"

            invoData = db.SelectData(sd.outInvoCol, sd.invoiceTable, filterHeader_line, sd.inInvoCol) 

            buyer_email = str(row['buyer_email'])
            exc_rate = float(row['Invoice_Exchange_Rate']) if row['Invoice_Exchange_Rate'] is not None else float(1)
            print(buyer_email) 
            payLoad  = jg.header_json_array(row, invoData)
            
            filterHeader = "header_id = '"+str(row['header_id'])+"'"
            filterHeader_line = "header_id= '"+str(row['order_id_en'])+"'"
            
            lw.logBackUpRecord("Head Json Loaded for:"+str(filterHeader_line))
            
            # invoData = db.SelectData(sd.outInvoCol, sd.invoiceTable, filterHeader_line, sd.inInvoCol)
            
            
            payLoad['EInvoice']['InvoiceLine']  =  jg.invoice_json_array(invoData)
            
            lw.logBackUpRecord("Invoice Json Loaded for:"+str(filterHeader_line))
            
            taxData = db.SelectData(sd.inTaxCol, sd.taxTable, filterHeader_line, sd.outTaxCol)
    
            payLoad['EInvoice']['TaxTotal'] = jg.tax_json_array(taxData, exc_rate)

            # payLoad['EInvoice']['AllowanceCharge'] = jg.tax_allowance(taxData)
            
            lw.logBackUpRecord("TaxTotal Json Loaded for:"+str(filterHeader_line))
            
            #To be deleted
            
            print(str(payLoad))

            lw.logBackUpRecord(str(payLoad))

            lw.logRecord(str(payLoad))
            
            #Ends
            zHeader = jg.head_json(payLoad['EInvoice']['AccountingSupplierParty']['Party']['PartyTaxScheme']['CompanyID'])
            print(zHeader)
            resp = postRequest(zHeader,payLoad)

            lw.logBackUpRecord(str(payLoad))
            lw.logBackUpRecord(str(resp))
            lw.logBackUpRecord("Json Shared to cleartax:"+str(filterHeader_line))
            
            requestHandler(payLoad,resp,filterHeader)
            
            lw.logBackUpRecord("Data Loaded into ROCKFORD :"+str(filterHeader_line))
            try:
                if resp['Status'] == 'GENERATED':
                    pdfPrint(payLoad)
                    send_email(payLoad, buyer_email)
                else:
                    pass
            except:
                pass
        except Exception as e: 
            lw.logRecord("Invoice Status Loading Failed :"+str(e))
        break
    move_to_error()
    delete_duplicate_Records()
    return "Done"

def pdfPrint(payLoad):
    # Generate PDF JSON header 
    vat = payLoad['EInvoice']['AccountingSupplierParty']['Party']['PartyTaxScheme']['CompanyID']           
    try:    
        headerData = jg.head_json_pdf(vat)
    except Exception as e:
        lw.logRecord("PDF header JSON Failed :"+str(e))
    
    invoiceNumber = payLoad['EInvoice']['ID']['en'] 
    inv_type = payLoad['EInvoice']['InvoiceTypeCode']['value']
    invoiceTypeDic = {
                    '388': 'INV',
                    '381': 'CRN',
                    '383': 'DBN',
                    '386': 'RECEIPT'
                    }
    inv_type = invoiceTypeDic[inv_type]
    issueDate = payLoad['EInvoice']['IssueDate']
    templateId = '2584'
    filterHeader = "order_id_en = '"+invoiceNumber+"'"
    # Print PDF
    try:
        pdfURL = '{}?invoiceNumber={}&documentType={}&vat={}&issueDate={}&templateId={}'.format(sd.pdfURL, invoiceNumber, inv_type, vat, issueDate, templateId) 
        response_pdf = requests.get(pdfURL, headers=headerData) 
    except Exception as e:
        lw.logRecord("PDF payload Failed :"+str(e))

    try:
        print(response_pdf.status_code)
        # Check if the response is successful (status code 200)
        if response_pdf.status_code == 200:
            # Open a file in binary mode and write the content
            with open('data/pdf/'+str(payLoad['EInvoice']['ID']['en'])+'.pdf', 'wb') as pdf_file:
                pdf_file.write(response_pdf.content)
            db.updateDataSQL(['zatca_pdfa3'],sd.headerTable, filterHeader  ,('GENERATED'))  
        else:
            lw.logRecord("No PDF generated by cleartax")
            db.updateDataSQL(['zatca_pdfa3'],sd.headerTable, filterHeader  ,('FAILED'))
    except:
        lw.logRecord("Clear tax Response is not 200")
        db.updateDataSQL(['zatca_pdfa3'],sd.headerTable, filterHeader  ,('FAILED'))

def send_email(payLoad, buyer_email):
    # Generate send Email JSON header 
    vat = payLoad['EInvoice']['AccountingSupplierParty']['Party']['PartyTaxScheme']['CompanyID']           
    try:    
        headerData = jg.head_json_pdf(vat)
    except Exception as e:
        lw.logRecord("PDF header JSON Failed :"+str(e))    

    invoiceNumber = payLoad['EInvoice']['ID']['en'] 
    inv_type = payLoad['EInvoice']['InvoiceTypeCode']['value']
    invoiceTypeDic = {
                    '388': 'INV',
                    '381': 'CRN',
                    '383': 'DBN',
                    '386': 'RECEIPT'
                    }
    inv_type = invoiceTypeDic[inv_type]
    issueDate = payLoad['EInvoice']['IssueDate']
    templateId = '2584'
    filterHeader = "order_id_en = '"+invoiceNumber+"'"
    buyer_email = buyer_email.split(",")
    email_json = json.dumps({
            "Attachments": {
                "documentDetails": [
                {
                "IssueDate": issueDate,
                "InvoiceNumber": invoiceNumber,
                "InvoiceType": inv_type,
                "Vat": vat
                }
            ],
                "documentType": "EINVOICE",
                "printTemplateId": templateId
            },
            "PreviewDetails": {
            "Template": {
                    "Type": "INVOICE_GENERATED"
                },
                "CounterParties": [
                    {
                        "Contacts": [
                            {
                                "Email": buyer_email[0],
                                "EmailRecipientType": "TO"
                            },
                            {
                                "Email": buyer_email[1],
                                "EmailRecipientType": "TO"
                            },
                            {
                                "Email": "rohan.d@cloudare.in",
                                "EmailRecipientType": "CC"
                            }
                        ]
                    }
                ]
                
            }
            })
    try:
        # email_json = json.dumps(email_json, indent=4)
        # pdfURL = '{}'.format(sd.emailURL) 
        print(email_json)
        response_pdf = requests.post(sd.emailURL, data=email_json, headers=headerData) 
    except Exception as e:
        lw.logRecord("Email payload Failed :"+str(e))

    try:
        print(response_pdf.status_code)
        # Check if the response is successful (status code 200)
        if response_pdf.status_code == 200:
            # Update the status
            db.updateDataSQL(['zatca_email'],sd.headerTable, filterHeader  ,('GENERATED'))  
        else:
            lw.logRecord("Email not sent by cleartax")
            db.updateDataSQL(['zatca_email'],sd.headerTable, filterHeader  ,('FAILED'))
    except:
        lw.logRecord("Clear tax Response is not 200")
        db.updateDataSQL(['zatca_email'],sd.headerTable, filterHeader  ,('FAILED'))

                     

# A3 PDF generation 
def pdfProcess():
    
    #Get all the PD file list
    try:
        pdfList = os.listdir(sd.readPDF)
        print("PDF to A3 PDF:"+str(len(pdfList)))
    except Exception as e:
        lw.logRecord("PDF directory Failed :"+str(e))
        
    for pdfName in pdfList:
        
        if pdfName.endswith('.pdf'):
            #Read file Details
            try:
                invoice , vat , inv_type , dt = pdfName.split('_')
                dt , fileType = dt.split('.')
                dt = datetime.datetime.strptime(dt, '%d%m%Y')
                invoiceDate = dt.strftime('%Y-%m-%d')
                
                invoicePDF = sd.readPDF+'/'+pdfName
                
                #print(invoicePDF)
                
                invoiceTypeDic = {
                    '388': 'INV',
                    '381': 'CRN',
                    '383': 'DBN',
                    '386': 'RECEIPT'
                    }
                inv_type = invoiceTypeDic[inv_type]
                
                filterHeader = "NUM_0 = '"+invoice+"'"
                
            except Exception as e:
                lw.logRecord("PDF file Name reading Failed :"+str(e))
            
            # Generate PDF JSON header            
            try:    
                headerData = jg.head_json_pdf()
            except Exception as e:
                lw.logRecord("PDF header JSON Failed :"+str(e))
            
            # Create the Payload for PDF
            try:
                payLoad = jg.pdf_invoice_gener(invoice , vat , inv_type , invoiceDate)
            except Exception as e:
                lw.logRecord("PDF payload Failed :"+str(e))
            
            # Read pdf File and Send data to clear tax
            try:    
                with open(invoicePDF, 'rb') as invoicePDFfile:
                    pdffile = {'file': invoicePDFfile}
                    resp = requests.post(sd.pdfURL, headers=headerData, data=payLoad, files=pdffile)                     
            except Exception as e:
                lw.logRecord("PDF reading file and sending failed :"+str(e))    
           
            try: 
            #Handle Resposne
                if resp.status_code == 200:                
                    outfile = sd.saveA3PDF +'/'+pdfName
      
                    if 'application/pdf' in resp.headers.get('Content-Type', ''):
                        invocieA3pdf = resp.content
                        
                        #Save the A3 file
                        with open(outfile, 'wb') as pdfA3:
                            pdfA3.write(invocieA3pdf)
                        
                        #Move the file to Archive
                        dstPath = sd.archivePDF +'/'+pdfName
                        scrPath = invoicePDF
                        os.rename(scrPath, dstPath)
                        
                        db.updateDataSQL(['ZATCAPDFA3_0'],sd.headerTable, filterHeader  ,('GENERATED'))    
                    else:
                        lw.logRecord("No PDF generated by cleartax")
                        db.updateDataSQL(['ZATCAPDFA3_0'],sd.headerTable, filterHeader  ,('FAILED'))
                else:
                    lw.logRecord("Clear tax Response is not 200")
                    db.updateDataSQL(['ZATCAPDFA3_0'],sd.headerTable, filterHeader  ,('FAILED'))
                    
            except Exception as e:
                lw.logRecord("PDF saving Failed :"+str(e))       
            
def move_to_error():
    try:
        
        dataSelecter = "(error_message IS NOT NULL OR CONVERT(varchar, error_message) <> '')" 
        # result = db.SelectData(sd.outHeadCols, sd.headerTable,dataSelecter, sd.inHeadCols)
        colData = ', '.join(sd.outHeadCols)
        sql = "SELECT "+colData+" FROM "+sd.headerTable
        if dataSelecter != "":
            sql = sql +" WHERE "+dataSelecter
        mydb = sq.connection()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        results = mycursor.fetchall()
        # values = [list(row) for row in mycursor.fetchall()]
        # values = ', '.join(values)
        # print(values)
        column_names = ', '.join(sd.inHeadCols)
        print(column_names)
        lw.logBackUpRecord("No of Records to be deleted:"+str(len(results)))
    except Exception as e: 
        lw.logRecord("Invoice Status Loading Failed :"+str(e))
        return False
    try:
        if isinstance(results, list) and len(results) > 0:
            # Prepare the placeholders for the INSERT statement
            num_columns = len(results[0])
            # column_names = ", ".join(result[0].keys())
            placeholders = ", ".join([f":{i+1}" for i in range(num_columns)])

            # insert_query = f"INSERT INTO {sd.headerTable_error} ({column_names}) VALUES ({placeholders})"
            insert_query = f"SET IDENTITY_INSERT [CYGTST].[dbo].[ARINVHEADER_STAGING_ERROR] ON; INSERT INTO {sd.headerTable_error} ({column_names}) VALUES "
            print(insert_query)
            for result in results:
                print(result)
                result = list(result)
                # values = [list(row) for row in result]
                print(result)
                result = [str(item) for item in result]
                print(result)
                # values = ', '.join(result)
                # print(values)
                # values = f"({values})"
                values = tuple(result)
                print(values)
                insert_query = insert_query + str(values)
                print(insert_query)
                # db.dbInsert_many(insert_query, values)
                db.dbInsert(insert_query)

                print(int(result['order_id_en']))
                # result = self._execute(conn, cursor, insert_query, params=values, is_commit=True)
                delete_invoice_query = f"DELETE FROM {sd.headerTable} WHERE order_id_en = {result['order_id_en']}"
                print(delete_invoice_query)
                delete_invoice_line_query = f"DELETE FROM {sd.invoiceTable} WHERE header_id = {result['order_id_en']}"
                print(delete_invoice_line_query)
                # self._execute(conn, cursor, delete_invoice_query, is_commit=True)
                print(delete_invoice_query)
                db.dbInsert(delete_invoice_query)
                
                # self._execute(conn, cursor, delete_invoice_line_query, is_commit=True)
                print(delete_invoice_line_query)
                db.dbInsert(delete_invoice_line_query)
                
                # conn.commit()
    except Exception as e: 
        lw.logRecord("Invoice Status Loading Failed :"+str(e))
        return False

def standardise_results(self, query_cursor):
        '''
        Takes a cursor object as input and returns a standardized data list of dictionaries
        '''
        data_rows = query_cursor.fetchall()
        final_row = list()
        if len(data_rows) != 0:
            for data_row in data_rows:
                obj = {}
                for i in range(len(data_row)):
                    obj[query_cursor.description[i - 1][0].lower()] = data_row[i - 1]
                final_row.append(obj)
            return final_row
        return final_row

def delete_duplicate_Records():
    # sql = 'DELETE FROM [CYGTST].[dbo].[ARINVDETAIL_STAGING] WHERE ROWID IN ( SELECT ROWID FROM ( SELECT ROWID AS row_id, ROW_NUMBER() OVER (PARTITION BY header_id) AS row_num FROM [CYGTST].[dbo].[ARINVDETAIL_STAGING]) WHERE row_num > 1);'
    sql = 'WITH DuplicateRows AS (SELECT order_id_en, ROW_NUMBER() OVER (PARTITION BY order_id_en ORDER BY last_update_date DESC) AS row_num FROM [CYGTST].[dbo].[ARINVHEADER_STAGING_ERROR]) DELETE FROM DuplicateRows WHERE row_num > 1;'
    db.dbInsert(sql)