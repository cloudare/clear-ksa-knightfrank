import json


dataJSON = '''{
				"clientName":"Azaq",
				"serviceName":"Cloudare",
				"car":null
			}'''
serverData = json.loads(dataJSON)


#URL Data
invoiceUrl  = 'https://api-sandbox.cleartax.com/middle-east/ksa/einvoicing/v2/einvoices/generate'
pdfURL = 'https://api-sandbox.cleartax.com/middle-east/ksa/einvoicing/v2/einvoices/print'
emailURL      = 'https://api-sandbox.cleartax.com/middle-east/ksa/einvoicing/v1/emails'


#Header Data
headToken   = '1.8e86a1b6-4f97-4a2a-b4f4-175794818e36_725da35c657477ba0cf153bbb438198bc0ec5788e933202ccc2f3c4c364e3197'
vat         = ['301244195200003','310377157300003']
branch      = 'SAGEX3'
deviceId    = ['15424900-8891-4ddd-935a-71a1da7ba6dc','5cb37939-4813-4429-9c82-4c9cffbfb9e1']
        
#Who column fixed value
createdBy = 'Cloudare'
updatedBy = 'Cloudare' 


#Database information SQLServer Main
driver_name = 'SQL SERVER'
server_ip   = 'sql-me-instance-01.e38804f8638f.database.windows.net'
username    = 'kfsa'
password    = 'Wby4gyMpufc5MVSy'
database    = 'CYGTST'
port        = '1433'


#SQL Query
headerTable  = '[CYGTST].[dbo].[ARINVHEADER_STAGING]'

inHeadCols = [
    'header_id',
    'BatchNo',
    'EntryNo',
    'device_id',
    'profile_id',
    'order_id_ar',
    'order_id_en',
    'invoice_class',
    'invoice_type',
    'export_transaction',
    'invoice_doc_ref_ar',
    'invoice_doc_ref_en',
    'order_ref_ar',
    'order_ref_en',
    'issue_date',
    'issue_time',
    'document_currency',
    'tax_currency',
    'supp_registration_name_ar',
    'supp_registration_name_en',
    'supp_company_vat',
    'supp_tax_scheme',
    'supp_party_identification_scheme',
    'supp_party_identification_value',
    'supp_treet_name_ar',
    'supp_street_name_en',
    'supp_additional_street_name_ar',
    'supp_additional_street_name_en',
    'supp_building_INT_ar',
    'supp_building_INT_en',
    'supp_plot_identification_ar',
    'supp_plot_identification_en',
    'supp_city_name_ar',
    'supp_city_name_en',
    'supp_city_subdivision_name_ar',
    'supp_city_subdivision_name_en',
    'supp_postal_zone',
    'supp_country_subentity_ar',
    'supp_country_subentity_en',
    'supp_country_identification_code',
    'buyer_registration_name_ar',
    'buyer_registration_name_en',
    'buyer_company_vat',
    'buyer_tax_scheme',
    'buyer_party_identification_scheme',
    'buyer_party_identification_value',
    'buyer_street_name_ar',
    'buyer_street_name_en',
    'buyer_additional_street_name_ar',
    'buyer_additional_street_name_en',
    'buyer_building_INT_ar',
    'buyer_building_INT_en',
    'buyer_plot_identification_ar',
    'buyer_plot_identification_en',
    'buyer_city_name_ar',
    'buyer_city_name_en',
    'buyer_city_subdivision_name_ar',
    'buyer_city_subdivision_name_en',
    'buyer_postal_zone',
    'buyer_country_subentity_ar',
    'buyer_country_subentity_en',
    'buyer_country_identification_code',
    'total_line_extension_amount',
    'total_line_tax_amount',
    'total_line_amount',
    'total_discount_amount',
    'total_discount_tax',
    'total_discount_reason_en',
    'total_prepaid_amount',
    'total_payable_amount',
    'total_payable_rounding_amount',
    'note_ar',
    'note_en',
    'credit_memo_reason',
    'payment_means_code',
    'linked_transaction_no',
    'error_message'
    'BankName',
    'Account_Name',
    'Account_No',
    'Bank_Address',
    'Currency',
    'SwiftCode',
    'IBAN_NO',
    'buyer_email',
    'Invoice_Exchange_Rate']

