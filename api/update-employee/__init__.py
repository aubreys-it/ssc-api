import logging
import os
import pyodbc
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    possFields = [
        'empId',
        'locId',
        'firstName',
        'lastName',
        'displayName',
        'phone',
        'emailAddress',
        'abcExpire',
        'monAM',
        'monPM',
        'tueAM',
        'tuePM',
        'wedAM',
        'wedPM',
        'thuAM',
        'thuPM',
        'friAM',
        'friPM',
        'satAM',
        'satPM',
        'sunAM',
        'sunPM',
        'tfd',
        'ttd'
    ]

    quotedFields = ['firstName', 'lastName', 'displayName', 'phone', 'emailAddress', 'abcExpire', 'tfd', 'ttd']
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
        fields.append(field)

    if 'empId' in fieldDict:
        sql = "UPDATE ssc.server info SET "
        
        for field in fields:
            if field != 'empId':
                if field in quotedFields:
                    sql += field + "='" + fieldDict[field] + "',"
                else:
                    sql += field + "=" + fieldDict[field] + ","
        
        sql = sql[:len(sql)-1]
        sql += ' WHERE empId=' + fieldDict['empId'] + ';'

        #conn = pyodbc.connect(os.environ['DMCP_CONNECT_STRING'])
        #cursor = conn.cursor()
        #cursor.execute(sql)
        #conn.commit()
    
        return func.HttpResponse(
            sql,
            status_code=200
        )
    else:

        return func.HttpResponse(
            "no empId provided",
            status_code=400
        )