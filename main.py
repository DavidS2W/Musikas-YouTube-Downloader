from __future__ import unicode_literals
import tkinter as app
from ctypes import windll
from tkinter import ttk
import tkinter.font as fnt
from tkinter import *
from tkinter.filedialog import askopenfile
import os
from tkinter import filedialog
from youtube_search import YoutubeSearch
import webbrowser
from threading import Thread
import datetime
import youtube_dl


page = app.Tk(screenName='Musikas', className='Musikas-1')
page.geometry('740x500')

frame = ttk.Frame(page)
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=3)
frame.columnconfigure(2, weight=1)



la = ttk.Label(frame, text="Search query or Youtube URL: ", font=("Calibri", 12))
la.grid(column=0, row=0, sticky=app.W)

input1 = app.StringVar()
lt = ttk.Entry(frame, width=50, textvariable=input1)




lt.focus()
lt.grid(column=1, row=0)

listre = ["MP3", "MP4", "WAV", "WEBM", "M4A"]

chosen_format = app.StringVar(frame)
input2 = app.StringVar()



def openurl():
    input = input1.get()
    if len(input) != 0:
        results = YoutubeSearch(input, max_results=2).to_dict()
        datapod = results[0]
        url = datapod["url_suffix"]
        webbrowser.open_new(f'https://www.youtube.com/{url}')
    else:
        pagetwo = app.Tk(screenName='Musikas', className='Musikas-2')
        pagetwo.geometry('300x100')
        frametwo = ttk.Frame(pagetwo)
        frametwo.columnconfigure(0, weight=1)
        dfa = ttk.Label(pagetwo, text="    You have not specified any songs.", font=("Calibri", 12))
        dfa.grid(column = 0, row=0)

cfbf = ttk.Button(frame, text="Search", command=lambda: fillsong(input1.get()))
cfbf.grid(column=2, row=0)
cfa = ttk.Label(frame, text='Media extraction options: ', font=("Calibri", 12))
cfa.grid(column=0, row=1, sticky=app.W)
cfm = ttk.OptionMenu(frame, chosen_format, listre[0], *listre)
cfm.grid(column=1, row=1)
cfb = ttk.Label(frame, text='Video details: ', font=("Calibri", 12))
cfb.grid(column=0, row=2, sticky=app.NW)
cfba = ttk.Label(frame, text="Title: -    \nCode: -     \nDuration: -\nChannel: -", font=("Calibri", 12))
cfba.grid(column=1, row=2, sticky=app.W)
cfbh = ttk.Button(frame, text="Watch Video", command=lambda: openurl(), state=app.DISABLED)
cfbh.grid(column=2, row=2, sticky=app.N)
cfbc = ttk.Label(frame, text="Download location:", font=("Calibri", 12))
cfbc.grid(column=0, row=3, sticky=app.W)
cfbg = ttk.Label(frame, text="[No location specified]", font=("Calibri", 12))
cfbg.grid(column=1, row=3, sticky=app.W)
cfbd = ttk.Button(frame, text='Browse', command = lambda: directoryone())
cfbd.grid(column=2, row=3)
cfbj = ttk.Label(frame, text="Status: ", font=("Calibri", 12))
cfbj.grid(column=0, row=4, sticky=app.NW)
cfbk = ttk.Label(frame, text="Idle", font=("Calibri", 12))
cfbk.grid(column=1, row=4, sticky=app.W)
cfv = ttk.Button(frame, text='Extract media', command=lambda: download_thread(get_url(), chosen_format.get(), input2.get()), state=app.DISABLED)
cfv.grid(column=2, row=5)

def download_thread(url, filetype, dir):
    t1 = Thread(target=ydl_download, args = (url, filetype, dir))
    t1.start()

def ydl_download(url, filetype, dir):
    cfbk.configure(text="Processing request... Please stand by")
    cfbf.configure(state=app.DISABLED)
    cfbd.configure(state=app.DISABLED)
    cfv.configure(state=app.DISABLED)
    def my_hook(info):
        percy = (info["downloaded_bytes"]/info["total_bytes"])*100
        perc = round(percy, 2)
        if info["status"] != "finished":
            filesize = round(info["total_bytes"]/1000000, 2)
            time = datetime.timedelta(seconds=info["eta"])
            speed = round(info["speed"]/125000, 2)
            cfbk.configure(text=f"Progress: {perc}% downloaded\nFilesize: {filesize}MB\nTime remaining: {time}\nDownload speed: {speed} Mbps")
        else:
            cfbk.configure(text=f"Finished downloading")

    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': str(filetype.lower()),
        'preferredquality': '192',
    }],
    'outtmpl': f'{dir}.{str(filetype.lower())}',
    'progress_hooks': [my_hook],
    'quiet': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    cfbk.configure(text="Idle")
    cfbf.configure(state=app.NORMAL)
    cfbd.configure(state=app.NORMAL)
    cfv.configure(state=app.NORMAL)
    askopenfile(mode ='r', filetypes =[(f'{filetype} files', f'*.{filetype}')])



def directoryone():
    asd = filedialog.asksaveasfilename()
    input2.set(asd)
    cfbg.configure(text=f"{asd}")

def get_url():
    s = input1.get()
    results = YoutubeSearch(s, max_results=2).to_dict()
    datapod = results[0]
    url = datapod["url_suffix"]
    return(f'https://youtube.com/{url}')

def fillsong(input):
    if len(input) != 0:
        results = YoutubeSearch(input, max_results=2).to_dict()
        if len(results) != 0:
            datapod = results[0]
            tit = datapod["title"]
            cod = datapod["id"]
            dura = datapod["duration"]
            chan = datapod["channel"]
            cfba.configure(text=f"Title: {tit}\nCode: {cod}\nDuration: {dura}\nChannel: {chan}")
            cfbh.configure(state=app.NORMAL)
            cfbf.configure(state=app.NORMAL)
            cfv.configure(state=app.NORMAL)
        else:
            pagetwoe = app.Tk(screenName='Musikas', className='Musikas-2')
            pagetwoe.geometry('450x100')
            frametwoe = ttk.Frame(pagetwoe)
            frametwoe.columnconfigure(0, weight=1)
            dfa = ttk.Label(pagetwoe, text="   I could not find a video with the specified keywords.", font=("Calibri", 12))
            dfa.grid(column = 0, row=0) 

    else:
        pagetwoe = app.Tk(screenName='Musikas', className='Musikas-2')
        pagetwoe.geometry('450x100')
        frametwoe = ttk.Frame(pagetwoe)
        frametwoe.columnconfigure(0, weight=1)
        dfa = ttk.Label(pagetwoe, text="   Please enter a search query or youtube URL.", font=("Calibri", 12))
        dfa.grid(column = 0, row=0) 

frame.pack(padx=3, pady=4)
try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
finally:
    app.mainloop()
