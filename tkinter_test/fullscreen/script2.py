from tkinter import *
root = Tk()

root.tk.call("::tk::unsupported::MacWindowStyle", "style", root._w, "plain", "none")

def quitApp():
    root.destroy()

button = Button(text = 'QUIT', command = quitApp).pack()

root.mainloop()
