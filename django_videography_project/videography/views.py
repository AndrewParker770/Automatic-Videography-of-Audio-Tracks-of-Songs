from django.shortcuts import render
from django.http import HttpResponse

from Source.audioStripper import stripAudio
from .forms import LinkForm

def index(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            result = stripAudio(form.cleaned_data['link'])
            context_dict = {'currentpage': 'index', 'method': 'POST', 'status': 'done', 'result': result}
            return HttpResponse(result)
    else:
        form = LinkForm()
        context_dict = {'currentpage': 'index', 'method': 'GET', 'form': form}
        return render(request, 'videography/index.html', context=context_dict)


def about(request):
    context_dict = {'currentpage': 'about'}
    return render(request, 'videography/about.html', context=context_dict)

def video(request):
    context_dict = {'currentpage': 'video'}
    return render(request, 'videography/video.html', context=context_dict)