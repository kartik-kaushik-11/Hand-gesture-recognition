from tkinter import *
import customtkinter
from tkinter import messagebox
from handGestures import hand_function
from PIL import Image

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

global a
global b

a = 0
b = 0

customtkinter.set_widget_scaling(1)  # widget dimensions and text size
customtkinter.set_window_scaling(1)  # window geometry dimensions

def start_application(p1,p2):
    if (p1 == 0 or p2 == 0):
        p1 = 4
        p2 = 12
    response = messagebox.askyesno("Start Camera","Do you want to show the camera output?\n Note:- Click No, to save power")
    if response == True:
        hand_function(1,p1,p2)
        root.destroy()
    else:
        hand_function(0,p1,p2)
        root.destroy()

def customize():
    custom = customtkinter.CTk()
    custom.geometry("400x400")
    optionmenu_var1 = customtkinter.StringVar(value="Select")
    optionmenu_var2 = customtkinter.StringVar(value="Select")  # set initial value
    global a,b
    def optionmenu_callback1(choice):
        global a
        landmark = {"Thumb":4,"Index Finger":8,"Middle Finger":12,"Ring Finger":16,"Pinky Finger":20}
        a = landmark[choice]
    
    def optionmenu_callback2(choice):
        global b
        landmark = {"Thumb":4,"Index Finger":8,"Middle Finger":12,"Ring Finger":16,"Pinky Finger":20}
        b = landmark[choice]
    
    def save():
        custom.destroy()
        return a,b

    point1 = customtkinter.CTkLabel(custom, text = "Finger 1")
    point1.place(x = 50, y = 10)
    combobox = customtkinter.CTkOptionMenu(master=custom,
                                       values=["Thumb", "Index Finger","Middle Finger","Ring Finger","Pinky Finger"],
                                       command=optionmenu_callback1,
                                       variable=optionmenu_var1)
    combobox.place(x = 10, y = 40)

    point2 = customtkinter.CTkLabel(custom, text = "Finger 2")
    point2.place(x = 250, y = 10)
    combobox2 = customtkinter.CTkOptionMenu(master=custom,
                                       values=["Thumb", "Index Finger","Middle Finger","Ring Finger","Pinky Finger"],
                                       command=optionmenu_callback2,
                                       variable=optionmenu_var2)
    combobox2.place(x = 200, y = 40)
    save_button = customtkinter.CTkButton(custom, text = "Save")
    save_button.configure(font = ("Verdana",15))
    save_button.configure(width=100, command = save)
    save_button.place(x = 130, y = 200)
    custom.mainloop()

root = customtkinter.CTk()
root.resizable(False,False)
# root = Tk()
root.geometry("400x500")
root.config(bg = "#15202b")
start_label = customtkinter.CTkLabel(root, text = "HAND TRACKING APPLICATION",fg_color = "#15202b")
start_label.place(x = 60, y = 50)
start_label.configure(font = ("Verdana",20))


start_button = customtkinter.CTkButton(root, text = "Start Application")
start_button.configure(font = ("Verdana",15))
start_button.configure(width=100, command = lambda:start_application(a,b))
start_button.place(x = 130, y = 200)

cust_button = customtkinter.CTkButton(root, text = "Customize")
cust_button.configure(font = ("Verdana",15), width = 100, command = customize)
cust_button.place(x = 150, y = 150)
root.mainloop()