from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context_dict = {'boldmessage': 'Cookies and Cream!'}
    return render(request, 'videography/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': 'One small step for man!'}
    return render(request, 'videography/about.html', context=context_dict)

def video(request):
    context_dict = {'boldmessage': 'Welcome to the video page!'}
    return render(request, 'videography/video.html', context=context_dict)