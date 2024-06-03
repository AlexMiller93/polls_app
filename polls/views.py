from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from core.settings import URL
from polls.models import Profile
# from polls.utils import (
#     get_question_answers,
#     parse_question,
#     update_score_status
#     )

# Create your views here.


def index(request):
    """ Функция для отображения статуса и счета пользователя """

    if not request.user.is_authenticated:
        return render(request, template_name='polls/index.html')
    
    profile = Profile.objects.get_or_create(user=request.user)

    context = {
            'score': profile.points,
            'status': profile.status
        }

    return render(
        request,
        template_name='polls/index.html',
        context=context
    )

'''
def _get_top_info_users(status: Status) -> None:
    """ Функция для получения пользователей по статусу"""
    
    status_user = Status.objects.filter(status=status).values('user')
    top_scores = Score.objects.order_by('-points').filter(user__in=status_user)[:3]
    return top_scores


def top_users(request):
    """
    Функция для отображения 3 наиболее успешных пользователей
        во всех статусах кроме Beginner
    """
    # get scores and status from top-3 users
    bests = _get_top_info_users('BEST')
    best_prof = _get_top_info_users('PRO')
    best_amateurs = _get_top_info_users('Amateur')

    context = {
        'bests': bests,
        'prof': best_prof,
        'amateurs': best_amateurs
    }
    
    if not request.user.is_authenticated:
        
        return render(
        request,
        template_name='polls/top_users.html',
        context=context
    )
    else:
        # получаем статус и счет текущего пользователя
        status = Status.objects.get(user=request.user)
        score = Score.objects.get(user=request.user)

        context.update(score=score, status=status.status)

        return render(
            request,
            template_name='polls/top_users.html',
            context=context
        )


@login_required
def quiz(request):
    """ Функция для отображения вопроса типа Правда или ложь """

    # получаем счет текущего пользователя,
    # создаем если его нет

    score = Score.objects.get_or_create(user=request.user)

    # обработка ответа пользователя
    if request.method == 'POST':
        if not Question.objects.filter(user=request.user).exists():
            return redirect(reverse_lazy('polls:quiz'))

        question = get_object_or_404(Question, user=request.user)
        user_answer = request.POST.get('user_answer')

        if question.correct_answer == user_answer:
            score.points += 1
            score.counter_bool += 1

            score.save()

        correct_answer = question.correct_answer
        text = question.text
        question.delete()

        context = {
            'correct_answer': correct_answer,
            'results': [{'question': text}],
            'score': score,
            'is_answered': True
        }

        return render(
            request,
            template_name='polls/quiz.html',
            context=context
        )

    # парсинг вопроса + вывод параметров вопроса
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
        'score': score
    }

    return render(
        request,
        template_name='polls/quiz.html',
        context=context
    )


@login_required
def quiz_multiple(request):
    """ Функция для отображения вопроса с множеством ответов """

    # получаем счет текущего пользователя,
    # создаем если его нет
    score = Score.objects.get_or_create(user=request.user)

    current_score = score.points
    counter = score.counter_multiple

    # обработка ответа пользователя
    if request.method == 'POST':
        if not Question.objects.filter(user=request.user).exists():
            return redirect(reverse_lazy('polls:quiz_multiple'))

        question = Question.objects.get(user=request.user)
        user_answer = request.POST.get('user_answer')
        is_right_answered = False

        if question.correct_answer == user_answer:
            current_score += 5
            counter += 1
            score.points = current_score
            score.counter_multiple = counter

            score.save()

            is_right_answered = True

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
            'is_right_answered': is_right_answered
        }

        return render(
            request,
            template_name='polls/quiz_multiple.html',
            context=context
        )

    # парсинг вопроса + вывод параметров вопроса
    json_data = parse_question(URL, is_multiple=True)

    if not Question.objects.filter(user=request.user).exists():
        Question.objects.create(user=request.user)

    question = Question.objects.get(user=request.user)

    answers = get_question_answers(question, json_data)

    context = {
        'results': json_data['results'],
        'score': score,
        'answers': answers
    }

    return render(
        request,
        template_name='polls/quiz_multiple.html',
        context=context
        )


@login_required
def upgrade_status(request):
    """ Функция для изменения счета пользователя после смены статуса """

    # данные в виде словаря по статусу и значением баллов,
    # с которым можно сделать апгрейд
    status_data = {
        'Beginner': 20,
        'Amateur': 50,
        'PRO': 100,
    }

    status = Status.objects.get_or_create(user=request.user)
    score = Score.objects.get(user=request.user)

    # изменение счета и статуса после нажатия кнопки
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
            'text': """
                Not available<br>
                Amateur - 50 points<br>
                PRO - 100 points<br>
                BEST - 500 points
                """,
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
    """
    Функция для очистки счета пользователя
    с изменением статуса на Beginner
    """

    status = Status.objects.get(user=request.user)
    score = Score.objects.get(user=request.user)
    not_clean = None

    if score.points > 0:
        not_clean = True
    not_clean = False

    # логика изменения счета и статуса
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

'''