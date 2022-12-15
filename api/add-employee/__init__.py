import os
import logging
import pyodbc


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        pass

    sql = "INSERT INTO ssc.insert_server_info VALUES "
    sql += "(" + req_body['locId'] + "),"
    sql += "('" + req_body['firstName'] + "'),"
    sql += "('" + req_body['lastName'] + "'),"
    sql += "('" + req_body['displayName'] + "'),"
    sql += "('" + req_body['phone'] + "'),"
    sql += "('" + req_body['emailAddress'] + "'),"
    sql += "('" + req_body['abcExpirationDate'] + "'),"
    sql += "(" + req_body['monAM'] + "),"
    sql += "(" + req_body['monPM'] + "),"
    sql += "(" + req_body['tueAM'] + "),"
    sql += "(" + req_body['tuePM'] + "),"
    sql += "(" + req_body['wedAM'] + "),"
    sql += "(" + req_body['wedPM'] + "),"
    sql += "(" + req_body['thuAM'] + "),"
    sql += "(" + req_body['thuPM'] + "),"
    sql += "(" + req_body['friAM'] + "),"
    sql += "(" + req_body['friPM'] + "),"
    sql += "(" + req_body['satAM'] + "),"
    sql += "(" + req_body['satPM'] + "),"
    sql += "(" + req_body['sunAM'] + "),"
    sql += "(" + req_body['sunPM'] + "),"
    sql += "('" + req_body['tfd'] + "'),"
    sql += "('" + req_body['ttd'] + "');"
    
    conn = pyodbc.connect(os.environ['DMCP_CONNECT_STRING'])
    cursor = conn.cursor()
    count = cursor.execute(sql)
    conn.commit()

    return func.HttpResponse(
        count,
        status_code=200
    )
