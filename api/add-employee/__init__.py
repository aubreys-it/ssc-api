import os
import logging
import pyodbc
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        req_body = req.get_body()

    emailAddress=req_body.getitem('emailAddress')

    """
    items = []
    quotedItems = ['firstName', 'lastName', 'displayName', 'phone', 'emailAddress', 'abcExpireDate', 'tfd', 'ttd']

    for item in req_body:
        items.append(item)

    sql = "INSERT INTO ssc.insert_server_info ("
    for item in items:
        sql += item + ","

    sql = sql[:len(sql)-1] + ") VALUES ("

    for item in items:
        if item in quotedItems:
            sql += "'" + req_body[item] + "',"
        else:
            sql += req_body[item] + ","

    sql = sql[:len(sql)-1]

    sql += ");"
    
    
    #onn = pyodbc.connect(os.environ['DMCP_CONNECT_STRING'])
    #cursor = conn.cursor()
    #count = cursor.execute(sql)
    #conn.commit()
    """
    return func.HttpResponse(
        emailAddress,
        status_code=200
    )
