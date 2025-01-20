import serverData as sd
import pandas as pd
#import pypyodbc as odbc
import pyodbc as odbc

def connection():
    driver_name = sd.driver_name
    server_ip   = sd.server_ip
    username    = sd.username
    password    = sd.password
    database    = sd.database  
    port        = sd.port
    
    conn_str = f'DRIVER={{SQL Server}};SERVER={server_ip},{port};DATABASE={database};UID={username};PWD={password};'
    
    #conn_str = f'DRIVER={{SQL Server}};SERVER={server_ip};DATABASE={database};trusted_connection=yes;'
    
    conn = odbc.connect(conn_str)
    #conn.setdecoding(odbc.SQL_CHAR, encoding='utf-8')
    #conn.setdecoding(odbc.SQL_WCHAR, encoding='utf-8')
    #conn.setdecoding(odbc.SQL_WMETADATA, encoding='utf-8')
    #conn.setdecoding(encoding='utf-8')
    
    return conn

#Select table from the DB
def dbSelect(sql, col):
    mydb = connection()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    df = pd.DataFrame((tuple(t) for t in myresult))
    #df = pd.DataFrame(myresult)
    if len(df) >0:
        df.columns = col
        
    # mycursor.close()
    # mydb.close()
    return df, mycursor, mydb

#Insert or Update to DB
def dbInsert(sql):
    mydb = connection()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()
    return mycursor.rowcount


#Insert or Update to DB
def dbInsert_many(sql, values):
    mydb = connection()
    mycursor = mydb.cursor()
    mycursor.executemany(sql, values)
    mydb.commit()
    mycursor.close()
    mydb.close()
    return mycursor.rowcount
    
#Generate Select SQL    
def SelectData(inCols, tableName, whereClause, outCols):
    colData = ', '.join(inCols)
    sql = "SELECT "+colData+" FROM "+tableName
    if whereClause != "":
        sql = sql +" WHERE "+whereClause
    
    print(sql)
    data, conn, mydb = dbSelect(sql, outCols)
    print(data)
    return data, conn, mydb

#Generate Update SQL
def updateDataSQL(whoCol,tableName,whereClause,inData):
    colData = '= ?, '.join(whoCol)
    colData = colData+'= ?'
    sql = 'UPDATE '+tableName+' SET '+colData+' where '+whereClause+';'
    print(sql)
    formatted_query = sql
    for val in inData:
        # Format each value appropriately for SQL (add quotes if it's a string)
        if isinstance(val, str):
            val_str = f"'{val}'"
        else:
            val_str = f"'{str(val).replace("[","").replace("]","").replace("{","").replace("}","").replace("'",'')}'"
        # Replace the first occurrence of '?' with the formatted value
        formatted_query = formatted_query.replace('?', val_str, 1)
    # formatted_query = formatted_query
    print("Formatted SQL Query:", formatted_query)
    dat  = dbInsert(formatted_query)

#Execute SQL    
def sqlExecute(sql):
    mydb = connection()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()
    return mycursor.rowcount
    

def sqlUpdate(sql,InvoiceId,errorMes):
    mydb = connection()
    mycursor = mydb.cursor()
    mycursor.execute(sql,errorMes,InvoiceId)
    mydb.commit()
    mycursor.close()
    mydb.close()
