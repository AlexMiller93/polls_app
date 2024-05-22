import requests

from django.http import HttpResponseServerError


def parse_question(url: str):
    try:
        response = requests.get(url)
    except Exception as error:
        return HttpResponseServerError(error)
    if not response.status_code == 200:
        return HttpResponseServerError(
            'Service not available. Please try again later')

    return response.json()
