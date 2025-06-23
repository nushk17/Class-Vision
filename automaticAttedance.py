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
import tkinter.ttk as tkk
import tkinter.font as font

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

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImageLabel\\Trainner.yml"
trainimage_path = "TrainingImage"
studentdetail_path = "StudentDetails\\studentdetails.csv"
attendance_path = "Attendance"

# for choose subject and fill attendance
def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()
        now = time.time()
        future = now + 20
        
        if sub == "":
            t = "Please enter the subject name!"
            text_to_speech(t)
            status_label.config(text=t, bg=COLORS["warning"], fg=COLORS["light_text"])
        else:
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)
                except:
                    e = "Model not found, please train model first"
                    status_label.config(text=e, bg=COLORS["warning"], fg=COLORS["light_text"])
                    text_to_speech(e)
                    return
                
                status_label.config(
                    text="Starting face recognition...", 
                    bg=COLORS["secondary"], 
                    fg=COLORS["light_text"]
                )
                
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ["Enrollment", "Name"]
                attendance = pd.DataFrame(columns=col_names)
                
                while True:
                    ___, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                        if conf < 70:
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime(
                                "%Y-%m-%d"
                            )
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
                                "%H:%M:%S"
                            )
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values
                            global tt
                            tt = str(Id) + "-" + aa
                            attendance.loc[len(attendance)] = [
                                Id,
                                aa,
                            ]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4
                            )
                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4
                            )
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(
                        ["Enrollment"], keep="first"
                    )
                    cv2.imshow("Taking Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break

                ts = time.time()
                # attendance["date"] = date
                # attendance["Attendance"] = "P"
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")
                path = os.path.join(attendance_path, Subject)
                if not os.path.exists(path):
                    os.makedirs(path)
                    
                fileName = (
                    f"{path}/"
                    + Subject
                    + "_"
                    + date
                    + "_"
                    + Hour
                    + "-"
                    + Minute
                    + "-"
                    + Second
                    + ".csv"
                )
                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                attendance.to_csv(fileName, index=False)

                m = f"Attendance recorded successfully for {Subject}"
                status_label.config(text=m, bg=COLORS["success"], fg=COLORS["light_text"])
                text_to_speech(m)

                cam.release()
                cv2.destroyAllWindows()

                # Show attendance in a table
                display_attendance(path, fileName)
                
            except Exception as e:
                f = "No face detected or error occurred"
                status_label.config(text=f, bg=COLORS["warning"], fg=COLORS["light_text"])
                text_to_speech(f)
                print(e)
                cv2.destroyAllWindows()

    def display_attendance(path, fileName):
        root = Toplevel()
        root.title("Attendance Record")
        root.geometry("800x600")
        root.configure(background=COLORS["background"])
        
        # Create header
        header_frame = Frame(root, bg=COLORS["primary"], height=60)
        header_frame.pack(fill=X)
        
        header_label = Label(
            header_frame,
            text=f"Attendance for {os.path.basename(fileName).split('_')[0]}",
            fg=COLORS["light_text"],
            bg=COLORS["primary"],
            font=("Verdana", 16, "bold"),
            pady=15
        )
        header_label.pack()
        
        # Table frame
        table_frame = Frame(root, bg=COLORS["background"])
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Create scrollable frame
        canvas = Canvas(table_frame, bg=COLORS["background"])
        scrollbar = Scrollbar(table_frame, orient="vertical", command=canvas.yview)
        scroll_frame = Frame(canvas, bg=COLORS["background"])
        
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Read and display CSV data
        try:
            with open(fileName, newline="") as file:
                reader = csv.reader(file)
                
                # Create headers
                headers = next(reader)
                for col_idx, header in enumerate(headers):
                    header_label = Label(
                        scroll_frame,
                        text=header,
                        width=15,
                        height=2,
                        relief=RIDGE,
                        bg=COLORS["dark_bg"],
                        fg=COLORS["light_text"],
                        font=("Verdana", 12, "bold")
                    )
                    header_label.grid(row=0, column=col_idx, sticky="nsew", padx=1, pady=1)
                
                # Create data rows
                for row_idx, row in enumerate(reader, 1):
                    for col_idx, cell in enumerate(row):
                        cell_label = Label(
                            scroll_frame,
                            text=cell,
                            width=15,
                            height=2,
                            relief=RIDGE,
                            bg=COLORS["light_text"],
                            fg=COLORS["text"],
                            font=("Verdana", 10)
                        )
                        cell_label.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)
        except Exception as e:
            print(f"Error displaying attendance: {e}")

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!"
            text_to_speech(t)
            status_label.config(text=t, bg=COLORS["warning"], fg=COLORS["light_text"])
        else:
            try:
                os.startfile(f"Attendance\\{sub}")
            except:
                t = f"No attendance records found for {sub}"
                status_label.config(text=t, bg=COLORS["warning"], fg=COLORS["light_text"])

    # Create the subject window
    subject = Tk()
    subject.title("Take Attendance")
    subject.geometry("600x400")
    subject.resizable(0, 0)
    subject.configure(background=COLORS["background"])

    # Create header
    header_frame = Frame(subject, bg=COLORS["primary"])
    header_frame.pack(fill=X)
    
    header_label = Label(
        header_frame,
        text="Take Attendance",
        bg=COLORS["primary"],
        fg=COLORS["light_text"],
        font=("Verdana", 18, "bold"),
        pady=15
    )
    header_label.pack()

    # Create content frame
    content_frame = Frame(subject, bg=COLORS["background"])
    content_frame.pack(fill=BOTH, expand=True, padx=30, pady=30)
    
    # Subject entry components
    subject_label = Label(
        content_frame,
        text="Enter Subject Name:",
        bg=COLORS["background"],
        fg=COLORS["text"],
        font=("Verdana", 12),
        anchor="w"
    )
    subject_label.pack(fill=X, pady=5)
    
    # Create a frame for the entry to style it better
    entry_frame = Frame(content_frame, bg=COLORS["background"], highlightbackground="#cccccc", highlightthickness=1)
    entry_frame.pack(fill=X, pady=10)
    
    tx = Entry(
        entry_frame,
        width=30,
        bd=0,
        bg=COLORS["light_text"],
        fg=COLORS["text"],
        font=("Verdana", 14),
        relief=FLAT
    )
    tx.pack(fill=X, ipady=8, padx=2, pady=2)
    
    # Status label
    status_label = Label(
        content_frame,
        text="Enter subject name and click on 'Take Attendance'",
        bg=COLORS["light_text"],
        fg=COLORS["text"],
        font=("Verdana", 10),
        wraplength=500,
        justify=LEFT,
        padx=10,
        pady=10
    )
    status_label.pack(fill=X, pady=20)
    
    # Button frame
    button_frame = Frame(content_frame, bg=COLORS["background"])
    button_frame.pack(fill=X, pady=20)
    
    # Fill attendance button
    fill_attendance_btn = Button(
        button_frame,
        text="Take Attendance",
        command=FillAttendance,
        bd=0,
        bg=COLORS["secondary"],
        fg=COLORS["light_text"],
        font=("Verdana", 12),
        padx=15,
        pady=8,
        cursor="hand2"
    )
    fill_attendance_btn.pack(side=LEFT, padx=10)
    
    # View records button
    view_records_btn = Button(
        button_frame,
        text="View Records",
        command=Attf,
        bd=0,
        bg=COLORS["accent"],
        fg=COLORS["light_text"],
        font=("Verdana", 12),
        padx=15,
        pady=8,
        cursor="hand2"
    )
    view_records_btn.pack(side=LEFT, padx=10)
    
    subject.mainloop()