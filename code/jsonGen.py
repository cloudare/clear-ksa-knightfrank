import pandas as pd
import json
import numpy as np
from datetime import datetime
import logWriter as lw
import serverData as sd
          
#E Invoice hearer
def head_json(vat):
    try:
        header = {}
        header['Content-Type'] = 'application/json'
        header['x-cleartax-auth-token'] = sd.headToken
        header['vat'] = vat
        # header['branch'] = sd.branch
        
    except Exception as e: 
        lw.logRecord("Header Generation Failed :"+str(e))
        
    return header

#PDF hearer
def head_json_pdf(vat):
    try:
        header = {}
        #header['Content-Type'] = 'application/pdf'
        header['x-cleartax-auth-token'] = sd.headToken
        header['vat'] = vat
        header['Content-Type'] = 'application/json'
        # header['branch'] = sd.branch
        
    except Exception as e: 
        lw.logRecord("Header Generation Failed :"+str(e))
        
    return header

#If null asign Value 
def arg(val,dtype):
    if str(val) == "":
        if dtype == "int":
            return 0
        elif dtype == "str":
            return "null"
    else:
        return val
        
#JSON Generator
# Generate Header Invoice Data
def header_json_array(selData):
    try:
        selData = selData.fillna('null')
        
        data = {}
        # selData['supp_company_vat'] = selData['supp_company_vat'][4:]
        if str(int(selData['supp_company_vat'])).zfill(15) == '301244195200003':
            device_id = '15424900-8891-4ddd-935a-71a1da7ba6dc'
        elif str(int(selData['supp_company_vat'])).zfill(15) == '310377157300003':
            device_id = '5cb37939-4813-4429-9c82-4c9cffbfb9e1'
        else:
            device_id = ''

        data['DeviceId'] = device_id

        data['EInvoice'] = {}
        data['EInvoice']['ProfileID'] = selData['profile_id']
        
        data['EInvoice']['ID'] = {}
        data['EInvoice']['ID']['ar']  = selData['order_id_ar']
        data['EInvoice']['ID']['en']  = selData['order_id_en']

        data['EInvoice']['InvoiceTypeCode'] = {}
        data['EInvoice']['InvoiceTypeCode']['name']  = str(selData['invoice_type'])
        #data['EInvoice']['InvoiceTypeCode']['name']   = "0100000"
        data['EInvoice']['InvoiceTypeCode']['value']  = str(selData['invoice_class']) 

        data['EInvoice']['IssueDate'] = selData['issue_date']
        data['EInvoice']['IssueTime'] = selData['issue_time'].split('.')[0]
        
        data['EInvoice']['Delivery']= []
        
        delivery = {}
        delivery['ActualDeliveryDate'] = selData['issue_date']
        #delivery['LatestDeliveryDate'] = '2024-01-27'
        data['EInvoice']['Delivery'].append(delivery)
        
        data['EInvoice']['BillingReference'] = []
        
        billing = {}
        billing['InvoiceDocumentReference'] = {}
        billing['InvoiceDocumentReference']['ID'] = {}
        billing['InvoiceDocumentReference']['ID']['ar'] = '' #selData['invoice_doc_ref_ar']
        billing['InvoiceDocumentReference']['ID']['en'] = selData['linked_transaction_no']
        data['EInvoice']['BillingReference'].append(billing)
        
        data['EInvoice']['OrderReference'] = {}
        data['EInvoice']['OrderReference']['ID'] = {}
        data['EInvoice']['OrderReference']['ID']['ar'] = '' #selData['order_ref_ar']
        data['EInvoice']['OrderReference']['ID']['en'] = selData['order_ref_en']

        # data['EInvoice']['ContractDocumentReference'] = {}
        # data['EInvoice']['ContractDocumentReference']['ID'] = {}
        # data['EInvoice']['ContractDocumentReference']['ID']['ar'] = '' 
        # data['EInvoice']['ContractDocumentReference']['ID']['en'] = selData['invoice_doc_ref_ar']


        data['EInvoice']['DocumentCurrencyCode'] =  selData['document_currency']
        data['EInvoice']['TaxCurrencyCode'] =  selData['tax_currency']

        #Supplier Side Data
        
        data['EInvoice']['AccountingSupplierParty'] = {}
        data['EInvoice']['AccountingSupplierParty']['Party'] ={}
        data['EInvoice']['AccountingSupplierParty']['Party']['PartyLegalEntity'] = {}
        data['EInvoice']['AccountingSupplierParty']['Party']['PartyLegalEntity']['RegistrationName'] = {}
        data['EInvoice']['AccountingSupplierParty']['Party']['PartyLegalEntity']['RegistrationName']['ar'] =  '' #selData['supp_registration_name_ar']
        data['EInvoice']['AccountingSupplierParty']['Party']['PartyLegalEntity']['RegistrationName']['en'] =  selData['supp_registration_name_en']

        data['EInvoice']['AccountingSupplierParty']['Party']['PartyTaxScheme'] = {}
        try:
            data['EInvoice']['AccountingSupplierParty']['Party']['PartyTaxScheme']['CompanyID'] =  str(int(selData['supp_company_vat'])).zfill(15)
        except:
            data['EInvoice']['AccountingSupplierParty']['Party']['PartyTaxScheme']['CompanyID'] = ''
            
        data['EInvoice']['AccountingSupplierParty']['Party']['PartyTaxScheme']['TaxScheme'] = {}
        data['EInvoice']['AccountingSupplierParty']['Party']['PartyTaxScheme']['TaxScheme']['ID'] =  selData['supp_tax_scheme']
        
        if selData['supp_party_identification_scheme'] == "" or selData['buyer_party_identification_scheme'] is None:
            data['EInvoice']['AccountingSupplierParty']['Party']['PartyIdentification'] = None
        else:
            data['EInvoice']['AccountingSupplierParty']['Party']['PartyIdentification'] = {}
            data['EInvoice']['AccountingSupplierParty']['Party']['PartyIdentification']['ID'] = {}
            data['EInvoice']['AccountingSupplierParty']['Party']['PartyIdentification']['ID']['schemeID'] =  selData['supp_party_identification_scheme']
            data['EInvoice']['AccountingSupplierParty']['Party']['PartyIdentification']['ID']['value'] =  selData['supp_party_identification_value']

        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress'] = {}
        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['StreetName'] = {}
        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['StreetName']['ar'] =  '' #selData['supp_treet_name_ar']
        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['StreetName']['en'] =  selData['supp_street_name_en']

        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['AdditionalStreetName'] = {}
        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['AdditionalStreetName']['ar'] =  '' #selData['supp_additional_street_name_ar']
        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['AdditionalStreetName']['en'] =  selData['supp_additional_street_name_en']

        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['BuildingNumber'] = {}
        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['BuildingNumber']['ar'] =  '' #selData['supp_building_INT_ar']
        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['BuildingNumber']['en'] =  selData['supp_building_INT_en']
        try:
            data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['PlotIdentification'] = {}
            data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['PlotIdentification']['ar'] =  '' #str(int(selData['supp_plot_identification_ar'])).zfill(4)
            data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['PlotIdentification']['en'] =  str(int(selData['supp_plot_identification_en'])).zfill(4)
        except:
            lw.logRecord("AccountingSupplierParty PlotIdentification missing")
            
        
        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['CityName'] = {}
        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['CityName']['ar'] =  '' #selData['supp_city_name_ar']
        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['CityName']['en'] =  selData['supp_city_name_en']

        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['CitySubdivisionName'] = {}
        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['CitySubdivisionName']['ar'] =  '' #selData['supp_city_subdivision_name_ar']
        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['CitySubdivisionName']['en'] =  selData['supp_city_subdivision_name_en']


        try:
            data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['PostalZone'] =  str(arg(selData['supp_postal_zone'],"int")).zfill(5)
        except:
            lw.logRecord("AccountingSupplierParty Postal Zone missing")
        
        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['CountrySubentity'] = {}
        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['CountrySubentity']['ar'] =  '' #selData['supp_country_subentity_ar']
        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['CountrySubentity']['en'] =  selData['supp_country_subentity_en']

        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['Country'] = {}
        data['EInvoice']['AccountingSupplierParty']['Party']['PostalAddress']['Country']['IdentificationCode'] =  'SA' #selData['supp_country_identification_code']


        #Buyer Side Data
        data['EInvoice']['AccountingCustomerParty'] = {}
        data['EInvoice']['AccountingCustomerParty']['Party'] = {}
        data['EInvoice']['AccountingCustomerParty']['Party']['PartyLegalEntity'] = {}
        data['EInvoice']['AccountingCustomerParty']['Party']['PartyLegalEntity']['RegistrationName'] = {}
        data['EInvoice']['AccountingCustomerParty']['Party']['PartyLegalEntity']['RegistrationName']['ar'] = '' #selData['buyer_registration_name_ar']
        data['EInvoice']['AccountingCustomerParty']['Party']['PartyLegalEntity']['RegistrationName']['en'] = selData['buyer_registration_name_en']

        data['EInvoice']['AccountingCustomerParty']['Party']['PartyTaxScheme'] = {}
        try:
            data['EInvoice']['AccountingCustomerParty']['Party']['PartyTaxScheme']['CompanyID'] = str(int(selData['buyer_company_vat'])).zfill(15)
        except:
            data['EInvoice']['AccountingCustomerParty']['Party']['PartyTaxScheme']['CompanyID'] = ''
            lw.logRecord("AccountingCustomerParty CompanyID missing")
            
        data['EInvoice']['AccountingCustomerParty']['Party']['PartyTaxScheme']['TaxScheme'] = {}
        data['EInvoice']['AccountingCustomerParty']['Party']['PartyTaxScheme']['TaxScheme']['ID'] = selData['buyer_tax_scheme']
        
        if selData['buyer_party_identification_scheme'] == "" or selData['buyer_party_identification_scheme'] is None:
            data['EInvoice']['AccountingCustomerParty']['Party']['PartyIdentification'] = None
        else:
            data['EInvoice']['AccountingCustomerParty']['Party']['PartyIdentification'] = {}
            data['EInvoice']['AccountingCustomerParty']['Party']['PartyIdentification']['ID'] = {}
            data['EInvoice']['AccountingCustomerParty']['Party']['PartyIdentification']['ID']['schemeID'] = selData['buyer_party_identification_scheme']
            data['EInvoice']['AccountingCustomerParty']['Party']['PartyIdentification']['ID']['value'] = selData['buyer_party_identification_value']

        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress'] = {}
        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['StreetName'] = {}
        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['StreetName']['ar'] = '' #selData['buyer_street_name_ar']
        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['StreetName']['en'] = selData['buyer_street_name_en']

        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['AdditionalStreetName'] = {}
        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['AdditionalStreetName']['ar'] = '' #selData['buyer_additional_street_name_ar']
        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['AdditionalStreetName']['en'] = selData['buyer_additional_street_name_en']

        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['BuildingNumber'] = {}
        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['BuildingNumber']['ar'] = '' #selData['buyer_building_INT_ar']
        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['BuildingNumber']['en'] = selData['buyer_building_INT_en']
        try:
            data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['PlotIdentification'] = {}
            data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['PlotIdentification']['ar'] = '' #str(int(selData['buyer_plot_identification_ar'])).zfill(4)
            data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['PlotIdentification']['en'] = str(int(selData['buyer_plot_identification_en'])).zfill(4)
        except:
            lw.logRecord("AccountingCustomerParty PlotIdentification missing")
            
        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['CityName'] = {}
        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['CityName']['ar'] = '' #selData['buyer_city_name_ar']
        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['CityName']['en'] = selData['buyer_city_name_en']

        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['CitySubdivisionName'] = {}
        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['CitySubdivisionName']['ar'] = '' #selData['buyer_city_subdivision_name_ar']
        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['CitySubdivisionName']['en'] = selData['buyer_city_subdivision_name_en']
        try:
            data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['PostalZone'] = str(int(selData['buyer_postal_zone'])).zfill(5)
        except:
            lw.logRecord("AccountingCustomerParty PostalZone missing")
        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['CountrySubentity'] = {}
        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['CountrySubentity']['ar'] = '' #selData['buyer_country_subentity_ar']
        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['CountrySubentity']['en'] = selData['buyer_country_subentity_en']

        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['Country'] = {}
        data['EInvoice']['AccountingCustomerParty']['Party']['PostalAddress']['Country']['IdentificationCode'] = selData['buyer_country_identification_code']
        
        #Payment Means
        data['EInvoice']['PaymentMeans'] = []
        paymentMeans = {}
        paymentMeans['PaymentMeansCode'] =  selData['payment_means_code']
        
        if selData['credit_memo_reason'] == "CAN":
            credit_memo_reason = "Cancellation or suspension of the supplies after its occurrence either wholly or partially"
        elif selData['credit_memo_reason'] == "ASUP":
            credit_memo_reason = "In case of essential change or amendment in the supply, which leads to the change of the VAT due"
        elif selData['credit_memo_reason'] == "ASUPV":
            credit_memo_reason = "Amendment of the supply value which is pre-agreed upon between the supplier and consumer"
        elif selData['credit_memo_reason'] == "REF":
            credit_memo_reason = "In case of goods or services refund"
        elif selData['credit_memo_reason'] == "CHG":
            credit_memo_reason = "In case of change in Seller's or Buyer's information"
        else:
            credit_memo_reason = ''
            
        paymentMeans['InstructionNote']  = {}
        paymentMeans['InstructionNote']['ar'] = ''
        paymentMeans['InstructionNote']['en'] = credit_memo_reason
        
        paymentMeans['PayeeFinancialAccount']  = {}
        paymentMeans['PayeeFinancialAccount']['PaymentNote'] = {}
        paymentMeans['PayeeFinancialAccount']['PaymentNote']['en'] = ''
        paymentMeans['PayeeFinancialAccount']['PaymentNote']['ar'] = ''
        data['EInvoice']['PaymentMeans'].append(paymentMeans)
        
        #Legal Monetary Total
        data['EInvoice']['LegalMonetaryTotal'] = {}
        data['EInvoice']['LegalMonetaryTotal']['PrepaidAmount'] = {}
        data['EInvoice']['LegalMonetaryTotal']['PrepaidAmount']['currencyID'] = selData['document_currency']
        data['EInvoice']['LegalMonetaryTotal']['PrepaidAmount']['value'] = float(selData['total_prepaid_amount'])

        data['EInvoice']['LegalMonetaryTotal']['TaxExclusiveAmount'] = {}
        data['EInvoice']['LegalMonetaryTotal']['TaxExclusiveAmount']['currencyID'] = selData['document_currency']
        data['EInvoice']['LegalMonetaryTotal']['TaxExclusiveAmount']['value'] = float(selData['total_line_extention_amount'])

        data['EInvoice']['LegalMonetaryTotal']['TaxInclusiveAmount'] = {}
        data['EInvoice']['LegalMonetaryTotal']['TaxInclusiveAmount']['currencyID'] = selData['document_currency']
        data['EInvoice']['LegalMonetaryTotal']['TaxInclusiveAmount']['value'] = float(selData['total_line_amount'])

        data['EInvoice']['LegalMonetaryTotal']['PayableAmount'] = {}
        data['EInvoice']['LegalMonetaryTotal']['PayableAmount']['currencyID'] = selData['document_currency']
        data['EInvoice']['LegalMonetaryTotal']['PayableAmount']['value'] = float(selData['total_payable_amount'])
        
        #Note
        data['EInvoice']['Note'] = {}
        data['EInvoice']['Note']['ar'] = '' #selData['note_ar']
        data['EInvoice']['Note']['en'] = selData['note_en']
        
        #CustomFields
        data['CustomFields'] = {}
        data['CustomFields']['BankName'] = selData['BankName']
        data['CustomFields']['Account_Name'] = selData['Account_Name']
        data['CustomFields']['Account_No'] = selData['Account_No']
        data['CustomFields']['Bank_Address'] = selData['Bank_Address']
        data['CustomFields']['Currency_1'] = selData['Currency']
        data['CustomFields']['SwiftCode'] = selData['SwiftCode']
        data['CustomFields']['IBAN_NO'] = selData['IBAN_NO']

        # data['AllowanceCharge'] = {}
        # data['EInvoice']['AllowanceCharge'] = {}
        # data['EInvoice']['AllowanceCharge']['ChargeIndicator'] = "false"
        # data['EInvoice']['AllowanceCharge']['BaseAmount'] = {}
        # data['EInvoice']['AllowanceCharge']['BaseAmount']['currencyID'] = selData['document_currency']
        # data['EInvoice']['AllowanceCharge']['BaseAmount']['value'] =  selData['total_line_amount']
        # # data['EInvoice']['AllowanceCharge']['MultiplierFactorNumeric'] = 
        # data['EInvoice']['AllowanceCharge']['Amount'] = {}
        # data['EInvoice']['AllowanceCharge']['Amount']['currencyID'] = selData['document_currency']
        # data['EInvoice']['AllowanceCharge']['Amount']['value'] = str(selData['total_discount_amount'])

        # data['EInvoice']['AllowanceCharge']['TaxCategory']={}
        # data['EInvoice']['AllowanceCharge']['TaxCategory']['ID'] = selData

        return data
    except Exception as e: 
        lw.logRecord("Invoice Status Loading Failed :"+str(e))
