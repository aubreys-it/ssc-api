import logging
import os
import pyodbc
import json
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    locId = req.params.get('locId')
    weekStart = req.params.get('weekStart')
    if not locId and weekStart:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            locId = req_body.get('locId')
            weekStart = req_body.get('weekStart')

    weekStartDate = weekStart[:4] + '-' + weekStart[4:6] + '-' + weekStart[6:8]
    jsonDict = {}

    sql = "SELECT * FROM ssc.getSchedule(" + locId + ", '" + weekStartDate + "') ORDER BY shiftDate, dayPart, shiftNumber;"

    conn = pyodbc.connect(os.environ['DMCP_CONNECT_STRING'])
    cursor = conn.cursor()
    cursor.execute(sql)
    records = cursor.fetchall()
    cursor.close()
    conn.close()

    for row in records:
        if not row[6] in jsonDict.keys():
            jsonDict[row[6]] = {}
            jsonDict[row[6]]['shiftDay'] = row[7]
            jsonDict[row[6]]['shiftPart'] = row[8]
            jsonDict[row[6]]['shiftDate'] = str(row[5])
            jsonDict[row[6]]['servers'] = []

        serverDict = {}
        serverDict['locId'] = row[0]
        serverDict['empId'] = row[1]
        serverDict['displayName'] = row[2]
        serverDict['shiftNumber'] = row[3]
        serverDict['shiftDisplay'] = row[4]

        jsonDict[row[6]]['servers'].append(serverDict)

    if jsonDict:
        return func.HttpResponse(json.dumps(jsonDict))
    else:
        return func.HttpResponse(
             "Error processing schedule",
             status_code=200
        )
