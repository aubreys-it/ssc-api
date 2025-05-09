import logging
import os
import pyodbc
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    
    empId = req.params.get('empId')
    if not empId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            empId = req_body.get('empId')
    
    if empId:
        sql = 'DELETE FROM ssc.server_info WHERE empId=' + empId + ';'

        conn = pyodbc.connect(os.environ['DMCP_CONNECT_STRING'])
        cursor = conn.cursor()
        cursor.execute(sql)
        logging.info(sql)
        sql = sql.replace("'",":")
        sqlLog = f"INSERT INTO ssc.sql_log (apiId, sqlCmd) VALUES ('delete-employee', '{sql}');"
        logging.info(sqlLog)
        log = cursor.execute(sqlLog)

        conn.commit()
        
        return func.HttpResponse(f"success")