outHeadCols = [
            'header_id',
            'BatchNo',
            'EntryNo',
            'TRIM(device_id)',
            'profile_id',
            'TRIM(order_id_ar)',
            'TRIM(order_id_en)',
            'invoice_class',
            'TRIM(invoice_type)',
            'TRIM(export_transaction)',
            'TRIM(invoice_doc_ref_ar)',
            'TRIM(invoice_doc_ref_en)',
            'TRIM(order_ref_ar)',
            'TRIM(order_ref_en)',
            'issue_date',
            'issue_time',
            'TRIM(document_currency)',
            'TRIM(tax_currency)',
            'TRIM(supp_registration_name_ar)',
            'TRIM(supp_registration_name_en)',
            'supp_company_vat',
            'TRIM(supp_tax_scheme)',
            'TRIM(supp_party_identification_scheme)',
            'TRIM(supp_party_identification_value)',
            'TRIM(supp_treet_name_ar)',
            'TRIM(supp_street_name_en)',
            'TRIM(supp_additional_street_name_ar)',
            'TRIM(supp_additional_street_name_en)',
            'TRIM(supp_building_INT_ar)',
            'TRIM(supp_building_INT_en)',
            'TRIM(supp_plot_identification_ar)',
            'TRIM(supp_plot_identification_en)',
            'TRIM(supp_city_name_ar)',
            'TRIM(supp_city_name_en)',
            'TRIM(supp_city_subdivision_name_ar)',
            'TRIM(supp_city_subdivision_name_en)',
            'TRIM(supp_postal_zone)',
            'TRIM(supp_country_subentity_ar)',
            'TRIM(supp_country_subentity_en)',
            'TRIM(supp_country_identification_code)',
            'TRIM(buyer_registration_name_ar)',
            'TRIM(buyer_registration_name_en)',
            'TRIM(buyer_company_vat)',
            'TRIM(buyer_tax_scheme)',
            'TRIM(buyer_party_identification_scheme)',
            'TRIM(buyer_party_identification_value)',
            'TRIM(buyer_street_name_ar)',
            'TRIM(buyer_street_name_en)',
            'TRIM(buyer_additional_street_name_ar)',
            'TRIM(buyer_additional_street_name_en)',
            'TRIM(buyer_building_INT_ar)',
            'TRIM(buyer_building_INT_en)',
            'TRIM(buyer_plot_identification_ar)',
            'TRIM(buyer_plot_identification_en)',
            'TRIM(buyer_city_name_ar)',
            'TRIM(buyer_city_name_en)',
            'TRIM(buyer_city_subdivision_name_ar)',
            'TRIM(buyer_city_subdivision_name_en)',
            'TRIM(buyer_postal_zone)',
            'TRIM(buyer_country_subentity_ar)',
            'TRIM(buyer_country_subentity_en)',
            'TRIM(buyer_country_identification_code)',
            'total_line_extension_amount',
            'total_line_tax_amount',
            'total_line_amount',
            'total_discount_amount',
            'total_discount_tax',
            'TRIM(total_discount_reason_en)',
            'total_prepaid_amount',
            'total_payable_amount',
            'total_payable_rounding_amount',
            'TRIM(note_ar)',
            'TRIM(note_en)',
            'TRIM(credit_memo_reason)',
            'TRIM(payment_means_code)',
            'TRIM(linked_transaction_no)',
            'TRIM(error_message)',
            'TRIM(BankName)',
            'TRIM(Account_Name)',
            'TRIM(Account_No)',
            'TRIM(Bank_Address)',
            'TRIM(Currency)',
            'TRIM(SwiftCode)',
            'TRIM(IBAN_NO)',    
            'TRIM(buyer_email)',
            'Invoice_Exchange_Rate']
#Invoice Column            
invoiceTable  = '[CYGTST].[dbo].[ARINVDETAIL_STAGING]'


