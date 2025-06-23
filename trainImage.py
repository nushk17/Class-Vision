import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox

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

# Train Image with better UI feedback
def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    # Create training progress window
    training_window = tk.Toplevel()
    training_window.title("Training Model")
    training_window.geometry("400x250")
    training_window.configure(background=COLORS["background"])
    training_window.resizable(False, False)
    
    # Create header
    header = tk.Frame(training_window, bg=COLORS["dark_bg"], height=60)
    header.pack(fill=tk.X)
    
    title = tk.Label(
        header, 
        text="Training Facial Recognition Model", 
        bg=COLORS["dark_bg"], 
        fg=COLORS["light_text"], 
        font=("Verdana", 14, "bold"),
        pady=10
    )
    title.pack()
    
    # Create content frame
    content_frame = tk.Frame(training_window, bg=COLORS["background"], pady=20)
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    # Status label
    status_var = tk.StringVar()
    status_var.set("Initializing training...")
    
    status_label = tk.Label(
        content_frame,
        textvariable=status_var,
        bg=COLORS["background"],
        fg=COLORS["text"],
        font=("Verdana", 10),
        pady=10
    )
    status_label.pack()
    
    # Progress bar
    progress_bar = ttk.Progressbar(
        content_frame, 
        orient=tk.HORIZONTAL, 
        length=300, 
        mode='indeterminate'
    )
    progress_bar.pack(pady=20)
    progress_bar.start(10)
    
    # Update the window
    training_window.update()
    
    try:
        # Check if path exists
        if not os.path.exists(trainimage_path):
            status_var.set("Error: Training images folder not found")
            training_window.update()
            time.sleep(2)
            training_window.destroy()
            message.configure(text="Error: Training images folder not found")
            text_to_speech("Error: Training images folder not found")
            return
        
        # Check if there are students to train
        if len(os.listdir(trainimage_path)) == 0:
            status_var.set("No students registered to train")
            training_window.update()
            time.sleep(2)
            training_window.destroy()
            message.configure(text="No students registered to train")
            text_to_speech("No students registered to train")
            return
        
        # Create recognizer
        status_var.set("Initializing facial recognition model...")
        training_window.update()
        
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier(haarcasecade_path)
        
        # Get images and labels
        status_var.set("Processing training images...")
        training_window.update()
        
        faces, Id = getImagesAndLabels(trainimage_path, status_var, training_window)
        
        if len(faces) == 0:
            status_var.set("No faces detected in the training images")
            training_window.update()
            time.sleep(2)
            training_window.destroy()
            message.configure(text="No faces detected in the training images")
            text_to_speech("No faces detected in the training images")
            return
        
        # Train the model
        status_var.set(f"Training model with {len(faces)} facial images...")
        training_window.update()
        
        recognizer.train(faces, np.array(Id))
        
        # Save the model
        status_var.set("Saving the trained model...")
        training_window.update()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(trainimagelabel_path), exist_ok=True)
        recognizer.save(trainimagelabel_path)
        
        # Complete
        status_var.set("Training completed successfully!")
        progress_bar.stop()
        progress_bar['value'] = 100
        progress_bar['mode'] = 'determinate'
        training_window.update()
        
        # Wait a moment before closing
        time.sleep(2)
        training_window.destroy()
        
        # Update message in main window
        res = "Model trained successfully!"
        message.configure(text=res)
        text_to_speech(res)
        
        # Show success dialog
        messagebox.showinfo("Success", "Facial recognition model has been trained successfully!")
        
    except Exception as e:
        status_var.set(f"Error: {str(e)}")
        training_window.update()
        time.sleep(2)
        training_window.destroy()
        message.configure(text=f"Error: {str(e)}")
        text_to_speech(f"An error occurred during training: {str(e)}")

def getImagesAndLabels(path, status_var=None, window=None):
    # Get all directories inside path (one directory per student)
    student_dirs = [os.path.join(path, d) for d in os.listdir(path)]
    faces = []
    Ids = []
    
    # Total number of student directories
    total_dirs = len(student_dirs)
    
    for i, student_dir in enumerate(student_dirs):
        if status_var and window:
            status_var.set(f"Processing student {i+1}/{total_dirs}")
            window.update()
            
        # Get all image files in this student's directory
        try:
            image_paths = [os.path.join(student_dir, f) for f in os.listdir(student_dir)]
        except:
            # Skip if not a directory
            continue
            
        for imagePath in image_paths:
            try:
                # Open image and convert to grayscale
                pilImage = Image.open(imagePath).convert("L")
                imageNp = np.array(pilImage, "uint8")
                
                # Extract student ID from filename
                Id = int(os.path.split(imagePath)[-1].split("_")[1])
                
                # Add image and ID to training data
                faces.append(imageNp)
                Ids.append(Id)
            except Exception as e:
                print(f"Error processing image {imagePath}: {str(e)}")
                continue
    
    return faces, Ids