import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance

# Define color scheme for consistency
COLORS = {
    "primary": "#3498db",      # Blue
    "secondary": "#2ecc71",    # Green
    "accent": "#f39c12",       # Orange
    "background": "#f5f5f5",   # Light gray
    "dark_bg": "#2c3e50",      # Dark blue/gray
    "text": "#2c3e50",         # Dark blue/gray
    "light_text": "#ecf0f1",   # Almost white
    "success": "#27ae60",      # Darker green
    "warning": "#e74c3c"       # Red
}

def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"
trainimage_path = "TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = "./StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

window = Tk()
window.title("Class Vision - Face Recognition Attendance System")
window.geometry("1280x720")
dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"
window.configure(background=COLORS["background"])

# Custom styles for buttons
def create_button(parent, text, command, width=15, height=2, bg=COLORS["primary"]):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bd=0,
        font=("Verdana", 12),
        bg=bg,
        fg=COLORS["light_text"],
        height=height,
        width=width,
        cursor="hand2",
        activebackground=bg,
        activeforeground=COLORS["light_text"],
    )

# Custom styles for entries
def create_entry(parent, width=15, bg=COLORS["light_text"]):
    return tk.Entry(
        parent,
        width=width,
        bd=0,
        bg=bg,
        fg=COLORS["text"],
        font=("Verdana", 12),
        relief=FLAT,
    )

# Custom styles for labels
def create_label(parent, text, width=15, height=1, bg=COLORS["background"]):
    return tk.Label(
        parent,
        text=text,
        width=width,
        height=height,
        bg=bg,
        fg=COLORS["text"],
        font=("Verdana", 12),
    )

# to destroy screen
def del_sc1():
    sc1.destroy()

# error message for name and no
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x120")
    sc1.title("Warning!")
    sc1.configure(background=COLORS["background"])
    sc1.resizable(0, 0)
    
    # Create a frame for the error message
    error_frame = Frame(sc1, bg=COLORS["warning"], bd=1, relief=RIDGE)
    error_frame.pack(padx=20, pady=20, fill=X)
    
    tk.Label(
        error_frame,
        text="Enrollment & Name required!",
        fg=COLORS["light_text"],
        bg=COLORS["warning"],
        font=("Verdana", 14),
        pady=10
    ).pack()
    
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg=COLORS["light_text"],
        bg=COLORS["primary"],
        width=8,
        height=1,
        bd=0,
        cursor="hand2",
        font=("Verdana", 12),
    ).pack(pady=10)

def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True

# Create header frame
header_frame = Frame(window, bg=COLORS["dark_bg"], height=100)
header_frame.pack(fill=X)

# Load logo
try:
    logo = Image.open("UI_Image/0001.png")
    logo = logo.resize((50, 47), Image.LANCZOS)
    logo1 = ImageTk.PhotoImage(logo)
    l1 = tk.Label(header_frame, image=logo1, bg=COLORS["dark_bg"])
    l1.pack(side=LEFT, padx=20)
except:
    pass  # Handle missing logo gracefully

# App title
app_title = tk.Label(
    header_frame, 
    text="CLASS VISION",
    bg=COLORS["dark_bg"],
    fg=COLORS["light_text"],
    font=("Verdana", 24, "bold"),
    pady=20
)
app_title.pack(side=LEFT, padx=10)

# Welcome message
welcome_frame = Frame(window, bg=COLORS["background"], pady=20)
welcome_frame.pack(fill=X)

welcome_text = tk.Label(
    welcome_frame,
    text="Facial Recognition Attendance System",
    bg=COLORS["background"],
    fg=COLORS["text"],
    font=("Verdana", 18),
)
welcome_text.pack()

# Create main content frame
content_frame = Frame(window, bg=COLORS["background"], pady=20)
content_frame.pack(fill=BOTH, expand=True)

