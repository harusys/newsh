import azure.functions as func
from bonnette import Bonnette
import logging

from .main import app


def main(req: func.HttpRequest) -> func.HttpResponse:
    handler = Bonnette(app)
    return handler(req)