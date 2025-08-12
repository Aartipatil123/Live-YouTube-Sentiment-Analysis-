import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder

# Step 1: Load dataset from CSV
# Assuming you have a CSV file named 'train_data.csv'
# Replace 'train_data.csv' with the actual path to your dataset
df = pd.read_csv(r'D:/Final Project/Live_Youtube_comment_analysis updated code_Tkinter/Live_Youtube_comment_analysis/Live_Youtube_comment_analysis/Live_Youtube_comment_analysis/new.csv')

# Step 2: Preprocess the data
# Encode labels (target classes) as numbers
label_encoder = LabelEncoder()
df['target_encoded'] = label_encoder.fit_transform(df['target'])

# Step 3: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['target_encoded'], test_size=0.2, random_state=42)

# Step 4: Create a machine learning pipeline (TF-IDF + Logistic Regression)
model = make_pipeline(
    TfidfVectorizer(stop_words='english'),
    LogisticRegression(max_iter=1000)
)

# Step 5: Train the model
model.fit(X_train, y_train)

# Step 6: Evaluate the model on the test set
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Print detailed classification report
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Step 7: Save the model using joblib (or pickle)
# You can choose either joblib or pickle to save the model
joblib.dump(model, 'sentiment_model.joblib')  # Save the model as joblib file
# Alternatively, you can use pickle if you prefer:
# import pickle
# with open('sentiment_model.pkl', 'wb') as f:
#     pickle.dump(model, f)

print("Model saved successfully!")

# Step 8: Load the saved model and make predictions
# Load the model back
loaded_model = joblib.load('sentiment_model.joblib')  # Or use pickle.load if using pickle

# Test the model with a new sample
sample_text = ["This video was really helpful!"]
sample_pred = loaded_model.predict(sample_text)
predicted_class = label_encoder.inverse_transform(sample_pred)

print(f"Predicted class for the sample text: {predicted_class[0]}")
