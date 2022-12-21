import logging
import os
import pyodbc
import json
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    locId = req.params.get('locId')
    if not locId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            locId = req_body.get('locId')
            
    servers = {}
    sql = "SELECT * FROM ssc.server_info WHERE locId=" + locId + " AND ttd='9999-12-31' ORDER BY lastName, firstName;"

    conn = pyodbc.connect(os.environ['DMCP_CONNECT_STRING'])
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    rowId = 0

    for row in rows:
        if rowId not in servers.keys():
            servers[rowId]={}
            servers[rowId]['empId']=row[0]
            servers[rowId]['locId']=row[1]
            servers[rowId]['firstName']=row[2]
            servers[rowId]['lastName']=row[3]
            servers[rowId]['displayName']=row[4]
            servers[rowId]['phone']=row[5]
            servers[rowId]['emailAddress']=row[6]
            servers[rowId]['abcExpire']=str(row[7])
            servers[rowId]['monAM']=row[8]
            servers[rowId]['monPM']=row[9]
            servers[rowId]['tueAM']=row[10]
            servers[rowId]['tuePM']=row[11]
            servers[rowId]['wedAM']=row[12]
            servers[rowId]['wedPM']=row[13]
            servers[rowId]['thuAM']=row[14]
            servers[rowId]['thuPM']=row[15]
            servers[rowId]['friAM']=row[16]
            servers[rowId]['friPM']=row[17]
            servers[rowId]['satAM']=row[18]
            servers[rowId]['satPM']=row[19]
            servers[rowId]['sunAM']=row[20]
            servers[rowId]['sunPM']=row[21]
            servers[rowId]['tfd']=str(row[22])
            servers[rowId]['ttd']=str(row[23])
            servers[rowId]['abcBookLocation']=row[24]

            rowId += 1

    if servers:
        return func.HttpResponse(json.dumps(servers))
    
