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

    daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    for row in records:
        if not row[7] in jsonDict.keys():
            jsonDict[row[7]] = {1: {}, 2: {}}
            
            for dayPart in jsonDict[row[7]]:
                jsonDict[row[7]][dayPart]['servers'] = []
                jsonDict[row[7]][dayPart]['togo'] = {'inTime': '', 'employees': []}
                jsonDict[row[7]][dayPart]['bartenders'] = []
                jsonDict[row[7]][dayPart]['hosts'] = []
                
            jsonDict[row[7]]['dayName'] = daysOfWeek[row[7] - 1]
            jsonDict[row[7]]['shiftDate'] = row[5]
        
        shiftDict = {}
        shiftDict['locId'] = row[0]
        shiftDict['empId'] = row[1]
        shiftDict['displayName'] = row[2]
        shiftDict['shiftNumber'] = row[3]
        shiftDict['shiftDisplay'] = row[4]
        shiftDict['inTimes'] = row[11]

        if row[9] == 'server':
            jsonDict[row[7]][row[8]]['servers'].append(shiftDict)
        elif row[9] == 'bar':
            jsonDict[row[7]][row[8]]['bartenders'].append(shiftDict)
        elif row[9] == 'togo':
            jsonDict[row[7]][row[8]]['togo']['employees'].append(shiftDict)
            jsonDict[row[7]][row[8]]['togo']['inTime'] = row[10]
        elif row[9] == 'host':
            jsonDict[row[7]][row[8]]['hosts'].append(shiftDict)

    if jsonDict:
        return func.HttpResponse(json.dumps(jsonDict))
    else:
        return func.HttpResponse(
             "Error processing schedule",
             status_code=200
        )
