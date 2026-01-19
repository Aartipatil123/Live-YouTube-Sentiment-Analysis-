# Live YouTube Comment Sentiment Analysis System

A Machine Learning–based application that performs **real-time sentiment analysis on YouTube live comments** using Natural Language Processing (NLP).  
The system classifies comments into **Positive, Negative, or Neutral sentiments** through a user-friendly GUI.

---

## Problem Statement
With the rapid growth of YouTube live streaming, manually analyzing audience sentiment becomes difficult and time-consuming.  
This project automates the sentiment analysis of live YouTube comments to help creators and analysts **instantly understand audience reactions**.

---

## Features
- Fetches **live YouTube comments** using YouTube Data API  
- Sentiment classification using **Machine Learning & NLP**
- Supports **multiple ML models** (SVM, Random Forest)
- **GUI-based application** built with Tkinter
- User **Login & Registration system**
- CSV dataset support
- Stores sentiment results in a database

---

## Tech Stack
- **Programming Language:** Python  
- **Machine Learning:** SVM, Random Forest  
- **NLP:** TF-IDF, Text Preprocessing  
- **Libraries:** Pandas, NumPy, Scikit-learn, Joblib  
- **GUI:** Tkinter  
- **Database:** SQLite  
- **API:** YouTube Data API  

---

## How It Works
1. User logs in through the GUI  
2. Enters YouTube video ID  
3. Live comments are fetched via YouTube API  
4. Text preprocessing is applied  
5. Trained ML model predicts sentiment  
6. Results are displayed and stored  

---

## Project Structure
- `GUI_main.py` – Main GUI application  
- `train_new.py` – Model training  
- `test_new.py` – Model testing  
- `Best_Model.joblib` – Saved ML model  
- `comments_dataset.csv` – Training dataset  
- `login.py` / `registration.py` – Authentication system  

---

## Outcome
- Achieved accurate sentiment classification on live YouTube comments  
- Enabled real-time analysis of audience engagement  

---

## Future Scope
- Deep Learning models (LSTM, BERT)
- Real-time sentiment visualization (charts/graphs)
- Multi-language comment analysis
- Web-based deployment using Flask/Django

---

## Author
**Aarti Patil**  
MCA Graduate | Frontend & Python Full Stack Developer  
Pune  
LinkedIn: https://linkedin.com/in/aarti-patil
