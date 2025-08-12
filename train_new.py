import pandas as pd
import numpy as np
import re
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pickle
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from textblob import TextBlob
from joblib import dump

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def preprocess_data():
    result = pd.read_csv(r"D:/Final Project/Live_Youtube_comment_analysis updated code_Tkinter/Live_Youtube_comment_analysis/Live_Youtube_comment_analysis/Live_Youtube_comment_analysis/comments_dataset.csv", encoding='unicode_escape')
    result = result.dropna(subset=['Comment', 'Sentiment'])
    result['Comment'] = result['Comment'].fillna('').astype(str)
    result['headline_without_stopwords'] = result['Comment'].apply(lambda x: ' '.join([word for word in str(x).split() if word.lower() not in set(nltk.corpus.stopwords.words('english'))]))
    result['pos'] = result['headline_without_stopwords'].apply(lambda x: " ".join(["/".join(tag) for tag in TextBlob(x).tags]))
    return result

def train_best_model():
    result = preprocess_data()
    
    review_train, review_test, label_train, label_test = train_test_split(result['pos'], result['Sentiment'], test_size=0.2, random_state=42)
    
    tf_vect = TfidfVectorizer(lowercase=True, use_idf=True, smooth_idf=True, sublinear_tf=False)
    X_train_tf = tf_vect.fit_transform(review_train)
    X_test_tf = tf_vect.transform(review_test)
    
    models = {
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
        "GradientBoosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
        "SVM": SVC(C=10, gamma=0.001, kernel='linear'),
        "NaiveBayes": MultinomialNB()
    }
    
    best_model = None
    best_accuracy = 0
    best_model_name = ""
    
    for name, model in models.items():
        model.fit(X_train_tf, label_train)
        predictions = model.predict(X_test_tf)
        accuracy = accuracy_score(label_test, predictions)
        print(f"{name} Accuracy: {accuracy:.2f}")
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = model
            best_model_name = name
    
    print(f"Best Model: {best_model_name} with Accuracy: {best_accuracy:.2f}")
    
    with open('vectorizer.pickle', 'wb') as f:
        pickle.dump(tf_vect, f)
    
    dump(best_model, "Best_Model.joblib")
    print("Best model saved as Best_Model.joblib")

def main():
    train_best_model()

if __name__ == "__main__":
    main()