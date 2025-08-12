# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 23:38:56 2025

@author: DELL
"""

import tkinter as tk
from tkinter import scrolledtext
from bs4 import BeautifulSoup
import requests
import pandas as pd
from joblib import load
import pickle
from scipy.sparse import csr_matrix
from googleapiclient.discovery import build
from graph import show_sentiment_graph
from googleapiclient.errors import HttpError
import webbrowser
from PIL import Image, ImageTk
import subprocess
import sys
from io import BytesIO

# --- Constants ---
DEVELOPER_KEY = "AIzaSyD3emiSTH3PqUQnqYZdiCh33DZE72lpfEw"
BG_IMG_WIDTH, BG_IMG_HEIGHT = 1500, 1500

# --- Sentiment Analysis Function ---
def analyze_sentiment(text):
    predictor = load("Best_Model.joblib")
    with open("vectorizer.pickle", 'rb') as vec_file:
        tf_vect = pickle.load(vec_file)
    X_test_tf = csr_matrix(tf_vect.transform([text]))
    y_predict = predictor.predict(X_test_tf)

    if y_predict[0] == 0:
        return text, "Negative Review"
    elif y_predict[0] == 1:
        return text, "Positive Review"
    else:
        return text, "Neutral Review"

# --- YouTube Comments Fetcher ---
def fetch_youtube_comments(video_id, part="snippet", max_results=100):
    youtube = build("youtube", "v3", developerKey=DEVELOPER_KEY)
    try:
        response = youtube.commentThreads().list(
            part=part,
            videoId=video_id,
            textFormat="plainText",
            maxResults=max_results
        ).execute()
        return [
            item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            for item in response.get("items", [])
        ]
    except HttpError as error:
        print(f"An HTTP error {error.resp.status} occurred:\n{error.content}")
        return []

# --- Fetch Video Details ---
def fetch_video_details(video_id):
    youtube = build("youtube", "v3", developerKey=DEVELOPER_KEY)
    try:
        response = youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()

        if response["items"]:
            snippet = response["items"][0]["snippet"]
            return snippet["title"], snippet["thumbnails"]["high"]["url"]
        return "No title", ""
    except HttpError as error:
        print(f"Error fetching video details: {error}")
        return "Error", ""

# --- Analyze Comments Callback ---
def analyze_youtube_comments():
    video_url = youtube_url_entry.get().strip()
    if not video_url:
        return

    video_id = video_url.split("v=")[-1]
    title, thumbnail_url = fetch_video_details(video_id)
    video_title_label.config(text=f"\U0001F4FA Title: {title}")

    # Display thumbnail
    try:
        img_data = requests.get(thumbnail_url).content
        img = Image.open(BytesIO(img_data)).resize((320, 180))
        thumbnail_img = ImageTk.PhotoImage(img)
        thumbnail_label.config(image=thumbnail_img)
        thumbnail_label.image = thumbnail_img
    except:
        print("Failed to load thumbnail")

    comments = fetch_youtube_comments(video_id)
    reviews_text.delete(1.0, tk.END)

    if not comments:
        reviews_text.insert(tk.END, "No comments found or an error occurred.")
        return

    pos, neg, neu = 0, 0, 0
    analyzed = []

    for comment in comments:
        comment, sentiment = analyze_sentiment(comment)
        analyzed.append((comment, sentiment))

        tag = "positive" if sentiment == "Positive Review" else \
              "negative" if sentiment == "Negative Review" else "neutral"

        if sentiment == "Positive Review": pos += 1
        elif sentiment == "Negative Review": neg += 1
        else: neu += 1

        reviews_text.insert(tk.END, f"Comment: {comment}\nSentiment: {sentiment}\n\n", tag)

    df = pd.DataFrame(analyzed, columns=["Comment", "Sentiment"])
    df.to_csv("youtube_comments_with_sentiment.csv", index=False)

    positive_count_label.config(text=f"\u2705 Positive Reviews: {pos}")
    negative_count_label.config(text=f"\u274C Negative Reviews: {neg}")
    neutral_count_label.config(text=f"\u2753 Neutral Reviews: {neu}")

    if pos > neg and pos > neu:
        overall_sentiment_label.config(text="\u2B50 Strong positive sentiment detected. Viewers appreciate this content.")
    elif neg > pos and neg > neu:
        overall_sentiment_label.config(text="\u26A0 Many users shared negative experiences. Consider investigating further.")
    else:
        overall_sentiment_label.config(text="\u2753 The reviews are largely neutral. Opinions are mixed.")

# --- Utility Buttons ---
def open_youtube(): webbrowser.open_new("https://www.youtube.com")
def open_graph(): show_sentiment_graph()
def open_custom_gui(): subprocess.Popen([sys.executable, "custom_comment.py"])

# --- GUI Setup ---
root = tk.Tk()
root.title("\U0001F4CA YouTube Sentiments Analyzer")
root.geometry(f"{BG_IMG_WIDTH}x{BG_IMG_HEIGHT}")
root.configure(bg="#ecf0f1")

# --- Background Image ---
try:
    image2 = Image.open('jjj.jpg').resize((BG_IMG_WIDTH, BG_IMG_HEIGHT), Image.LANCZOS)
    background_image = ImageTk.PhotoImage(image2)
    tk.Label(root, image=background_image).place(x=0, y=0)
except:
    print("Background image not loaded.")

# --- Header ---
header_frame = tk.Frame(root, bg="#2c3e50", height=80)
header_frame.pack(fill=tk.X)
tk.Label(header_frame, text="\U0001F4CA YouTube Sentiments Analyzer", font=("Helvetica", 22, "bold"), fg="white", bg="#2c3e50").pack(side=tk.LEFT, padx=20, pady=20)
tk.Button(header_frame, text="▶ Open YouTube", command=open_youtube, font=("Arial", 10, "bold"), bg="red", fg="white", cursor="hand2", relief=tk.FLAT).pack(side=tk.RIGHT, padx=20)

# --- Input ---
input_frame = tk.Frame(root, bg="black")
input_frame.pack(pady=20)
tk.Label(input_frame, text="Enter YouTube Video ID:", font=("Arial", 12), bg="#ecf0f1").grid(row=0, column=0, padx=10, sticky="e")
youtube_url_entry = tk.Entry(input_frame, width=50, font=("Arial", 12), bd=2, relief=tk.GROOVE)
youtube_url_entry.grid(row=0, column=1, padx=10)
tk.Button(input_frame, text="Analyze Comments", command=analyze_youtube_comments, font=("Arial", 12, "bold"), bg="#2980b9", fg="white", width=20, bd=0, relief=tk.RIDGE, cursor="hand2").grid(row=0, column=2, padx=10)

# --- Video Info ---
video_info_frame = tk.Frame(root, bg="#ecf0f1")
video_info_frame.pack(pady=10)
video_title_label = tk.Label(video_info_frame, text="", font=("Arial", 14, "bold"), bg="#ecf0f1")
video_title_label.pack(pady=5)
thumbnail_label = tk.Label(video_info_frame, bg="#ecf0f1")
thumbnail_label.pack()

# --- Buttons ---
button_frame = tk.Frame(video_info_frame, bg="black")
button_frame.pack(pady=10)
tk.Button(button_frame, text="Show Sentiment Graph", command=open_graph, font=("Arial", 11, "bold"), bg="#27ae60", fg="white", width=22, bd=0, relief=tk.RIDGE, cursor="hand2").grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Analyze Custom Comment", command=open_custom_gui, font=("Arial", 11, "bold"), bg="#8e44ad", fg="white", width=22, bd=0, relief=tk.RIDGE, cursor="hand2").grid(row=0, column=1, padx=10)

# --- Reviews Area ---
reviews_frame = tk.Frame(root, bg="#ecf0f1")
reviews_frame.pack(pady=10)
reviews_text = scrolledtext.ScrolledText(reviews_frame, width=110, height=10, wrap=tk.WORD, font=("Arial", 10), bd=2, relief=tk.GROOVE)
reviews_text.pack()
reviews_text.tag_config("positive", foreground="green")
reviews_text.tag_config("negative", foreground="red")
reviews_text.tag_config("neutral", foreground="blue")

# --- Counters ---
counter_frame = tk.Frame(root, bg="#ecf0f1")
counter_frame.pack(pady=10)
positive_count_label = tk.Label(counter_frame, text="\u2705 Positive Reviews: 0", font=("Arial", 12, "bold"), fg="green", bg="#ecf0f1")
positive_count_label.grid(row=0, column=0, padx=20)
negative_count_label = tk.Label(counter_frame, text="\u274C Negative Reviews: 0", font=("Arial", 12, "bold"), fg="red", bg="#ecf0f1")
negative_count_label.grid(row=0, column=1, padx=20)
neutral_count_label = tk.Label(counter_frame, text="\u2753 Neutral Reviews: 0", font=("Arial", 12, "bold"), fg="blue", bg="#ecf0f1")
neutral_count_label.grid(row=0, column=2, padx=20)

# --- Overall Summary ---
overall_sentiment_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="#ecf0f1", wraplength=800, justify="center")
overall_sentiment_label.pack(pady=20)

# --- Footer ---
tk.Label(root, text="Developed by Aarti - 2025", font=("Arial", 10), bg="#2c3e50", fg="white").pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