# inInvoCol  = [
#             'NUM_0',
#             'ZLINE_0',
#             'ZITMREFAR_0',
#             'ZITMREFEN_0',
#             'ZCUSITMAR_0',
#             'ZCUSITMEN_0',
#             'ZSELITMAR_0',
#             'ZSELITMEN_0',
#             'ZSTDITMAR_0',
#             'ZSTDITMEN_0',
#             'ZTAXCAT_0',
#             'ZATXPER_0',
#             'ZTAXSCH_0',
#             'ZCUR_0',
#             'ZUOM_0',
#             'GROPRI_0',
#             'QTY_0',
#             'ZINVTOTNOT_0',
#             'ZINVTOTAX_0',
#             'ZINVTOTATI_0',
#             'ZLINDISAMT_0',
#             'ZLINDISTAX_0',
#             'ZLINDISREN_0',
#             'ZLINDISRAR_0',
#             'ZADVUUID_0',
#             'ZADVINVNUM_0',
#             'ZADVINVDAT_0',
#             'ZADVTAMT_0',
#             'ZADVTAX_0'
#                 ]
outInvoCol = [
                'line_id',
                'header_id',
                'line_INT',
                'TRIM(item_name_ar)',
                'TRIM(item_name_en)',
                'TRIM(buyers_item_id_ar)',
                'TRIM(buyers_item_id_en)',
                'TRIM(sellers_item_id_ar)',
                'TRIM(sellers_item_id_en)',
                'TRIM(standard_item_id_ar)',
                'TRIM(standard_item_id_en)',
                'TRIM(item_tax_category)',
                'item_tax_category_percent',
                'TRIM(item_tax_scheme)',
                'TRIM(tax_exemption_reason)',
                'TRIM(tax_exemption_code)',
                'TRIM(line_currency)',
                'TRIM(unit_code)',
                'unit_price',
                'invoiced_quantity',
                'line_extension_amount',
                'line_tax_amount',
                'line_total_amount',
                'line_discount_amount',
                'line_discount_tax',
                'TRIM(line_discount_reason_en)',
                'TRIM(line_discount_reason_ar)'#,
                # 'advance_UUID',		 
                # 'advance_invoice_no',		 
                # 'advance_invoice_date',		 
                # 'advance_taxable_amount',		
                # 'avdnace_tax_amount'		
            ]           

inInvoCol = [
    'line_id',
    'header_id',
    'line_INT',
    'item_name_ar',
    'item_name_en',
    'buyers_item_id_ar',
    'buyers_item_id_en',
    'sellers_item_id_ar',
    'sellers_item_id_en',
    'standard_item_id_ar',
    'standard_item_id_en',
    'item_tax_category',
    'item_tax_category_percent',
    'item_tax_scheme',
    'tax_exemption_reason',
    'tax_exemption_code',
    'line_currency',
    'unit_code',
    'unit_price',
    'invoiced_quantity',
    'line_extension_amount',
    'line_tax_amount',
    'line_total_amount',
    'line_discount_amount',
    'line_discount_tax',
    'line_discount_reason_en',
    'line_discount_reason_ar'
    # 'advance_UUID',		 
    # 'advance_invoice_no',		 
    # 'advance_invoice_date',		 
    # 'advance_taxable_amount',		
    # 'avdnace_tax_amount'		
] 
            
#Tax
inTaxCol =[
    'header_id',
    'line_extension_amount',
    'TRIM(line_currency)',
    'line_tax_amount',
    'TRIM(item_tax_category)',
    'item_tax_category_percent',
    'TRIM(item_tax_scheme)',
    'TRIM(tax_exemption_reason)',
    'TRIM(tax_exemption_code)'
    # 'ZEXCRATE_0'
]

taxTable = '[CYGTST].[dbo].[ARINVDETAIL_STAGING]'

outTaxCol = [
    'header_id',
    'taxable_amount',
    'tax_currency_code',
    'tax_amount',
    'tax_category_code',
    'tax_percentage',
    'tax_scheme',
    'tax_exemption_reason',
    'tax_exemption_code'
    # 'currency_conv'
    ]

headerTable_error = '[CYGTST].[dbo].[ARINVHEADER_STAGING_ERROR]'