# Create card layout for the main options
def create_card(parent, title, image_path, description):
    card = Frame(parent, bg=COLORS["light_text"], bd=0, relief=RAISED, padx=15, pady=15)
    
    try:
        img = Image.open(image_path)
        img = img.resize((80, 80), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        img_label = Label(card, image=photo, bg=COLORS["light_text"])
        img_label.image = photo
        img_label.pack(pady=10)
    except:
        # Create a colored box as fallback
        canvas = Canvas(card, width=80, height=80, bg=COLORS["primary"], highlightthickness=0)
        canvas.pack(pady=10)
    
    title_label = Label(
        card, 
        text=title, 
        font=("Verdana", 16, "bold"),
        bg=COLORS["light_text"],
        fg=COLORS["text"]
    )
    title_label.pack(pady=5)
    
    desc_label = Label(
        card, 
        text=description, 
        font=("Verdana", 10),
        bg=COLORS["light_text"],
        fg=COLORS["text"],
        wraplength=200
    )
    desc_label.pack(pady=5)
    
    return card

# Create three columns for cards
card_frame1 = Frame(content_frame, bg=COLORS["background"])
card_frame1.pack(side=LEFT, expand=True, padx=20, pady=20)

card_frame2 = Frame(content_frame, bg=COLORS["background"])
card_frame2.pack(side=LEFT, expand=True, padx=20, pady=20)

card_frame3 = Frame(content_frame, bg=COLORS["background"])
card_frame3.pack(side=LEFT, expand=True, padx=20, pady=20)

# Create cards with descriptions
register_card = create_card(
    card_frame1, 
    "Register Student", 
    "UI_Image/register.png", 
    "Register a new student by capturing facial images and adding details to the system."
)
register_card.pack(fill=BOTH, expand=True)

attendance_card = create_card(
    card_frame2, 
    "Take Attendance", 
    "UI_Image/verifyy.png", 
    "Use facial recognition to automatically track student attendance for a subject."
)
attendance_card.pack(fill=BOTH, expand=True)

view_card = create_card(
    card_frame3, 
    "View Records", 
    "UI_Image/attendance.png", 
    "View and analyze attendance records by student or by class."
)
view_card.pack(fill=BOTH, expand=True)

# Button Frame
button_frame = Frame(window, bg=COLORS["background"], pady=20)
button_frame.pack(fill=X)

def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Register New Student")
    ImageUI.geometry("780x500")
    ImageUI.configure(background=COLORS["background"])
    ImageUI.resizable(0, 0)
    
    # Create header
    header = Frame(ImageUI, bg=COLORS["primary"], height=60)
    header.pack(fill=X)
    
    title = tk.Label(
        header, 
        text="Register New Student", 
        bg=COLORS["primary"], 
        fg=COLORS["light_text"], 
        font=("Verdana", 18, "bold"),
        pady=10
    )
    title.pack()
    
    # Create form frame
    form_frame = Frame(ImageUI, bg=COLORS["background"], pady=20)
    form_frame.pack(fill=BOTH, expand=True)
    
    # Form fields with better spacing and alignment
    form_left = Frame(form_frame, bg=COLORS["background"])
    form_left.pack(side=LEFT, padx=20, fill=BOTH, expand=True)
    
    # Enrollment field
    enroll_label = Label(
        form_left, 
        text="Enrollment No:", 
        bg=COLORS["background"], 
        fg=COLORS["text"],
        font=("Verdana", 12),
        anchor="e"
    )
    enroll_label.pack(fill=X, pady=5)
    
    enroll_entry_frame = Frame(form_left, bg=COLORS["background"], pady=5)
    enroll_entry_frame.pack(fill=X)
    
    txt1 = Entry(
        enroll_entry_frame,
        width=20,
        validate="key",
        bg=COLORS["light_text"],
        fg=COLORS["text"],
        relief=FLAT,
        highlightthickness=1,
        highlightbackground="#cccccc",
        font=("Verdana", 12)
    )
    txt1.pack(fill=X, ipady=5)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")
    
    # Name field
    name_label = Label(
        form_left, 
        text="Name:", 
        bg=COLORS["background"], 
        fg=COLORS["text"],
        font=("Verdana", 12),
        anchor="e"
    )
    name_label.pack(fill=X, pady=(15, 5))
    
    name_entry_frame = Frame(form_left, bg=COLORS["background"], pady=5)
    name_entry_frame.pack(fill=X)
    
    txt2 = Entry(
        name_entry_frame,
        width=20,
        bg=COLORS["light_text"],
        fg=COLORS["text"],
        relief=FLAT,
        highlightthickness=1,
        highlightbackground="#cccccc",
        font=("Verdana", 12)
    )
    txt2.pack(fill=X, ipady=5)
    
    # Notification area
    notif_label = Label(
        form_left, 
        text="Status:", 
        bg=COLORS["background"], 
        fg=COLORS["text"],
        font=("Verdana", 12),
        anchor="e"
    )
    notif_label.pack(fill=X, pady=(15, 5))

    message = Label(
        form_left,
        text="",
        width=30,
        height=2,
        bg=COLORS["light_text"],
        fg=COLORS["text"],
        font=("Verdana", 10),
        anchor="w",
        padx=10,
        pady=10
    )
    message.pack(fill=X, pady=5)
    
    # Buttons frame
    button_frame = Frame(form_left, bg=COLORS["background"], pady=20)
    button_frame.pack(fill=X)
    
    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")
    
    takeImg = Button(
        button_frame,
        text="Capture Images",
        command=take_image,
        bd=0,
        font=("Verdana", 12),
        bg=COLORS["primary"],
        fg=COLORS["light_text"],
        cursor="hand2",
        padx=10,
        pady=5
    )
    takeImg.pack(side=LEFT, padx=10)
    
    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )
    
    trainImg = Button(
        button_frame,
        text="Train Model",
        command=train_image,
        bd=0,
        font=("Verdana", 12),
        bg=COLORS["secondary"],
        fg=COLORS["light_text"],
        cursor="hand2",
        padx=10,
        pady=5
    )
    trainImg.pack(side=LEFT, padx=10)

