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

    sql = "SELECT * FROM ssc.staffing_levels WHERE locId=" + locId + " ORDER BY shiftId;"

    conn = pyodbc.connect(os.environ['DMCP_CONNECT_STRING'])
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    shifts = {}

    for row in rows:
        if not row[2] in shifts.keys():
            shifts[row[2]] = {}
            shifts[row[2]]['shift'] = row[1]
            shifts[row[2]]['shiftId'] = row[2]
            shifts[row[2]]['serversAvailable'] = row[3]
            shifts[row[2]]['serversNeeded'] = row[4]
            shifts[row[2]]['filledShifts'] = row[5]
            shifts[row[2]]['percentStaffed'] = row[6]
            
    if shifts:
        return func.HttpResponse(json.dumps(shifts))
    
