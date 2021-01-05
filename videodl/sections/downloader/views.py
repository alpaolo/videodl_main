from django.shortcuts import render, redirect
from django.http import HttpResponse
from . process import download_process, popen_and_call, call_on_exit, sendmessage
import threading
import json


# This views satisfy any kind of url with appropriate view and template but is confused
args ={'section':'download'}

def index(request):
    return HttpResponse("Hello, world. Is download section")

def download_finish(request):
   return render(request, 'd_finish.html', args)

def downloadyoutube(request, action=''): # va tutto spostato in models
    args = {}
    args ={'section':'Video Downloader:', 'subsection': 'YOUTUBE', 'message' : '', 'videosrc':'', 'download_videosrc' : ''}
    args['yturl'] = ''
    if action =='download' and request.method == 'POST':
        args['yturl'] = request.POST.get('youtube_url', False)
        if args['yturl'] == False or args['yturl'] == '':
            args['message'] = "Nessun link da scaricare"
            return render(request, 'd_youtube.html', args)
        else: 
            args['message'] = "sto scaricando il file: " + args['yturl']
            #popen_and_call(args['yturl'])
            download_process(args['yturl'])
            #await sendmessage()
            
    return render(request, 'd_youtube.html', args)

def downloadrai(request):
    return render(request, 'd_rai.html', args)

def finishdownloadyoutube(request):
    args = {}
    args ={'section':'Video Downloader:', 'subsection': 'YOUTUBE', 'message' : 'aggio fornuto', 'videosrc':'', 'download_videosrc' : ''}
    return render(request, 'd_youtube.html', args)



    