# Generate Invoice Line    
def invoice_json_array(df):
    json_array = []
    b = False
    print(df.loc[0, 'buyers_item_id_en'])
    if df.loc[0, 'buyers_item_id_en'] == "" or df.loc[0, 'buyers_item_id_en'] == None:
        b = True
        unit_price = line_discount_amount = line_tax_amount = line_total_amount = line_extension_amount = float(0.0)

        for i in range(0,len(df)):
            unit_price = unit_price + float(df.loc[i, 'unit_price'])
            line_discount_amount= line_discount_amount + float(df.loc[i, 'line_discount_amount'])
            line_tax_amount = line_tax_amount + float(df.loc[i, 'line_tax_amount'])
            line_total_amount = line_total_amount + float(df.loc[i, 'line_total_amount'])
            line_extension_amount = line_extension_amount + float(df.loc[i, 'line_extension_amount'])
    try:
        for index, row in df.iterrows():
            if b == False:
                unit_price = row['unit_price']
                line_discount_amount = row['line_discount_amount']
                line_tax_amount = row['line_tax_amount']
                line_total_amount = row['line_total_amount']
                line_extension_amount = row['line_extension_amount']
                total_payable_amount = row['unit_price']

            json_object = {}
            json_object['ID'] = str(index + 1)
            json_object['Item'] = {}
            json_object['Item']['Name'] ={}
            json_object['Item']['Name']['en'] = row['item_name_en'][:255] if row['item_name_en'] is not None else ""
            json_object['Item']['Name']['ar'] = '' #row['item_name_ar']
            
            json_object['Item']['BuyersItemIdentification'] ={}
            json_object['Item']['BuyersItemIdentification']['ID'] = {}
            json_object['Item']['BuyersItemIdentification']['ID']['en'] = row['buyers_item_id_en']
            json_object['Item']['BuyersItemIdentification']['ID']['ar'] = '' #row['buyers_item_id_ar']
            
            json_object['Item']['SellersItemIdentification'] ={}
            json_object['Item']['SellersItemIdentification']['ID'] = {}
            json_object['Item']['SellersItemIdentification']['ID']['en'] = row['sellers_item_id_en']
            json_object['Item']['SellersItemIdentification']['ID']['ar'] = '' #row['sellers_item_id_ar']
            
            json_object['Item']['StandardItemIdentification'] ={}
            json_object['Item']['StandardItemIdentification']['ID'] = {}
            json_object['Item']['StandardItemIdentification']['ID']['en'] = row['standard_item_id_en']
            json_object['Item']['StandardItemIdentification']['ID']['ar'] = '' #row['standard_item_id_ar']
            
            json_object['Item']['ClassifiedTaxCategory'] ={}
            json_object['Item']['ClassifiedTaxCategory']['ID'] = row['item_tax_category']
            json_object['Item']['ClassifiedTaxCategory']['Percent'] = row['item_tax_category_percent']
            json_object['Item']['ClassifiedTaxCategory']['TaxScheme'] = {}
            json_object['Item']['ClassifiedTaxCategory']['TaxScheme']['ID'] = row['item_tax_scheme']
            
            json_object['Price'] = {}
            json_object['Price']['AllowanceCharge'] = {}
            json_object['Price']['AllowanceCharge']['ChargeIndicator'] = "false"
            json_object['Price']['AllowanceCharge']['BaseAmount'] = {}
            json_object['Price']['AllowanceCharge']['BaseAmount']['currencyID'] = row['line_currency']
            json_object['Price']['AllowanceCharge']['BaseAmount']['value'] =  unit_price
            
            json_object['Price']['AllowanceCharge']['Amount'] = {}
            json_object['Price']['AllowanceCharge']['Amount']['currencyID'] = row['line_currency']
            json_object['Price']['AllowanceCharge']['Amount']['value'] = line_discount_amount
            
            
            json_object['Price']['PriceAmount'] = {}
            json_object['Price']['PriceAmount']['currencyID'] = row['line_currency']
            #json_object['Price']['PriceAmount']['value'] = str(row['line_extension_amount'] - row['line_discount'])
            json_object['Price']['PriceAmount']['value'] = unit_price
            

            #Advance
            # if len(row['advance_UUID']) > 0:
            #     json_object['DocumentReference'] = {}
            #     json_object['DocumentReference']['ID'] = row['advance_invoice_no']
            #     json_object['DocumentReference']['UUID'] = row['advance_UUID']
            #     json_object['DocumentReference']['IssueDate'] = row['advance_invoice_date']
                #json_object['DocumentReference']['IssueTime'] = row['']
                #json_object['DocumentReference']['InvoiceTypeCode'] = row['']
            
            
            
            #json_object['Price']['BaseQuantity'] = {}
            #json_object['Price']['BaseQuantity']['unitCode'] = row['unit_code']
            #json_object['Price']['BaseQuantity']['value'] = row['invoiced_quantity']
            
            json_object['InvoicedQuantity'] = {}
            json_object['InvoicedQuantity']['unitCode'] = row['unit_code']
            json_object['InvoicedQuantity']['value'] = float(row['invoiced_quantity'])
            
            json_object['LineExtensionAmount'] = {}
            json_object['LineExtensionAmount']['currencyID'] = row['line_currency']
            json_object['LineExtensionAmount']['value'] = line_extension_amount - line_discount_amount
            
            json_object['TaxTotal'] = {}
            json_object['TaxTotal']['TaxAmount'] = {}
            json_object['TaxTotal']['TaxAmount']['currencyID'] = row['line_currency']
            json_object['TaxTotal']['TaxAmount']['value'] = line_tax_amount
            
            json_object['TaxTotal']['RoundingAmount'] = {}
            json_object['TaxTotal']['RoundingAmount']['currencyID'] = row['line_currency']
            json_object['TaxTotal']['RoundingAmount']['value'] = line_total_amount
            
            
            json_array.append(json_object)
            if b == True:
                break
        
        return json_array
    except Exception as e: 
        lw.logRecord("Invoice Status Loading Failed :"+str(e))
    
    # Generate Tax Amount Data
