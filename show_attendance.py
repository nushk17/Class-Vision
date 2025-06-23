import pandas as pd
from glob import glob
import os
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import csv

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

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return
    
        filenames = glob(f"Attendance\\{Subject}\\{Subject}*.csv")
        if not filenames:
            t = f"No attendance records found for {Subject}"
            text_to_speech(t)
            return
            
        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = 0
        for i in range(len(newdf)):
            newdf["Attendance"] = newdf["Attendance"].astype(str)
            newdf.loc[i, "Attendance"] = str(int(round(newdf.iloc[i, 2:-1].mean() * 100))) + '%'
        newdf.to_csv(f"Attendance\\{Subject}\\attendance.csv", index=False)

        # Create attendance display window
        root = tk.Tk()
        root.title("Attendance of " + Subject)
        root.geometry("800x600")
        root.configure(background=COLORS["background"])
        
        # Create header frame
        header = Frame(root, bg=COLORS["primary"], height=60)
        header.pack(fill=X)
        
        title = tk.Label(
            header, 
            text=f"Attendance Report: {Subject}", 
            bg=COLORS["primary"], 
            fg=COLORS["light_text"], 
            font=("Verdana", 16, "bold"),
            pady=10
        )
        title.pack()
        
        # Create content frame
        content_frame = Frame(root, bg=COLORS["background"], pady=20)
        content_frame.pack(fill=BOTH, expand=True)
        
        # Table headers styling
        header_style = {
            "bg": COLORS["dark_bg"],
            "fg": COLORS["light_text"],
            "font": ("Verdana", 12, "bold"),
            "padx": 5,
            "pady": 5,
            "relief": RIDGE,
            "bd": 1
        }
        
        # Table content styling
        row_style = {
            "bg": COLORS["light_text"],
            "fg": COLORS["text"],
            "font": ("Verdana", 10),
            "padx": 5,
            "pady": 5,
            "relief": RIDGE,
            "bd": 1
        }
        
        # Alternate row styling
        alt_row_style = {
            "bg": "#e8f4f8",
            "fg": COLORS["text"],
            "font": ("Verdana", 10),
            "padx": 5,
            "pady": 5,
            "relief": RIDGE,
            "bd": 1
        }
        
        # Read CSV and populate the table
        cs = f"Attendance\\{Subject}\\attendance.csv"
        with open(cs) as file:
            reader = csv.reader(file)
            r = 0
            
            for col in reader:
                c = 0
                for row in col:
                    # Apply header style to first row
                    if r == 0:
                        label = tk.Label(
                            content_frame,
                            width=15,
                            text=row,
                            **header_style
                        )
                    # Apply alternating row styles
                    else:
                        style = row_style if r % 2 == 0 else alt_row_style
                        # Highlight attendance percentage
                        if c == len(col) - 1:  # If it's the attendance column
                            att_value = int(row.strip('%'))
                            if att_value >= 75:
                                style["fg"] = COLORS["success"]
                            elif att_value < 60:
                                style["fg"] = COLORS["warning"]
                            style["font"] = ("Verdana", 10, "bold")
                            
                        label = tk.Label(
                            content_frame,
                            width=15,
                            text=row,
                            **style
                        )
                    
                    label.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
                    content_frame.grid_columnconfigure(c, weight=1)
                    c += 1
                r += 1
        
        # Create footer with export button
        footer = Frame(root, bg=COLORS["dark_bg"], height=50)
        footer.pack(side=BOTTOM, fill=X)
        
        def export_csv():
            os.startfile(cs)
        
        export_btn = Button(
            footer,
            text="Export CSV",
            command=export_csv,
            bd=0,
            font=("Verdana", 10),
            bg=COLORS["secondary"],
            fg=COLORS["light_text"],
            padx=10,
            pady=5,
            cursor="hand2"
        )
        export_btn.pack(side=RIGHT, padx=20, pady=10)
        
        root.mainloop()

    # Main subject selection window
    subject = Tk()
    subject.title("Class Vision - Select Subject")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background=COLORS["background"])
    
    # Create header
    header = Frame(subject, bg=COLORS["dark_bg"], height=60)
    header.pack(fill=X)
    
    title = tk.Label(
        header, 
        text="View Attendance Records", 
        bg=COLORS["dark_bg"], 
        fg=COLORS["light_text"], 
        font=("Verdana", 18, "bold"),
        pady=10
    )
    title.pack()
    
    # Create content frame
    content_frame = Frame(subject, bg=COLORS["background"], pady=20)
    content_frame.pack(fill=BOTH, expand=True)
    
    # Subject label
    tk.Label(
        content_frame,
        text="Enter Subject Name:",
        bg=COLORS["background"],
        fg=COLORS["text"],
        font=("Verdana", 12),
        anchor=W
    ).pack(fill=X, padx=50, pady=10)
    
    # Subject entry
    tx = tk.Entry(
        content_frame,
        bd=0,
        bg=COLORS["light_text"],
        fg=COLORS["text"],
        font=("Verdana", 14),
        relief=FLAT,
        highlightthickness=1,
        highlightbackground="#cccccc"
    )
    tx.pack(fill=X, ipady=5, padx=50)
    
    # Button frame
    button_frame = Frame(content_frame, bg=COLORS["background"], pady=20)
    button_frame.pack(fill=X)
    
    # Function to open folder with attendance files
    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            try:
                os.startfile(f"Attendance\\{sub}")
            except:
                t = f"Directory for {sub} not found"
                text_to_speech(t)

    # View Attendance button
    fill_a = tk.Button(
        button_frame,
        text="View Attendance",
        command=calculate_attendance,
        bd=0,
        font=("Verdana", 12),
        bg=COLORS["primary"],
        fg=COLORS["light_text"],
        padx=15,
        pady=8,
        cursor="hand2"
    )
    fill_a.pack(side=LEFT, padx=20, expand=True)
    
    # Check Sheets button
    attf = tk.Button(
        button_frame,
        text="Browse Files",
        command=Attf,
        bd=0,
        font=("Verdana", 12),
        bg=COLORS["accent"],
        fg=COLORS["light_text"],
        padx=15,
        pady=8,
        cursor="hand2"
    )
    attf.pack(side=LEFT, padx=20, expand=True)
    
    subject.mainloop()