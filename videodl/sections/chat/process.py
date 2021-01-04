from __future__ import unicode_literals
from django.shortcuts import redirect
from django.http import HttpResponse
import youtube_dl
import subprocess
from subprocess import check_output, run
import threading

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


def download_sub_process(url):
    cmd = 'youtube-dl ' + url + ' --out videodl.mp4'
    try:
        #out = subprocess.check_output("dir",shell=True,stderr=subprocess.STDOUT)
        #out = subprocess.check_output("youtube-dl https://www.youtube.com/watch?v=suIAo0EYwOE --out videodl.mp4",shell=True,stderr=subprocess.STDOUT)
        process = subprocess.Popen(cmd, shell=False, stderr=subprocess.STDOUT)
    except:
        raise RuntimeError("command '{}' return with error (code {}): {}")
    return "sto faticando"

def download_sub_process_a(url):
    out = ''
    cmd = 'youtube-dl ' + url + ' --out videodl.mp4'
    print(cmd)
    #cmd = 'python test.py'
    #cmd = 'dir'
    
    process = subprocess.Popen(cmd, shell=False, stderr=subprocess.STDOUT,stdin  = subprocess.PIPE,
                    stdout = subprocess.PIPE,
                    universal_newlines=True)
    #outs, errs = process.communicate(timeout=15)
    while process.poll() is None:
        data = process.stdout.readline()
        
    return "sto lavorando"

def checkout ():
    cmd = 'dir'
    cmd = 'python test.py'
    try:
        out = subprocess.check_output(cmd,shell=False,stderr=subprocess.STDOUT, timeout=20)
        print(out)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    return "sto lavorando"

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
        return redirect('youtube/')
    thread = threading.Thread(target=run_in_thread, args=(call_on_exit, popen_args))
    thread.start()
    # returns immediately after the thread starts
    return thread

def call_on_exit ():
    print("basta")
    return HttpResponse("vai ")
    return redirect('dfinishyoutube')


