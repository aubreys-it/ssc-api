import os
import logging
import pyodbc
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    items = []
    quotedItems = ['firstName', 'lastName', 'displayName', 'phone', 'emailAddress', 'abcExpire', 'tfd', 'ttd']
    unQuotedItems = ['locId', 'monAM', 'monPM', 'tueAM', 'tuePM', 'wedAM', 'wedPM', 'thuAM', 'thuPM', 'friAM', 'friPM', 'satAM', 'satPM', 'sunAM', 'sunPM']
    possItems = quotedItems + unQuotedItems

    itemDict = {}
    
    for item in possItems:
        itemDict[item] = str(req.params.get(item))

        if not req.params.get(item):
            try:
                req_body = req.get_json()
            except ValueError:
                pass
            else:
                itemDict[item] = str(req_body.get(item))

    for item in itemDict:
        items.append(item)

    sql = "INSERT INTO ssc.insert_server_info ("
    for item in items:
        sql += item + ","

    sql = sql[:len(sql)-1] + ") VALUES ("

    for item in items:
        if item in quotedItems:
            sql += "'" + itemDict[item] + "',"
        else:
            sql += itemDict[item] + ","

    sql = sql[:len(sql)-1]

    sql += ");"
    
    
    conn = pyodbc.connect(os.environ['DMCP_CONNECT_STRING'])
    cursor = conn.cursor()
    count = cursor.execute(sql)
    conn.commit()
    
    return func.HttpResponse(
        "success",
        status_code=200
    )
