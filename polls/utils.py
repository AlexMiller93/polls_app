from typing import Dict, List
from django.shortcuts import redirect
from django.urls import reverse_lazy
import requests

from django.http import HttpResponseServerError

# from polls.models import Question, Score, Status

''' 
def parse_question(url: str, is_multiple: bool):
    if is_multiple:
        url += 'multiple'
    else:
        url += 'boolean'

    try:
        response = requests.get(url)
    except Exception as error:
        return HttpResponseServerError(error)
    if response.status_code != 200:
        return HttpResponseServerError(
            'Service not available. Please try again later')

    return response.json()


def update_score_status(
        status: Status, score: Score, data: Dict['str', int]) -> None:
    for key, value in data.items():

        if status.status != 'BEST':
            if key == 'Beginner' and score.points >= value:
                status.status = 'Amateur'
                score.points -= value
            elif key == 'Amateur' and score.points >= value:
                status.status = 'PRO'
                score.points -= value
            elif key == 'PRO' and score.points >= value:
                score.points -= value
                status.status = 'BEST'

            score.save()
            status.save()

    return redirect(reverse_lazy('polls:upgrade'))


def update_score_status_2(
        status: Status, score: Score, data: Dict['str', int]) -> None:
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
                'text': """Not available to upgrade
                    <br>Amateur - 50 points<br>
                    PRO - 70 points
                    <br>BEST - 100 points""",
                'score': score,
                'status': status.status,
                }

    return context  


def get_question_answers(question: Question, data) -> List:
    question.category = data['results'][0]['category']
    question.type = data['results'][0]['type']
    question.difficulty = data['results'][0]['difficulty']
    question.question = data['results'][0]['question']
    question.correct_answer = data['results'][0]['correct_answer']
    question.incorrect_answers = data['results'][0]['incorrect_answers']

    all_answers = list(
        {
            *data['results'][0]['incorrect_answers'],
            data['results'][0]['correct_answer']
        }
    )

    question.answer1 = all_answers[0]
    question.answer2 = all_answers[1]
    question.answer3 = all_answers[2]
    question.answer4 = all_answers[3]

    question.save()

    answers_lst = [
        question.answer1,
        question.answer2,
        question.answer3,
        question.answer4,
    ]

    return answers_lst
'''