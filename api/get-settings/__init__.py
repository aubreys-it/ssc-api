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

    sql = "SELECT * FROM ssc.schedule_settings WHERE locId=" + locId + " ORDER BY shiftId;"

    conn = pyodbc.connect(os.environ['DMCP_CONNECT_STRING'])
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    shifts = {}

    for row in rows:
        if not row[7] in shifts.keys():
            shifts[row[7]] = {}
            shifts[row[7]]['shiftName'] = row[0]
            shifts[row[7]]['mustCallNeeded'] = row[1]
            shifts[row[7]]['openShifts'] = row[2]
            shifts[row[7]]['togo'] = row[3]
            shifts[row[7]]['bartenders'] = row[4]
            shifts[row[7]]['autoRotateBar'] = row[5]
            shifts[row[7]]['inTimes'] = row[6]
            shifts[row[7]]['shiftId'] = row[7]
            shifts[row[7]]['dayNumber'] = row[8]
            shifts[row[7]]['dayPart'] = row[9]
            shifts[row[7]]['locId'] = row[10]
            shifts[row[7]]['togoInTime'] = row[11]
            shifts[row[7]]['showHosts'] = row[12]
            shifts[row[7]]['hosts'] = row[13]
            shifts[row[7]]['buildToShiftCount'] = row[14]
            shifts[row[7]]['manualRotationOffset'] = row[15]

    if shifts:
        return func.HttpResponse(json.dumps(shifts))
    
