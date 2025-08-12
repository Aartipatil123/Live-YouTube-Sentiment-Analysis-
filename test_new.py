import sys
import io
import joblib
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from sklearn.preprocessing import LabelEncoder

# ✅ Removed sys.stdout.buffer line

# Load the trained model and label encoder
model = joblib.load('sentiment_model.joblib')  # Assuming the model is saved as 'sentiment_model.joblib'
label_encoder = LabelEncoder()
label_encoder.fit(["negative", "neutral", "positive"])  # Make sure this matches your encoding

# Function to fetch YouTube comments
def fetch_youtube_comments(video_id, part="snippet", max_results=100):
    DEVELOPER_KEY = "AIzaSyD3emiSTH3PqUQnqYZdiCh33DZE72lpfEw"  # Replace with your valid YouTube API key
    youtube = build("youtube", "v3", developerKey=DEVELOPER_KEY)
    try:
        response = youtube.commentThreads().list(
            part=part,
            videoId=video_id,
            textFormat="plainText",
            maxResults=max_results
        ).execute()
        comments = [
            item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            for item in response.get("items", [])
        ]
        return comments
    except HttpError as error:
        print(f"An HTTP error {error.resp.status} occurred:\n{error.content}")
        return []

# Function to predict sentiment for fetched comments
def predict_comment_sentiment(comments):
    # Check if comments are empty
    if not comments:
        print("No comments fetched or video may be private.")
        return

    # Predict sentiment using the trained model
    predictions = model.predict(comments)
    predicted_classes = label_encoder.inverse_transform(predictions)
    
    # Print predictions for each comment
    for comment, sentiment in zip(comments, predicted_classes):
        try:
            print(f"Comment: {comment}\nPredicted Sentiment: {sentiment}\n")
        except UnicodeEncodeError:
            # Handle case where printing fails due to non-ASCII characters
            print(f"Comment (non-ASCII): {comment.encode('utf-8', 'ignore').decode('utf-8')}\nPredicted Sentiment: {sentiment}\n")

# Step 1: Fetch live comments from a YouTube video
video_id = "Xt01NHLjlgk"  # Replace with the YouTube video ID you want to fetch comments from
comments = fetch_youtube_comments(video_id)

# Step 2: Check if comments are fetched and predict sentiment for the fetched comments
predict_comment_sentiment(comments)
