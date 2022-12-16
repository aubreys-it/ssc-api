import logging
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    #name = req.params.get('name')
    #city = req.params.get("city")
    #req_body = req.get_json()
    req_body = req.get_body()
    name = req_body.get('name')
    city = req_body.get('city')
    """
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
            city = req_body.get('city')
    """
    if name:
        return func.HttpResponse(f"Hello, {name}. You live in {city}!")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
