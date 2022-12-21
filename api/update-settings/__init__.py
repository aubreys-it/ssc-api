import logging
import os
import pyodbc
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    possFields = [
        'locId',
        'shiftId',
        'mustCallNeeded',
        'openShifts',
        'amTogo',
        'amBartenders',
        'autoRotateBar',
        'inTimes'
    ]

    quotedFields = ['amTogo', 'amBartenders', 'inTimes'] 
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

    if 'locId' in fieldDict.keys() and 'shiftId' in fieldDict.keys():
        sql = "UPDATE ssc.schedule_settings SET "
        
        for field in fields:
            if field not in ['locId', 'shiftId']:
                if field in quotedFields:
                    sql += field + "='" + fieldDict[field] + "',"
                else:
                    sql += field + "=" + fieldDict[field] + ","
        
        sql = sql[:len(sql)-1]
        sql += ' WHERE locId=' + fieldDict['locId'] + ' AND shiftId=' + fieldDict['shiftId'] + ';'

        conn = pyodbc.connect(os.environ['DMCP_CONNECT_STRING'])
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit
        
        cursor.close()
        conn.close()

        return func.HttpResponse(
                sql,
                status_code=200
            )
    else:

        return func.HttpResponse(
            "missing required fields",
            status_code=400
        )
