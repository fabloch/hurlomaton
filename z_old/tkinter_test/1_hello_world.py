from tkinter import *

FENETRE = Tk()

FENETRE['bg'] = 'white'

PHOTO = PhotoImage(file="img_sunset.gif")

CANVAS = Canvas(FENETRE,width=350, height=200)
CANVAS.create_image(0, 0, anchor=NW, image=PHOTO)
CANVAS.pack()

FENETRE.mainloop()
