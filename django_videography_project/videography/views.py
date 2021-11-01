from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context_dict = {'boldmessage': 'One small step for man!'}
    return render(request, 'videography/index.html', context=context_dict)


def about(request):
    return HttpResponse("Rango says here is the about page.<a href='/videography/'>Index</a>")