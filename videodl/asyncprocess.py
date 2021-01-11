from __future__ import unicode_literals
import os
import shutil
import json
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
import youtube_dl
import subprocess
from subprocess import check_output, run
import threading
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
import time
import asyncio
import random

class MyLogger(object):
    def debug(self, msg):
        return(msg)

    def warning(self, msg):
        return(msg)

    def error(self, msg):
        return(msg)

class AsyncProcess(object):
    consumer = None

    def __init__(self, c):
        self.consumer = c
    
    def debug(self, msg):
        return(msg)

    def warning(self, msg):
        return(msg)

    def error(self, msg):
        return(msg)


    def get_info(self, url):
        result = None
        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'}) 
        with ydl:
            result = ydl.extract_info(url, download=False # We just want to extract the info
        )

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result

        print(video)
        video_url = video['url']
        print(video_url)   


    #======================================================================================================================== 
   
    def download_process(self, url):
        result = None
        ydl_opts = {
            'writethumbnail': True,
            'download': False,
            'forceurl': True,
            'forcejson': True,
            'outtmpl': 'videodl.mp4',
            'format': 'best',
            'logger': MyLogger(),
            'progress_hooks': [self.my_hook],
            'consumer' : self.consumer,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([url])
        print (result)
            
            
    # CALLBACK di DOWNLOAD PROCESS
    def my_hook(self,d):
        channel_layer = get_channel_layer()
        room_group_name = 'chat_%s' % 'room'
        #----------------------------------------------------------------
        if d['status'] == 'finished':
            print (d)
            print("my hook finish")
            file_tuple = os.path.split(os.path.abspath(d['filename']))
            print("Done downloading {}".format(file_tuple[1]))
            hash = random.getrandbits(128)
            dst = str(settings.STATIC_ROOT+"/media/"+str(hash)+".mp4")
            shutil.copy("videodl.mp4", dst)
            os.remove(os.path.abspath(d['filename']))
            print (os.path.abspath(d['filename']), 'removed') 
            dst = str(settings.STATIC_ROOT+"/images/videodl.jpg")
            shutil.copy("videodl.jpg", dst)
            # ***** creare un messaggio per comunicare il nome del file al client
            self.sendmessage('end_download','download_ok#'+str(hash)+".mp4") 
        if d['status'] == 'downloading':
            p = d['_percent_str']
            p = p.replace('%','')
            print(d['filename'], d['_percent_str'], d['_eta_str'])
            #self.sendmessage('progress_download',d['filename']+" "+d['_percent_str']+" "+d['_eta_str'])
           
    #========================================================================================================================      

    def popen_process(self, url):
        cmd = 'youtube-dl ' + url + ' --get-url'
        popen_args = [cmd]
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)

    #========================================================================================================================      

    def popen_in_thread(self, url):
        """
        Runs the given args in a subprocess.Popen, and then calls the function
        on_exit when the subprocess completes.
        on_exit is a callable object, and popen_args is a list/tuple of args that 
        would give to subprocess.Popen.
        """
        cmd = 'youtube-dl ' + url + ' --get-url'
        popen_args = [cmd]

        thread = threading.Thread(target=self.run_in_thread, args=(self.call_on_exit, popen_args))
        thread.start()
        # returns immediately after the thread starts
        return thread

    # CALLBACK di POPEN_AND_CALL
    def run_in_thread(on_exit, popen_args):
        proc = subprocess.Popen(*popen_args)
        proc.wait()
        on_exit()
        print("prima o dopo")
        
    #========================================================================================================================     

    def call_on_exit (self):
        #time.sleep(2)
        print("basta")
        type = "renderDeployments"
        message = "file downloaded"
        '''
        file_tuple = os.path.split(os.path.abspath(d['filename']))
        print("Done downloading {}".format(file_tuple[1]))
        dst = str(settings.STATIC_ROOT+"/media/videodl.mp4")
        shutil.copy("videodl.mp4", dst)
        os.remove(os.path.abspath(d['filename']))
        print (os.path.abspath(d['filename']), 'removed') 
        dst = str(settings.STATIC_ROOT+"/images/videodl.jpg")
        shutil.copy("videodl.jpg", dst)
        '''
        self.sendmessage('end_download','download_ok') 
        return

    #======================================================================================================================== 

    def sendmessage (self, type, message):
        room_name = self.consumer.scope['url_route']['kwargs']['comm_name']
        room_group_name = 'chat_%s' % room_name
        async_to_sync(self.consumer.channel_layer.group_send)(
            self.consumer.room_group_name,
            {
                'type': type,
                'message': message
            }
        )

        
