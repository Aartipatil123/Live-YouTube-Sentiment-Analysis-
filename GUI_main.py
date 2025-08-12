import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

root = tk.Tk()
root.configure(background="white")

# Fullscreen dimensions
# w, h = root.winfo_screenwidth(), root.winfo_screenheight()
# root.geometry("%dx%d+0+0" % (w, h))
# root.title("Home")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{w}x{h}+0+0")
root.title("Live YouTube Comment Analysis")

# Background Image
image2 = Image.open('2.jpg').resize((w, h), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image2)
background_label = tk.Label(root, image=background_image)
background_label.image = background_image
background_label.place(x=0, y=0)
# Path to background video
# video_path = "v1.mp4"

# # Function to play background video
# def play_video():
#     cap = cv2.VideoCapture(video_path)

#     def update_frame():
#         ret, frame = cap.read()
#         if ret:
#             frame = cv2.resize(frame, (w, h))
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             frame_image = ImageTk.PhotoImage(image=Image.fromarray(frame))
#             background_label.configure(image=frame_image)
#             background_label.image = frame_image
#             root.after(10, update_frame)
#         else:
#             cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             update_frame()

#     update_frame()

# # Label for video background
# background_label = tk.Label(root)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Title label
# title_label = tk.Label(
#     root,
#     text="Social Media Insights Analyzer",
#     font=("Helvetica", 26, 'bold'),
#     bg="black",
#     fg="white",
#     padx=20,
#     pady=10
# )
#title_label.place(relx=0.5, y=450, anchor="center")

# Navigation Functions
def reg():
    root.destroy()
    from subprocess import call
    call(["python", "registration.py"])

def log():
    root.destroy()
    from subprocess import call
    call(["python", "login.py"])

def window():
    root.destroy()

# Hover Effects
def on_enter(e):
    e.widget.config(bg="#ff4d4d", fg="black")

def on_leave(e):
    e.widget.config(bg="black", fg="white")

# Button Styling
button_style = {
    "width": 17,
    "height": 2,
    "font": ('times', 15, 'bold'),
    "bg": "black",
    "fg": "white",
    "activebackground": "#ff4d4d",
    "activeforeground": "black",
    "relief": "ridge",
    "bd": 4  # Thicker border for 'thicc' effect
}

# Buttons with Effects
button1 = tk.Button(root, text="LOGIN", command=log, **button_style)
button1.place(x=200, y=300)
button1.bind("<Enter>", on_enter)
button1.bind("<Leave>", on_leave)

button2 = tk.Button(root, text="REGISTER", command=reg, **button_style)
button2.place(x=200, y=400)
button2.bind("<Enter>", on_enter)
button2.bind("<Leave>", on_leave)

button3 = tk.Button(root, text="EXIT", command=window, **button_style)
button3.place(x=200, y=500)
button3.bind("<Enter>", on_enter)
button3.bind("<Leave>", on_leave)

#play_video()
root.mainloop()
