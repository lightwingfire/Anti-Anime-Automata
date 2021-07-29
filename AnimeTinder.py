import tkinter
import shutil
import os
from PIL import ImageTk, Image

top = tkinter.Tk()
canvas = tkinter.Canvas(top, width = 0, height = 0)
canvas.pack()

filepath = "C:\\Users\\Receptionist\\IdeaProjects\\Anti-Anime-Automata\\pfp\\"
pic = os.listdir(filepath)[0]
img = ImageTk.PhotoImage(Image.open(filepath + pic))
panel = tkinter.Label(top, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")

def anime (event):
    animeFilePath = "C:\\Users\\Receptionist\\IdeaProjects\\Anti-Anime-Automata\\pfp-anime"
    print("anime")

    shutil.move(filepath+os.listdir(filepath)[0],animeFilePath)
    try:
        pic = os.listdir(filepath)[0]
        img = ImageTk.PhotoImage(Image.open(filepath + pic))
    except:
        delete()

    panel.configure(image=img)
    panel.image = img
    panel.pack(side = "bottom", fill = "both", expand = "yes")

def notanime (event):
    notAnimeFilePath = "C:\\Users\\Receptionist\\IdeaProjects\\Anti-Anime-Automata\\pfp-not-anime"
    print("notanime")

    shutil.move(filepath+os.listdir(filepath)[0],notAnimeFilePath)
    try:
        pic = os.listdir(filepath)[0]
        img = ImageTk.PhotoImage(Image.open(filepath + pic))
    except:
        delete()

    panel.configure(image=img)
    panel.image = img
    panel.pack(side = "bottom", fill = "both", expand = "yes")

def cartoon (event):
    cartoonFilePath = "C:\\Users\\Receptionist\\IdeaProjects\\Anti-Anime-Automata\\pfp-cartoon"
    print("cartoon")

    shutil.move(filepath+os.listdir(filepath)[0],cartoonFilePath)
    try:
        pic = os.listdir(filepath)[0]
        img = ImageTk.PhotoImage(Image.open(filepath + pic))
    except:
        delete()

    panel.configure(image=img)
    panel.image = img
    panel.pack(side = "bottom", fill = "both", expand = "yes")

def delete (event):
    delete()

def delete ():
    print("delete")
    os.remove(filepath+os.listdir(filepath)[0])

    try:
        pic = os.listdir(filepath)[0]
        img = ImageTk.PhotoImage(Image.open(filepath + pic))
    except:
        delete()

    panel.configure(image=img)
    panel.image = img
    panel.pack(side = "bottom", fill = "both", expand = "yes")

frame1 = tkinter.Frame(top, height =0, width = 0)
frame1.bind('<q>', anime)
frame1.bind('<w>', notanime)
frame1.bind('<e>', cartoon)
frame1.bind('<r>', delete)
frame1.focus_set()
frame1.pack()

top.mainloop()