import azure.functions as func
from flask_app import create_app

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return func.WsgiMiddleware(create_app()).handle(req, context)
