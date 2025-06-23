import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

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

# Take Image of user with improved UI feedback
def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    if (l1 == "") and (l2==""):
        t='Please Enter the your Enrollment Number and Name.'
        text_to_speech(t)
    elif l1=='':
        t='Please Enter the your Enrollment Number.'
        text_to_speech(t)
    elif l2 == "":
        t='Please Enter the your Name.'
        text_to_speech(t)
    else:
        try:
            # Create directory if not exists
            if not os.path.exists("StudentDetails"):
                os.makedirs("StudentDetails")
                
            # Create CSV file if not exists
            if not os.path.isfile("StudentDetails/studentdetails.csv"):
                with open("StudentDetails/studentdetails.csv", 'a+') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(["Enrollment", "Name"])
                csvFile.close()
            
            # Initialize camera
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier(haarcasecade_path)
            Enrollment = l1
            Name = l2
            sampleNum = 0
            directory = Enrollment + "_" + Name
            path = os.path.join(trainimage_path, directory)
            
            # Create directory for student images
            os.makedirs(path, exist_ok=True)
            
            # Create a progress window
            progress_window = tk.Toplevel()
            progress_window.title("Capturing Images")
            progress_window.geometry("400x250")
            progress_window.configure(background=COLORS["background"])
            progress_window.resizable(False, False)
            
            # Create header
            header = tk.Frame(progress_window, bg=COLORS["primary"], height=60)
            header.pack(fill=tk.X)
            
            title = tk.Label(
                header, 
                text="Capturing Images", 
                bg=COLORS["primary"], 
                fg=COLORS["light_text"], 
                font=("Verdana", 14, "bold"),
                pady=10
            )
            title.pack()
            
            # Instruction label
            instruction = tk.Label(
                progress_window,
                text="Please look at the camera and move your head slightly.",
                bg=COLORS["background"],
                fg=COLORS["text"],
                font=("Verdana", 10),
                pady=10
            )
            instruction.pack()
            
            # Progress information
            progress_text = tk.StringVar()
            progress_text.set("Capturing image 0/50")
            
            progress_label = tk.Label(
                progress_window,
                textvariable=progress_text,
                bg=COLORS["background"],
                fg=COLORS["text"],
                font=("Verdana", 12),
                pady=5
            )
            progress_label.pack()
            
            # Progress bar
            progress_frame = tk.Frame(progress_window, bg=COLORS["background"], pady=10)
            progress_frame.pack(fill=tk.X, padx=20)
            
            progress_bar = tk.Frame(progress_frame, bg=COLORS["primary"], height=20, width=0)
            progress_bar.pack(fill=tk.X)
            
            # Cancel button
            def cancel_capture():
                cam.release()
                progress_window.destroy()
                
            cancel_btn = tk.Button(
                progress_window,
                text="Cancel",
                command=cancel_capture,
                bd=0,
                font=("Verdana", 10),
                bg=COLORS["warning"],
                fg=COLORS["light_text"],
                padx=10,
                pady=5,
                cursor="hand2"
            )
            cancel_btn.pack(side=tk.BOTTOM, pady=10)
            
            # Start image capture
            while True:
                ret, img = cam.read()
                if not ret:
                    messagebox.showerror("Error", "Cannot access the camera. Please check your camera connection.")
                    progress_window.destroy()
                    return
                    
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    
                    # Update progress
                    progress_text.set(f"Capturing image {sampleNum}/50")
                    progress_percent = int((sampleNum / 50) * 100)
                    progress_bar.config(width=progress_percent * 3.6)  # 360 is full width
                    progress_window.update()
                    
                    # Save the captured image
                    image_path = os.path.join(path, f"{Name}_{Enrollment}_{sampleNum}.jpg")
                    cv2.imwrite(image_path, gray[y:y+h, x:x+w])
                    
                    # Display the image being captured
                    cv2.imshow("Face Capturing", img)
                
                # Break if 'q' is pressed or we've captured enough images
                if cv2.waitKey(100) & 0xFF == ord("q"):
                    break
                elif sampleNum >= 50:
                    break
                    
            # Clean up
            cam.release()
            cv2.destroyAllWindows()
            progress_window.destroy()
            
            # Add to CSV
            row = [Enrollment, Name]
            with open("StudentDetails/studentdetails.csv", "a+") as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                writer.writerow(row)
                csvFile.close()
                
            # Update message
            res = f"Images Saved for ER No: {Enrollment}, Name: {Name}"
            message.configure(text=res)
            text_to_speech(res)
            
            # Show success dialog
            messagebox.showinfo("Success", f"Successfully captured 50 images for {Name}")
            
        except FileExistsError:
            message.configure(text="Student data already exists")
            text_to_speech("Student data already exists")
        except Exception as e:
            message.configure(text=f"Error: {str(e)}")
            text_to_speech(f"An error occurred: {str(e)}")