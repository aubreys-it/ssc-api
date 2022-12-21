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
    sql = "SELECT * FROM ssc.server_info WHERE locId=" + locId + " AND ttd='9999-12-31' ORDER BY empId;"

    conn = pyodbc.connect(os.environ['DMCP_CONNECT_STRING'])
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    for row in rows:
        if row[0] not in servers.keys():
            servers[row[0]]={}
            servers[row[0]]['locId']=row[1]
            servers[row[0]]['firstName']=row[2]
            servers[row[0]]['lastName']=row[3]
            servers[row[0]]['displayName']=row[4]
            servers[row[0]]['phone']=row[5]
            servers[row[0]]['emailAddress']=row[6]
            servers[row[0]]['abcExpire']=str(row[7])
            servers[row[0]]['monAM']=row[8]
            servers[row[0]]['monPM']=row[9]
            servers[row[0]]['tueAM']=row[10]
            servers[row[0]]['tuePM']=row[11]
            servers[row[0]]['wedAM']=row[12]
            servers[row[0]]['wedPM']=row[13]
            servers[row[0]]['thuAM']=row[14]
            servers[row[0]]['thuPM']=row[15]
            servers[row[0]]['friAM']=row[16]
            servers[row[0]]['friPM']=row[17]
            servers[row[0]]['satAM']=row[18]
            servers[row[0]]['satPM']=row[19]
            servers[row[0]]['sunAM']=row[20]
            servers[row[0]]['sunPM']=row[21]
            servers[row[0]]['tfd']=row[22]
            servers[row[0]]['ttd']=row[23]
            servers[row[0]]['abcBookLocation']=row[24]

    if servers:
        return func.HttpResponse(json.dumps(servers))
    
