import azure.functions as func
from bonnette import Bonnette
import logging

from .main import app


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("7073 START")
    handler = Bonnette(app)
    logging.info(handler(req))
    return handler(req)
