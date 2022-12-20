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
        if not row['shiftNameDisplay'] in jsonDict:
            jsonDict[row['shiftNameDisplay']] = {}
            jsonDict[row['shiftNameDisplay']]['shiftDay'] = row['shiftDay']
            jsonDict[row['shiftNameDisplay']]['shiftPart'] = row['dayPart']
            jsonDict[row['shiftNameDisplay']]['shiftDate'] = row['shiftDate']
            jsonDict[row['shiftNameDisplay']]['servers'] = []

        serverDict = {}
        serverDict['locId'] = row['locId']
        serverDict['empId'] = row['empId']
        serverDict['displayName'] = row['displayName']
        serverDict['shiftNumber'] = row['shiftNumber']
        serverDict['shiftDisplay'] = row['shiftDisplay']

        jsonDict[row['shiftNameDisplay']]['servers'].append(serverDict)

    if jsonDict:
        return func.HttpResponse(json.dumps(jsonDict))
    else:
        return func.HttpResponse(
             "Error processing schedule",
             status_code=200
        )
