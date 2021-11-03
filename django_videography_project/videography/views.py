from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context_dict = {'currentpage': 'index'}
    return render(request, 'videography/index.html', context=context_dict)


def about(request):
    context_dict = {'currentpage': 'about'}
    return render(request, 'videography/about.html', context=context_dict)

def video(request):
    context_dict = {'currentpage': 'video'}
    return render(request, 'videography/video.html', context=context_dict)