def tax_json_array(df, exc_rate):
    total_tax = float(0.0)
    json_array = []
    
    json_object = {}
    try:
        # mdData = df.groupby(['tax_category_code',
        #                     'tax_percentage',
        #                     'tax_scheme',
        #                     'tax_currency_code',
        #                     'tax_exemption_code',
        #                     'tax_exemption_reason',
        #                     'currency_conv']).agg({'taxable_amount':'sum','tax_amount':'sum'}).reset_index()
        
        mdData = df.groupby(['tax_category_code',
                        'tax_percentage',
                        'tax_scheme',
                        'tax_currency_code',
                        'tax_exemption_code',
                        'tax_exemption_reason']).agg({'taxable_amount':'sum','tax_amount':'sum'}).reset_index()
        
        json_object['TaxSubtotal'] = []
        
        for _, row in mdData.iterrows():
            total_tax = total_tax+ float(row['tax_amount']) #*float(row['currency_conv'])
            tax_subtotal = {}
            tax_subtotal['TaxableAmount'] = {}
            tax_subtotal['TaxableAmount']['currencyID'] = row['tax_currency_code']
            tax_subtotal['TaxableAmount']['value'] = row['taxable_amount']
            
            tax_subtotal['TaxAmount'] = {}
            tax_subtotal['TaxAmount']['currencyID'] = row['tax_currency_code']
            tax_subtotal['TaxAmount']['value'] = row['tax_amount']
            
            tax_subtotal['TaxCategory'] = {}
            tax_subtotal['TaxCategory']['ID'] = row['tax_category_code']
            tax_subtotal['TaxCategory']['Percent'] = row['tax_percentage']
            tax_subtotal['TaxCategory']['TaxScheme'] = {}
            tax_subtotal['TaxCategory']['TaxScheme']['ID'] = row['tax_scheme'] 
            if row['tax_category_code'] == 'E' or row['tax_category_code'] == 'Z':

                row['tax_exemption_code'] = (row['tax_exemption_code']).replace("_","-")
                tax_subtotal['TaxCategory']['TaxExemptionReasonCode'] = row['tax_exemption_code']

                if row['tax_exemption_code'] == "VATEX-SA-29":
                    row['tax_exemption_reason'] = "Financial services mentioned in Article 29 of the VAT Regulations."
                elif row['tax_exemption_code'] == "VATEX-SA-29-7":
                    row['tax_exemption_reason'] = "Life insurance services mentioned in Article 29 of the VAT Regulations."
                elif row['tax_exemption_code'] == "VATEX-SA-30":
                    row['tax_exemption_reason'] = "Real estate transactions mentioned in Article 30 of the VAT Regulations."
                elif row['tax_exemption_code'] == "VATEX-SA-32":
                    row['tax_exemption_reason'] = "Export of goods."
                elif row['tax_exemption_code'] == "VATEX-SA-33":
                    row['tax_exemption_reason'] = "Export of services."
                elif row['tax_exemption_code'] == "VATEX-SA-34-1":
                    row['tax_exemption_reason'] = "The international transport of Goods."
                elif row['tax_exemption_code'] == "VATEX-SA-34-2":
                    row['tax_exemption_reason'] = "International transport of passengers."
                elif row['tax_exemption_code'] == "VATEX-SA-34-3":
                    row['tax_exemption_reason'] = "Services directly connected and incidental to a Supply of international passenger transport."
                elif row['tax_exemption_code'] == "VATEX-SA-34-4":
                    row['tax_exemption_reason'] = "Supply of a qualifying means of transport."
                elif row['tax_exemption_code'] == "VATEX-SA-34-5":
                    row['tax_exemption_reason'] = "Any services relating to Goods or passenger transportation, as defined in article twenty five of these Regulations."
                elif row['tax_exemption_code'] == "VATEX-SA-35":
                    row['tax_exemption_reason'] = "Medicines and medical equipment."
                elif row['tax_exemption_code'] == "VATEX-SA-36":
                    row['tax_exemption_reason'] = "Qualifying metals."
                elif row['tax_exemption_code'] == "VATEX-SA-EDU":
                    row['tax_exemption_reason'] = "Private education to citizen."
                elif row['tax_exemption_code'] == "VATEX-SA-HEA":
                    row['tax_exemption_reason'] = "Private healthcare to citizen."
                elif row['tax_exemption_code'] == "VATEX-SA-MLTRY":
                    row['tax_exemption_reason'] = "Supply of qualified military goods"
                elif row['tax_exemption_code'] == "VATEX-SA-OOS":
                    row['tax_exemption_reason'] = "The reason is a free text, has to be provided by the taxpayer on case to case basis."
                else:
                    row['tax_exemption_reason'] = ""

                tax_subtotal['TaxCategory']['TaxExemptionReason'] = {}
                tax_subtotal['TaxCategory']['TaxExemptionReason']['en'] = row['tax_exemption_reason']
                tax_subtotal['TaxCategory']['TaxExemptionReason']['ar'] = '' #'null'
            
            # json_object['TaxSubtotal'].append(tax_subtotal)

        json_array.append({
            "TaxAmount": {
                "currencyID": row['tax_currency_code'],
                "value": str(total_tax)
            }
        })
        
        # json_array.append(json_object)
        
        if str(row['tax_currency_code']) != 'SAR':
            json_array.append({
                    "TaxAmount": {
                        "currencyID": 'SAR',
                        "value": f"{(total_tax*exc_rate):.2f}"
                    },
                    "TaxSubtotal": [tax_subtotal]
                })
        
        return json_array
    except Exception as e: 
        lw.logRecord("Invoice Status Loading Failed :"+str(e))
    
#PDF Invoice Generation
def pdf_invoice_gener(invoiceNo , vat , inv_type , invoiceDate):
    
    invJson = {}
    invJson['invoiceNumber']    = invoiceNo,
    invJson['invoiceType']      = inv_type,  
    invJson['issueDate']        = invoiceDate,
    invJson['vat']              = vat
    
    return invJson
