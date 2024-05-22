from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from core.settings import URL_BOOL, URL_MULTIPLE
from polls.models import Score, Status, Question
from polls.utils import parse_question

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        if not Status.objects.filter(user=request.user).exists():
            Status.objects.create(user=request.user, status='Beginner')
        status = Status.objects.get(user=request.user)
        if not Score.objects.filter(user=request.user).exists():
            Score.objects.create(user=request.user)
        score = Score.objects.get(user=request.user)
        return render(
            request,
            template_name='polls/index.html',
            context={
                'score': score,
                'status': status.status
            })
    return render(request, template_name='polls/index.html',)


@login_required
def quiz(request):
    # get status
    if not Status.objects.filter(user=request.user).exists():
        Status.objects.create(user=request.user)
    status = Status.objects.get(user=request.user)

    # get score
    if not Score.objects.filter(user=request.user).exists():
        Score.objects.create(user=request.user)
    score = Score.objects.get(user=request.user)
    current_score = score.points

    if request.method == 'POST':
        if not Question.objects.filter(user=request.user).exists():
            return redirect(reverse_lazy('polls:quiz'))

        question = get_object_or_404(Question, user=request.user)
        user_answer = request.POST.get('user_answer')

        if question.correct_answer == user_answer and \
                question.text == request.POST.get('question'):
            current_score += 1
            score.points = current_score

            score.save()

        correct_answer = question.correct_answer
        text = question.text
        question.delete()

        context = {
            'correct_answer': correct_answer,
            'results': [{'question': text}],
            'score': score,
            'is_answered': True,
            'status': status.status
        }

        return render(
            request,
            template_name='polls/quiz.html',
            context=context
        )

    else:
        json_data = parse_question(URL_BOOL)

        if not Question.objects.filter(user=request.user).exists():
            Question.objects.create(user=request.user)

        question = Question.objects.get(user=request.user)

        question.category = json_data['results'][0]['category']
        question.question_type = json_data['results'][0]['type']
        question.difficulty = json_data['results'][0]['difficulty']
        question.text = json_data['results'][0]['question']
        question.correct_answer = json_data['results'][0]['correct_answer']

        question.save()

        context = {
            'results': json_data['results'],
            'score': score,
            'status': status.status,
        }

        return render(
            request,
            template_name='polls/quiz.html',
            context=context
        )


@login_required
def quiz_multiple(request):

    # get status
    if not Status.objects.filter(user=request.user).exists():
        Status.objects.create(user=request.user)
    status = Status.objects.get(user=request.user)

    # get score
    if not Score.objects.filter(user=request.user).exists():
        Score.objects.create(user=request.user)
    score = Score.objects.get(user=request.user)

    current_score = score.points

    if request.method == 'POST':
        if not Question.objects.filter(user=request.user).exists():
            return redirect(reverse_lazy('polls:quiz_multiple'))

        question = Question.objects.get(user=request.user)
        user_answer = request.POST.get('user_answer')
        is_answered = False

        # if question.text != request.POST.get('question'):
        #     return redirect(reverse_lazy('polls:quiz_multiple'))

        if question.correct_answer == user_answer:
            current_score += 5
            score.points = current_score
            score.save()
            is_answered = True

        correct_answer = question.correct_answer
        text = question.text

        answers = [
            question.answer1,
            question.answer2,
            question.answer3,
            question.answer4
            ]

        question.delete()

        context = {
            'correct_answer': correct_answer,
            'results': [{'question': text, }],
            'answers': answers,
            'score': score,
            'is_answered': is_answered,
            'status': status.status
        }

        return render(
            request,
            template_name='polls/quiz_multiple.html',
            context=context
        )

    json_data = parse_question(URL_MULTIPLE)

    if not Question.objects.filter(user=request.user).exists():
        Question.objects.create(user=request.user)

    question = Question.objects.get(user=request.user)
    question.category = json_data['results'][0]['category']
    question.type = json_data['results'][0]['type']
    question.difficulty = json_data['results'][0]['difficulty']
    question.question = json_data['results'][0]['question']
    question.correct_answer = json_data['results'][0]['correct_answer']
    question.incorrect_answers = json_data['results'][0]['incorrect_answers']

    all_answers = list(
        {
            *json_data['results'][0]['incorrect_answers'],
            json_data['results'][0]['correct_answer']
        }
    )

    question.answer1 = all_answers[0]
    question.answer2 = all_answers[1]
    question.answer3 = all_answers[2]
    question.answer4 = all_answers[3]

    question.save()

    context = {
        'results': json_data['results'],
        'score': score,
        'answers': [
            question.answer1,
            question.answer2,
            question.answer3,
            question.answer4
        ],
        'status': status.status
    }

    return render(
        request,
        template_name='polls/quiz_multiple.html',
        context=context
        )
