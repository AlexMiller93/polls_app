from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from core.settings import URL
from polls.models import Score, Status, Question
from polls.utils import parse_question, update_score_status

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


def top_users(request):
    best = Status.objects.filter(status='BEST').values('user')
    bests = Score.objects.order_by('-points').filter(user__in=best)[:3]
    prof = Status.objects.filter(status='PRO').values('user')
    best_prof = Score.objects.order_by('-points').filter(user__in=prof)[:3]
    amateurs = Status.objects.filter(status='Amateur').values('user')
    best_amateurs = Score.objects.order_by('-points').filter(user__in=amateurs)[:3]

    if request.user.is_authenticated:

        status = Status.objects.get(user=request.user)

        score = Score.objects.get(user=request.user)

        context = {
            'score': score,
            'bests': bests,
            'prof': best_prof,
            'amateurs': best_amateurs,
            'status': status.status}

        return render(
            request,
            template_name='polls/top_users.html',
            context=context
        )

    context = {
        'bests': bests,
        'prof': best_prof,
        'amateurs': best_amateurs
    }

    return render(
        request,
        template_name='polls/top_users.html',
        context=context)


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

        if question.correct_answer == user_answer:
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
            'is_right_answered': True,
            'status': status.status
        }

        return render(
            request,
            template_name='polls/quiz.html',
            context=context
        )

    else:
        json_data = parse_question(URL, is_multiple=False)

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
            'is_post': True,
            'is_answered': is_answered,
            'status': status.status
        }

        return render(
            request,
            template_name='polls/quiz_multiple.html',
            context=context
        )

    json_data = parse_question(URL, is_multiple=True)

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


@login_required
def upgrade_status(request):

    status_data = {
        'Beginner': 20,
        'Amateur': 50,
        'PRO': 70,
    }

    if not Status.objects.filter(user=request.user).exists():
        Status.objects.create(user=request.user)
    status = Status.objects.get(user=request.user)
    score = Score.objects.get(user=request.user)

    if request.method == 'POST':
        update_score_status(status, score, status_data)

    for value in status_data.values():
        if status.status == 'Beginner' and score.points >= value:
            context = {
                'text': f'you can upgrade to AMATEUR ({value} points)',
                'status': status.status,
                'score': score,
                'upgrade': True
            }
            return render(
                request,
                template_name='polls/upgrade.html',
                context=context
            )

        if status.status == 'Amateur' and score.points >= value:
            context = {
                'text': f'you can upgrade to PRO ({value} points)',
                'status': status.status,
                'score': score,
                'upgrade': True
            }
            return render(
                request,
                template_name='polls/upgrade.html',
                context=context
            )

        if status.status == 'PRO' and score.points >= value:
            context = {
                'text': f'you can upgrade to the BEST ({value} points)',
                'status': status.status,
                'score': score,
                'upgrade': True
            }
            return render(
                request,
                template_name='polls/upgrade.html',
                context=context
            )

        if status.status == 'BEST':
            context = {
                'BEST': True,
                'score': score,
                'status': status.status,
            }
            return render(
                request,
                template_name='polls/upgrade.html',
                context=context
            )

        context = {
            'text': '''Not available<br>Amateur - 50 points<br>
                PRO - 70 points<br>BEST - 100 points''',
            'score': score,
            'status': status.status,
                    }

        return render(
                request,
                template_name='polls/upgrade.html',
                context=context
            )


@login_required
def clean_status_score(request):
    status = Status.objects.get(user=request.user)
    score = Score.objects.get(user=request.user)
    not_clean = None

    if score.points > 0:
        not_clean = True
    not_clean = False

    if request.method == 'POST':
        status.status = 'Beginner'
        score.points = 0
        not_clean = False

        context = {
            'score': score,
            'status': status.status,
            'not_clean': not_clean
        }

        return render(
                    request,
                    template_name='polls/clean.html',
                    context=context
                )

    context = {
            'score': score,
            'status': status.status,
            'not_clean': not_clean
        }

    return render(
                request,
                template_name='polls/clean.html',
                context=context
            )
