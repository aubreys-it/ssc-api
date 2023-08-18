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

    availShiftColumns = ['monAm', 'monPm', 'tueAm', 'tuePm', 'wedAm', 'wedPm', 'thuAm', 'thuPm', 'friAm', 'friPm', 'satAm', 'satPm', 'sunAm', 'sunPm']
    shiftNumberColumns = ['monAMShiftNumber', 'monPMShiftNumber', 'tueAMShiftNumber', 'tuePMShiftNumber', 'wedAMShiftNumber', 'wedPMShiftNumber', 'thuAMShiftNumber', 'thuPMShiftNumber', 'friAMShiftNumber', 'friPMShiftNumber', 'satAMShiftNumber', 'satPMShiftNumber', 'sunAMShiftNumber', 'sunPMShiftNumber']
    availServers = []

    conn = pyodbc.connect(os.environ['DMCP_CONNECT_STRING'])
    cursor = conn.cursor()
    
    sql = "SELECT * FROM ssc.schedule_settings WHERE locId=" + locId + " ORDER BY shiftId;"
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
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

    for i in range(0, len(availShiftColumns)):
        sql  = "SELECT empId, firstName, lastName, displayName, " + shiftNumberColumns[i] + " FROM ssc.server_info \
                WHERE " + availShiftColumns[i] + "=1 AND locId=" + locId + " ORDER BY " + shiftNumberColumns[i] + ";"
        
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            availServers.append({
                'empId': row[0],
                'firstName': row[1],
                'lastName': row[2],
                'displayName': row[3],
                'shiftNumber': row[4]
            })

        shifts[availShiftColumns[i]] = availServers
        availServers = []
        
    cursor.close()
    conn.close()

    if shifts:
        return func.HttpResponse(json.dumps(shifts))
    
