from __future__ import unicode_literals
import json
from django.shortcuts import redirect
from django.http import HttpResponse
import youtube_dl
import subprocess
from subprocess import check_output, run
import threading
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ... consumers  import ChatConsumer
import time

class MyLogger(object):
    def debug(self, msg):
        return(msg)

    def warning(self, msg):
        return(msg)

    def error(self, msg):
        return(msg)


def my_hook(d):
    if d['status'] == 'finished':
        return 'Done downloading, now converting ...'

def download_process(url):
    ydl_opts = {
        'outtmpl': 'videodl.mp4',
        'format': 'best',
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        return "sto a fatiga!"
        #return ydl_opts['progress_hooks']


def popen_and_call(url):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    on_exit when the subprocess completes.
    on_exit is a callable object, and popen_args is a list/tuple of args that 
    would give to subprocess.Popen.
    """
    cmd = cmd = 'youtube-dl ' + url + ' --out videodl.mp4'
    popen_args = [cmd]
    def run_in_thread(on_exit, popen_args):
        proc = subprocess.Popen(*popen_args)
        proc.wait()
        on_exit()
        print("prima o dopo")
    thread = threading.Thread(target=run_in_thread, args=(call_on_exit, popen_args))
    thread.start()
    # returns immediately after the thread starts
    return thread

def call_on_exit ():
    #time.sleep(2)
    print("basta")
    type = "renderDeployments"
    message = "file downloaded"
    channel_layer = get_channel_layer()
    room_group_name = 'chat_%s' % 'room'
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'chat_message',
            'message': "download_ok"
        }
    )
    return



