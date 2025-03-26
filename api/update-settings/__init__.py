import logging
import os
import pyodbc
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    possFields = [
        'locId',
        'shiftId',
        'mustCallNeeded',
        'openShifts',
        'togo',
        'bartenders',
        'autoRotateBar',
        'inTimes',
        'togoInTime',
        'hosts',
        'buildToShiftCount',
        'manualRotationOffset',
        'serverJson'
    ]

    shiftNumberColumns = [
        'monAMShiftNumber',
        'monPMShiftNumber',
        'tueAMShiftNumber',
        'tuePMShiftNumber',
        'wedAMShiftNumber',
        'wedPMShiftNumber',
        'thuAMShiftNumber',
        'thuPMShiftNumber',
        'friAMShiftNumber',
        'friPMShiftNumber',
        'satAMShiftNumber',
        'satPMShiftNumber',
        'sunAMShiftNumber',
        'sunPMShiftNumber'
    ]

    quotedFields = ['togo', 'bartenders', 'inTimes', 'togoInTime', 'togoInTime', 'hosts'] 
    fields = []
    fieldDict = {}

    for field in possFields:
        fieldDict[field] = str(req.params.get(field))

        if not req.params.get(field):
            try:
                req_body = req.get_json()
            except ValueError:
                pass
            else:
                fieldDict[field] = str(req_body.get(field))

    for field in fieldDict:
        if fieldDict[field] != 'None':
            fields.append(field)

    logging.info(fieldDict)
    logging.info(fields)

    conn = pyodbc.connect(os.environ['DMCP_CONNECT_STRING'])
    cursor = conn.cursor()

    if 'locId' in fieldDict.keys() and 'shiftId' in fieldDict.keys():

        # get buildToShiftCount before update
        sql = "SELECT buildToShiftCount FROM ssc.schedule_settings WHERE locId=" + fieldDict['locId'] + " AND shiftId=" + fieldDict['shiftId'] + ";"
        logging.info("Old BTSC")
        logging.info(sql)
        cursor.execute(sql)
        oldBTSC = cursor.fetchone()[0]
        logging.info(str(oldBTSC))

        sql = "UPDATE ssc.schedule_settings SET "
        
        for field in fields:
            if field not in ['locId', 'shiftId', 'serverJson']:
                if field in quotedFields:
                    sql += field + "='" + fieldDict[field] + "',"
                else:
                    sql += field + "=" + fieldDict[field] + ","
            elif field == 'serverJson':
                serverJson = json.loads(fieldDict[field])
                for server in serverJson:
                    jsonSql = "UPDATE ssc.server_info SET " + shiftNumberColumns[int(fieldDict['shiftId'])-1] + \
                        "=" + str(server['shiftNumber']) + " WHERE empId=" + str(server['empId']) + ";"        
                    
                    logging.info(jsonSql)
                    cursor.execute(jsonSql)
                    conn.commit()

        
        sql = sql[:len(sql)-1]
        sql += ' WHERE locId=' + fieldDict['locId'] + ' AND shiftId=' + fieldDict['shiftId'] + ';'
        
        logging.info(sql)
        cursor.execute(sql)
        conn.commit()

        # get buildToShiftCount after update
        sql = "SELECT buildToShiftCount FROM ssc.schedule_settings WHERE locId=" + fieldDict['locId'] + " AND shiftId=" + fieldDict['shiftId'] + ";"
        logging.info("New BTSC")
        logging.info(sql)
        cursor.execute(sql)
        newBTSC = cursor.fetchone()[0]
        logging.info(str(newBTSC))

        # update manualRotationOffset for locations running v2 of ssc
        if fieldDict['locId'] in ('0', '2', '12', '13', '14', '17', '18'):
            if oldBTSC != newBTSC:
                sql = "UPDATE ssc.schedule_settings SET manualRotationOffset=manualRotationOffset + " + str(oldBTSC - newBTSC)
                sql += " WHERE locId=" + fieldDict['locId'] + " AND shiftId=" + fieldDict['shiftId'] + ";"
                logging.info("Update BTSC")
                logging.info(sql)
                cursor.execute(sql)

        conn.commit()
        
        cursor.close()
        conn.close()

        return func.HttpResponse(
                "success",
                status_code=200
            )
    else:

        return func.HttpResponse(
            "missing required fields",
            status_code=400
        )
