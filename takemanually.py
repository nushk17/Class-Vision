import tkinter as tk
from tkinter import Message, Text, Frame, Label, Entry, Button, StringVar
import os
import csv
import numpy as np
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
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

# Get current timestamp
ts = time.time()
Date = datetime.datetime.fromtimestamp(ts).strftime("%Y_%m_%d")
timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
Hour, Minute, Second = timeStamp.split(":")

# Initialize dictionary for storing attendance data
d = {}
index = 0

def text_to_speech(text):
    """Placeholder for text-to-speech functionality"""
    # This would be implemented with pyttsx3 like in the main file
    pass

def testVal(inStr, acttyp):
    """Validate that input is numeric"""
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True

def manually_fill():
    """Main function for manual attendance entry"""
    # Create subject entry window
    subject_window = tk.Tk()
    subject_window.title("Class Vision - Enter Subject")
    subject_window.geometry("600x400")
    subject_window.configure(background=COLORS["background"])
    
    # Create header
    header_frame = Frame(subject_window, bg=COLORS["primary"], height=70)
    header_frame.pack(fill="x")
    
    header_label = Label(
        header_frame,
        text="Manual Attendance Entry",
        bg=COLORS["primary"],
        fg=COLORS["light_text"],
        font=("Verdana", 18, "bold"),
        pady=15
    )
    header_label.pack()
    
    # Content frame
    content_frame = Frame(subject_window, bg=COLORS["background"], padx=30, pady=30)
    content_frame.pack(fill="both", expand=True)
    
    # Error handler for empty subject
    def show_subject_error():
        error_window = tk.Toplevel(subject_window)
        error_window.title("Warning")
        error_window.geometry("400x150")
        error_window.configure(background=COLORS["background"])
        
        error_frame = Frame(error_window, bg=COLORS["warning"], padx=20, pady=20)
        error_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        Label(
            error_frame,
            text="Please enter a subject name!",
            bg=COLORS["warning"],
            fg=COLORS["light_text"],
            font=("Verdana", 14, "bold")
        ).pack(pady=10)
        
        Button(
            error_frame,
            text="OK",
            command=error_window.destroy,
            bg=COLORS["primary"],
            fg=COLORS["light_text"],
            font=("Verdana", 12),
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2"
        ).pack(pady=10)
    
    # Create attendance entry form
    def create_attendance_form():
        subject_name = subject_entry.get()
        
        if not subject_name:
            show_subject_error()
            text_to_speech("Please enter a subject name")
            return
        
        # Close the subject window
        subject_window.destroy()
        
        # Create attendance entry window
        attendance_window = tk.Tk()
        attendance_window.title(f"Class Vision - {subject_name} Attendance")
        attendance_window.geometry("800x600")
        attendance_window.configure(background=COLORS["background"])
        
        # Create header
        header_frame = Frame(attendance_window, bg=COLORS["primary"], height=70)
        header_frame.pack(fill="x")
        
        header_label = Label(
            header_frame,
            text=f"Manual Attendance for {subject_name}",
            bg=COLORS["primary"],
            fg=COLORS["light_text"],
            font=("Verdana", 18, "bold"),
            pady=15
        )
        header_label.pack()
        
        # Main content
        main_frame = Frame(attendance_window, bg=COLORS["background"], padx=30, pady=30)
        main_frame.pack(fill="both", expand=True)
        
        # Function to show error if fields are empty
        def show_empty_fields_error():
            error_window = tk.Toplevel(attendance_window)
            error_window.title("Warning")
            error_window.geometry("400x150")
            error_window.configure(background=COLORS["background"])
            
            error_frame = Frame(error_window, bg=COLORS["warning"], padx=20, pady=20)
            error_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            Label(
                error_frame,
                text="Please enter Student ID & Name!",
                bg=COLORS["warning"],
                fg=COLORS["light_text"],
                font=("Verdana", 14, "bold")
            ).pack(pady=10)
            
            Button(
                error_frame,
                text="OK",
                command=error_window.destroy,
                bg=COLORS["primary"],
                fg=COLORS["light_text"],
                font=("Verdana", 12),
                bd=0,
                padx=15,
                pady=5,
                cursor="hand2"
            ).pack(pady=10)
        
        # Form layout - left side
        form_frame = Frame(main_frame, bg=COLORS["background"])
        form_frame.pack(fill="both", expand=True)
        
        # Enrollment
        enrollment_label = Label(
            form_frame,
            text="Student ID:",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=("Verdana", 12),
            anchor="w"
        )
        enrollment_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        enrollment_entry = Entry(
            form_frame,
            validate="key",
            bg=COLORS["light_text"],
            fg=COLORS["text"],
            font=("Verdana", 14),
            relief="flat",
            highlightbackground="#cccccc",
            highlightthickness=1,
            width=25
        )
        enrollment_entry["validatecommand"] = (enrollment_entry.register(testVal), "%P", "%d")
        enrollment_entry.grid(row=0, column=1, padx=10, pady=10, ipady=5)
        
        # Clear enrollment button
        def clear_enrollment():
            enrollment_entry.delete(0, "end")
        
        clear_enrollment_btn = Button(
            form_frame,
            text="Clear",
            command=clear_enrollment,
            bg=COLORS["warning"],
            fg=COLORS["light_text"],
            font=("Verdana", 12),
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        clear_enrollment_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Student Name
        name_label = Label(
            form_frame,
            text="Student Name:",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=("Verdana", 12),
            anchor="w"
        )
        name_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        name_entry = Entry(
            form_frame,
            bg=COLORS["light_text"],
            fg=COLORS["text"],
            font=("Verdana", 14),
            relief="flat",
            highlightbackground="#cccccc",
            highlightthickness=1,
            width=25
        )
        name_entry.grid(row=1, column=1, padx=10, pady=10, ipady=5)
        
        # Clear name button
        def clear_name():
            name_entry.delete(0, "end")
        
        clear_name_btn = Button(
            form_frame,
            text="Clear",
            command=clear_name,
            bg=COLORS["warning"],
            fg=COLORS["light_text"],
            font=("Verdana", 12),
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        clear_name_btn.grid(row=1, column=2, padx=10, pady=10)
        
        # Notification area
        notification = Label(
            form_frame,
            text="Enter student details and click 'Enter Data'",
            bg=COLORS["light_text"],
            fg=COLORS["text"],
            font=("Verdana", 12),
            width=50,
            height=2,
            anchor="w",
            padx=10
        )
        notification.grid(row=2, column=0, columnspan=3, padx=10, pady=20, sticky="ew")
        
        # Function to add student to attendance
        def add_student():
            global index, d
            enrollment = enrollment_entry.get()
            student_name = name_entry.get()
            
            if not enrollment or not student_name:
                show_empty_fields_error()
                text_to_speech("Please enter both student ID and name")
                return
            
            # Add to dictionary
            if index == 0:
                d = {index: {"Enrollment": enrollment, "Name": student_name, Date: 1}}
            else:
                d[index] = {"Enrollment": enrollment, "Name": student_name, Date: 1}
            
            index += 1
            
            # Clear entries
            enrollment_entry.delete(0, "end")
            name_entry.delete(0, "end")
            
            # Update notification
            notification.config(
                text=f"Added: {enrollment} - {student_name}",
                bg=COLORS["success"],
                fg=COLORS["light_text"]
            )
            
            # Focus back on enrollment entry
            enrollment_entry.focus_set()
        
        # Function to create CSV
        def create_csv():
            if not d:
                notification.config(
                    text="No data to save. Please add students first.",
                    bg=COLORS["warning"],
                    fg=COLORS["light_text"]
                )
                return
            
            # Create attendance directory if it doesn't exist
            if not os.path.exists("Attendance(Manually)"):
                os.makedirs("Attendance(Manually)")
            
            # Create CSV file
            df = pd.DataFrame(d)
            csv_name = (
                "Attendance(Manually)/"
                + subject_name
                + "_"
                + Date
                + "_"
                + Hour
                + "-"
                + Minute
                + "-"
                + Second
                + ".csv"
            )
            df = df.transpose()  # Make it more readable
            df.to_csv(csv_name, index=False)
            
            notification.config(
                text=f"CSV created successfully: {csv_name}",
                bg=COLORS["success"],
                fg=COLORS["light_text"]
            )
            
            # Show record count
            record_count = len(d)
            summary_label.config(text=f"Total Records: {record_count}")
        
        # Button frame
        button_frame = Frame(form_frame, bg=COLORS["background"], pady=20)
        button_frame.grid(row=3, column=0, columnspan=3, sticky="ew")
        
        # Add student button
        add_btn = Button(
            button_frame,
            text="Enter Data",
            command=add_student,
            bg=COLORS["secondary"],
            fg=COLORS["light_text"],
            font=("Verdana", 12, "bold"),
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        add_btn.pack(side="left", padx=20)
        
        # Create CSV button
        csv_btn = Button(
            button_frame,
            text="Create CSV",
            command=create_csv,
            bg=COLORS["primary"],
            fg=COLORS["light_text"],
            font=("Verdana", 12, "bold"),
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        csv_btn.pack(side="left", padx=20)
        
        # Open folder button
        def open_folder():
            if os.path.exists("Attendance(Manually)"):
                os.startfile("Attendance(Manually)")
            else:
                notification.config(
                    text="Attendance folder does not exist yet",
                    bg=COLORS["warning"],
                    fg=COLORS["light_text"]
                )
        
        folder_btn = Button(
            button_frame,
            text="View Records",
            command=open_folder,
            bg=COLORS["accent"],
            fg=COLORS["light_text"],
            font=("Verdana", 12),
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        folder_btn.pack(side="left", padx=20)
        
        # Record summary
        summary_frame = Frame(main_frame, bg=COLORS["background"], pady=20)
        summary_frame.pack(fill="x")
        
        summary_label = Label(
            summary_frame,
            text="Total Records: 0",
            bg=COLORS["dark_bg"],
            fg=COLORS["light_text"],
            font=("Verdana", 12),
            padx=10,
            pady=5,
            width=20
        )
        summary_label.pack()
    
    # Subject entry components
    subject_label = Label(
        content_frame,
        text="Enter Subject Name:",
        bg=COLORS["background"],
        fg=COLORS["text"],
        font=("Verdana", 12),
        anchor="w"
    )
    subject_label.pack(fill="x", pady=10)
    
    entry_frame = Frame(content_frame, bg=COLORS["background"], highlightbackground="#cccccc", highlightthickness=1)
    entry_frame.pack(fill="x", pady=10)
    
    subject_entry = Entry(
        entry_frame,
        font=("Verdana", 14),
        bg=COLORS["light_text"],
        fg=COLORS["text"],
        relief="flat",
        bd=0
    )
    subject_entry.pack(fill="x", ipady=8, padx=2, pady=2)
    
    # Button to proceed
    button_frame = Frame(content_frame, bg=COLORS["background"], pady=20)
    button_frame.pack(fill="x")
    
    proceed_btn = Button(
        button_frame,
        text="Continue",
        command=create_attendance_form,
        bg=COLORS["primary"],
        fg=COLORS["light_text"],
        font=("Verdana", 12, "bold"),
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2"
    )
    proceed_btn.pack()
    
    # Instructions
    instruction_label = Label(
        content_frame,
        text="Enter the subject name for which you want to record attendance manually",
        bg=COLORS["background"],
        fg=COLORS["text"],
        font=("Verdana", 10),
        wraplength=500,
        justify="center"
    )
    instruction_label.pack(pady=20)
    
    subject_window.mainloop()

if __name__ == "__main__":
    manually_fill()