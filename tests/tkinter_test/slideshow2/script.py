import glob
from tkinter import Tk, Label
from PIL import Image, ImageTk

root = Tk()

## chargement de toutes les images dans une liste
listeimage = []
for i in glob.glob('./img/*.*'):
    image = Image.open(i)
    photo = ImageTk.PhotoImage(image)
    listeimage.append(photo)

## l'affichage se fera sur un label
lbl = Label(root)

j = 0
## affichage des images
def diapo():
    global j
    ## on essaie d'afficher une image sur le label
    try: lbl.config(image = listeimage[j])
    except: exit ## on a passe en revu toutes les images
    j+=1
    root.after(2000, diapo)  ## on rappelle la fonction diapo dans 2 secondes

lbl.pack()
root.after(100, diapo)
root.mainloop()
