import requests
import cv2
import numpy as np
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import threading
import time

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

def start_stream(url, status_label):
    """Function to handle camera streaming in a separate thread"""
    global running
    running = True
    
    try:
        status_label.config(text="Connecting to camera...", bg=COLORS["accent"], fg=COLORS["light_text"])
        
        while running:
            try:
                cam = requests.get(url, timeout=1)
                imgNp = np.array(bytearray(cam.content), dtype=np.uint8)
                img = cv2.imdecode(imgNp, -1)
                
                if img is not None:
                    # Process frame if needed
                    cv2.imshow("IP Camera Stream", img)
                    
                    # Break loop if 'q' is pressed
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                    
                status_label.config(text="Connected - Streaming from IP camera", bg=COLORS["success"], fg=COLORS["light_text"])
            except Exception as e:
                status_label.config(text=f"Error: {str(e)}", bg=COLORS["warning"], fg=COLORS["light_text"])
                time.sleep(1)  # Wait before retrying
                
    except Exception as e:
        status_label.config(text=f"Failed to connect: {str(e)}", bg=COLORS["warning"], fg=COLORS["light_text"])
    
    finally:
        cv2.destroyAllWindows()

def stop_stream():
    """Function to stop streaming"""
    global running
    running = False
    cv2.destroyAllWindows()

def create_camera_ui():
    """Create UI for IP camera connection"""
    root = tk.Tk()
    root.title("Class Vision - IP Camera Connection")
    root.geometry("600x400")
    root.configure(background=COLORS["background"])
    
    # Create header
    header_frame = Frame(root, bg=COLORS["dark_bg"], height=70)
    header_frame.pack(fill=X)
    
    title = Label(
        header_frame,
        text="IP Camera Connection",
        font=("Verdana", 18, "bold"),
        bg=COLORS["dark_bg"],
        fg=COLORS["light_text"],
        pady=15
    )
    title.pack()
    
    # Create main content frame
    content_frame = Frame(root, bg=COLORS["background"], pady=20)
    content_frame.pack(fill=BOTH, expand=True, padx=30)
    
    # Camera URL entry
    url_label = Label(
        content_frame,
        text="Camera URL:",
        font=("Verdana", 12),
        bg=COLORS["background"],
        fg=COLORS["text"],
        anchor="w"
    )
    url_label.pack(fill=X, pady=5)
    
    entry_frame = Frame(content_frame, bg=COLORS["background"], highlightbackground="#cccccc", highlightthickness=1)
    entry_frame.pack(fill=X, pady=10)
    
    url_entry = Entry(
        entry_frame,
        font=("Verdana", 12),
        bg=COLORS["light_text"],
        fg=COLORS["text"],
        relief=FLAT,
        bd=0
    )
    url_entry.pack(fill=X, ipady=8, padx=2, pady=2)
    url_entry.insert(0, "http://192.168.0.6:8080/shot.jpg")  # Default URL
    
    # Status label
    status_label = Label(
        content_frame,
        text="Enter IP camera URL and click Connect",
        font=("Verdana", 10),
        bg=COLORS["light_text"],
        fg=COLORS["text"],
        wraplength=500,
        justify=LEFT,
        padx=10,
        pady=10
    )
    status_label.pack(fill=X, pady=20)
    
    # Button frame
    button_frame = Frame(content_frame, bg=COLORS["background"])
    button_frame.pack(fill=X, pady=10)
    
    # Connect button
    def on_connect():
        url = url_entry.get()
        if url:
            threading.Thread(target=start_stream, args=(url, status_label), daemon=True).start()
        else:
            status_label.config(text="Please enter a valid URL", bg=COLORS["warning"], fg=COLORS["light_text"])
    
    connect_btn = Button(
        button_frame,
        text="Connect",
        command=on_connect,
        font=("Verdana", 12),
        bg=COLORS["primary"],
        fg=COLORS["light_text"],
        bd=0,
        cursor="hand2",
        padx=15,
        pady=8
    )
    connect_btn.pack(side=LEFT, padx=10)
    
    # Disconnect button
    disconnect_btn = Button(
        button_frame,
        text="Disconnect",
        command=stop_stream,
        font=("Verdana", 12),
        bg=COLORS["warning"],
        fg=COLORS["light_text"],
        bd=0,
        cursor="hand2",
        padx=15,
        pady=8
    )
    disconnect_btn.pack(side=LEFT, padx=10)
    
    # Instructions
    instruction_label = Label(
        content_frame,
        text="Note: You can press 'q' to close the camera window",
        font=("Verdana", 10, "italic"),
        bg=COLORS["background"],
        fg=COLORS["text"],
        anchor="w"
    )
    instruction_label.pack(fill=X, pady=10)
    
    # Handle window close
    def on_closing():
        stop_stream()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    create_camera_ui()