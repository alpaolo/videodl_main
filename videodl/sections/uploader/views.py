from django.shortcuts import render
from django.http import HttpResponse


# This views satisfy any kind of url with appropriate view and template but is confused
args ={'section':'upload'}

def index(request):
    return HttpResponse("Hello, world. Is upload section")

def uploadyoutube(request):
    return render(request, 'u_youtube.html', args)

def uploadrai(request):
    return render(request, 'u_rai.html', args)

def cippa(request):
    #return render(request, 'videodl/cippa.html', {})
    return HttpResponse("Hello, world. You're at  cippa.")