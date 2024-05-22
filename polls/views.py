from django.shortcuts import render

from polls.models import Score, Status

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
