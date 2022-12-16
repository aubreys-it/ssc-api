import logging
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    fields = ['name', 'city']
    fieldDict = {}
    for field in fields:
        fieldDict[field] = req.params.get(field)

        if not req.params.get(field):
            try:
                req_body = req.get_json()
            except ValueError:
                pass
            else:
                fieldDict[field] = req_body.get(field)

    """
    name = req.params.get('name')
    city = req.params.get("city")
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
            city = req_body.get('city')
    """

    #if name:
    if 'name' in fieldDict:
        #return func.HttpResponse(f"Hello, {name}. You live in {city}!")
        return func.HttpResponse(f"Hello, {fieldDict['name']}. You live in {fieldDict['city']}!")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
