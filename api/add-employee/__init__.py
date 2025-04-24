import os
import logging
import pyodbc
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    items = []
    quotedItems = ['firstName', 'lastName', 'displayName', 'phone', 'emailAddress', 'abcExpire', 'abcBookLocation']
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
            if itemDict[item] == 'None':
                sql += "NULL, "
            else:
                sql += "'" + itemDict[item] + "',"
        else:
            sql += itemDict[item] + ","

    sql = sql[:len(sql)-1]

    sql += ");"
    
    conn = pyodbc.connect(os.environ['DMCP_CONNECT_STRING'])
    cursor = conn.cursor()
    count = cursor.execute(sql)
    logging.info(sql)
    sqlLog = f"INSERT INTO ssc.sql_log (apiId, sqlCmd) VALUES ('add-employee', '{sql}');"
    logging.info(sqlLog)
    log = cursor.execute(sqlLog)

    conn.commit()
    
    sql = f"SELECT ssc.getEmpId({itemDict['locId']}, '{itemDict['firstName']}', '{itemDict['lastName']}') AS empId;"
    cursor.execute(sql)
    row = cursor.fetchone()
    empId = row.empId

    sql = f"EXEC ssc.updateIndividualServerShifts {empId};"
    cursor.execute(sql)

    conn.close()

    return func.HttpResponse(
        "success",
        status_code=200
    )
