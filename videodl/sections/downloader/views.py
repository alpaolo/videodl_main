from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
import threading
import json


# This views satisfy any kind of url with appropriate view and template but is confused
args ={'section':'download'}

def index(request):
    return HttpResponse("Hello, world. Is download section")

def download_finish(request):
   return render(request, 'd_finish.html', args)

def downloadyoutube(request, action=''): # va tutto spostato in models
    #response["Set-Cookie"] = COOKIE_NAME+'='+COOKIE_VALUE+';expires='+EXPIRES+';Secure;SameSite=None;HttpOnly;Path=/;domain='+MY_DOMAIN+';'
    args = {}
    args ={'section':'Youtube', 'subsection': '', 'message' : '', 'videosrc':'', 'download_videosrc' : ''}
    args['yturl'] = ''
    if action =='download' and request.method == 'POST':
        args['yturl'] = request.POST.get('youtube_url', False)
        if args['yturl'] == False or args['yturl'] == '':
            args['message'] = "Nessun link da scaricare"
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    
    #args['thsrc'] = settings.BASE_DIR
    args['psrc'] = "/images/videodl.jpg"
    args['vsrc'] = "/media/videodl.mp4"
    return render(request, 'd_youtube.html', args)


def downloadrai(request):
    return render(request, 'd_rai.html', args)

def finishdownloadyoutube(request):
    args = {}
    args ={'section':'Video Downloader:', 'subsection': 'YOUTUBE', 'message' : 'aggio fornuto', 'videosrc':'', 'download_videosrc' : ''}
    return render(request, 'd_youtube.html', args)



    