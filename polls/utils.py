from typing import Dict
from django.shortcuts import redirect
from django.urls import reverse_lazy
import requests

from django.http import HttpResponseServerError

from polls.models import Score, Status


score_dict = {
    'Beginner': 50,
    'Amateur': 100,
    'PRO': 200,
}


def parse_question(url: str):
    try:
        response = requests.get(url)
    except Exception as error:
        return HttpResponseServerError(error)
    if not response.status_code == 200:
        return HttpResponseServerError(
            'Service not available. Please try again later')

    return response.json()


def update_score_status(status: Status, score: Score, data: Dict['str', int]):
    for value in data.values():

        if status.status != 'BEST':
            if status.status == 'Beginner' and score.points >= value:
                status.status = 'Amateur'
                score.points -= value
            elif status.status == 'Amateur' and score.points >= value:
                status.status = 'PRO'
                score.points -= value
            elif status.status == 'PRO' and score.points >= value:
                score.points -= value
                status.status = 'BEST'

            score.save()
            status.save()

    return redirect(reverse_lazy('polls:upgrade'))


def show_status_text(
        status: Status, score: Score, data: Dict['str', int]) -> Dict:
    # status, score -> text, upgrade

    for key, value in data.items():
        if status.status == key and score.points >= value:
            if status.status == 'Beginner':
                text = f'you can upgrade to Amateur ({value} points)'

                context = {
                    'text': text,
                    'status': status.status,
                    'score': score,
                    'upgrade': True
                }

                # return context
                
            if status.status == 'Amateur':

                text = f'you can upgrade to PRO ({value} points)'
                context = {
                    'text': text,
                    'status': status.status,
                    'score': score,
                    'upgrade': True
                }
                # return context
                
            if status.status == 'PRO':
                text = f'you can upgrade to BEST ({value} points)'
                context = {
                    'text': text,
                    'status': status.status,
                    'score': score,
                    'upgrade': True
                }
                # return context
                
            if status.status == 'BEST':
                context = {
                    'BEST': True,
                    'status': status.status,
                    'score': score,
                    }
        else:
            context = {
                'text': '''Not available to upgrade
                    <br>Amateur - 50 points<br>
                    PRO - 70 points
                    <br>BEST - 100 points''',
                'score': score,
                'status': status.status,
                }

    return context  
