import os
import urllib.request
import ssl
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from langdetect import detect
from datetime import datetime, timedelta

# Read video IDs from a text file
def read_video_ids(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Function to get video details from YouTube API
def get_video_details(video_ids):
    api_key = os.getenv('YOUTUBE_API_KEY')
    base_url = "https://www.googleapis.com/youtube/v3/videos"
    details = []

    context = ssl._create_unverified_context()
    
    # YouTube API allows 50 IDs per request
    for i in range(0, len(video_ids), 50):
        ids_chunk = ",".join(video_ids[i:i+50])
        url = f"{base_url}?part=snippet&id={ids_chunk}&key={api_key}"
        with urllib.request.urlopen(url, context=context) as response:
            data = json.loads(response.read().decode())
            for item in data.get('items', []):
                snippet = item['snippet']
                video_data = {
                    'video_id': item['id'],
                    'published_at': snippet['publishedAt'],
                    'language': detect(snippet['title']),
                    'country': snippet.get('defaultAudioLanguage', 'Unknown')
                }
                details.append(video_data)
    
    return pd.DataFrame(details)

# Visualization function
def visualize_data(df):
    plt.figure(figsize=(14, 7))

    # Plot release dates
    plt.subplot(1, 3, 1)
    df['published_at'] = pd.to_datetime(df['published_at'])
    sns.histplot(df['published_at'].dt.date, kde=False, bins=30)
    plt.title('Distribution of Video Release Dates')
    plt.xlabel('Date')
    plt.ylabel('Number of Videos')

    # Plot primary languages
    plt.subplot(1, 3, 2)
    sns.countplot(y=df['language'], order=df['language'].value_counts().index)
    plt.title('Primary Language of Videos')
    plt.xlabel('Count')
    plt.ylabel('Language')

    # Plot countries/regions
    plt.subplot(1, 3, 3)
    sns.countplot(y=df['country'], order=df['country'].value_counts().index)
    plt.title('Country/Region of Creators')
    plt.xlabel('Count')
    plt.ylabel('Country/Region')

    plt.tight_layout()
    plt.show()

    # Save the visualization as an image
    plt.savefig('video_data_visualization.png')

# Function to analyze time periods
def analyze_time_periods(df):
    now = datetime.utcnow()
    day_ago = now - timedelta(days=1)
    week_ago = now - timedelta(weeks=1)
    month_ago = now - timedelta(days=30)
    year_ago = now - timedelta(days=365)

    within_day = df[df['published_at'] >= day_ago]
    within_week = df[df['published_at'] >= week_ago]
    within_month = df[df['published_at'] >= month_ago]
    within_year = df[df['published_at'] >= year_ago]

    print(f"Videos within the last day: {len(within_day)}")
    print(f"Videos within the last week: {len(within_week)}")
    print(f"Videos within the last month: {len(within_month)}")
    print(f"Videos within the last year: {len(within_year)}")

# Main function
def main(file_path):
    video_ids = read_video_ids(file_path)
    video_df = get_video_details(video_ids)
    visualize_data(video_df)
    analyze_time_periods(video_df)

# Path to the text file with video IDs
file_path = 'your_video_ids_file.txt'

# Run the main function
main('all-vids.txt')
