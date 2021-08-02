import tkinter
import shutil
import os
from PIL import ImageTk, Image

#creates window
top = tkinter.Tk()
canvas = tkinter.Canvas(top, width = 0, height = 0)
canvas.pack()

#filepath is where it pulls from (must end in\\) while the other three locations are where it places them
filepath = os.getcwd()+"\\pfp\\pfp\\"
animeFilePath = os.getcwd()+"\\pfp\\pfp-anime"
notAnimeFilePath = os.getcwd()+"\\pfp\\pfp-not-anime"
cartoonFilePath =os.getcwd()+"\\pfp\\cartoon"

#pulls the first image from filepath and places it into a panel on the window
pic = os.listdir(filepath)[0]
img = ImageTk.PhotoImage(Image.open(filepath + pic))
panel = tkinter.Label(top, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")

def anime (event):
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