def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)

def view_attendance():
    show_attendance.subjectchoose(text_to_speech)

# Create main function buttons
register_button = Button(
    button_frame,
    text="Register New Student",
    command=TakeImageUI,
    bd=0,
    font=("Verdana", 12),
    bg=COLORS["primary"],
    fg=COLORS["light_text"],
    padx=15,
    pady=8,
    cursor="hand2"
)
register_button.pack(side=LEFT, padx=20)

take_button = Button(
    button_frame,
    text="Take Attendance",
    command=automatic_attedance,
    bd=0,
    font=("Verdana", 12),
    bg=COLORS["secondary"],
    fg=COLORS["light_text"],
    padx=15,
    pady=8,
    cursor="hand2"
)
take_button.pack(side=LEFT, padx=20)

view_button = Button(
    button_frame,
    text="View Attendance",
    command=view_attendance,
    bd=0,
    font=("Verdana", 12),
    bg=COLORS["accent"],
    fg=COLORS["light_text"],
    padx=15,
    pady=8,
    cursor="hand2"
)
view_button.pack(side=LEFT, padx=20)

# Footer frame
footer_frame = Frame(window, bg=COLORS["dark_bg"], height=50)
footer_frame.pack(side=BOTTOM, fill=X)

exit_btn = Button(
    footer_frame,
    text="EXIT",
    command=quit,
    bd=0,
    font=("Verdana", 10),
    bg=COLORS["warning"],
    fg=COLORS["light_text"],
    padx=10,
    pady=5,
    cursor="hand2"
)
exit_btn.pack(side=RIGHT, padx=20, pady=10)

copyright_label = Label(
    footer_frame,
    text="© 2025 Class Vision | Face Recognition Attendance System",
    bg=COLORS["dark_bg"],
    fg=COLORS["light_text"],
    font=("Verdana", 8)
)
copyright_label.pack(side=LEFT, padx=20, pady=15)

window.mainloop()