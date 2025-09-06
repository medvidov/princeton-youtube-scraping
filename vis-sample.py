import os
import urllib.request
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from langdetect import detect
from dotenv import load_dotenv
import ssl

load_dotenv(override=True)

from langdetect import detect, LangDetectException

def get_video_details(video_ids):
    api_key = os.getenv('YOUTUBE_API_KEY')
    video_details = []

    # Create an SSL context to bypass SSL verification
    context = ssl._create_unverified_context()

    for video_id in video_ids:
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
        try:
            with urllib.request.urlopen(url, context=context) as response:
                data = json.loads(response.read().decode())

                for item in data.get('items', []):
                    snippet = item['snippet']
                    title = snippet.get('title', '')

                    # Attempt to detect language, handling potential exceptions
                    try:
                        language = detect(title) if title.strip() else 'unknown'
                    except LangDetectException:
                        language = 'unknown'

                    video_details.append({
                        'video_id': video_id,
                        'published_at': snippet['publishedAt'],
                        'title': title,
                        'channel_id': snippet['channelId'],
                        'language': language,
                    })
        except urllib.error.HTTPError as e:
            print(f"Failed to retrieve video details for {video_id}: {e.reason}")

    return pd.DataFrame(video_details)

# Function to get channel details using urllib
def get_channel_details(channel_ids):
    api_key = os.getenv('YOUTUBE_API_KEY')
    channel_details = []

    # Create an SSL context to bypass SSL verification
    context = ssl._create_unverified_context()

    for channel_id in channel_ids:
        url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={api_key}"
        with urllib.request.urlopen(url, context=context) as response:
            data = json.loads(response.read().decode())

            for item in data.get('items', []):
                snippet = item['snippet']
                channel_details.append({
                    'channel_id': channel_id,
                    'country': snippet.get('country', 'unknown')
                })

    return pd.DataFrame(channel_details)

# Load video IDs from text file
def load_video_ids(file_path):
    with open(file_path, 'r') as file:
        video_ids = file.read().splitlines()
    return video_ids

# Combine video and channel data
def combine_data(video_df, channel_df):
    combined_df = pd.merge(video_df, channel_df, on='channel_id', how='left')
    combined_df['published_at'] = pd.to_datetime(combined_df['published_at'])
    return combined_df

# Visualization function
def visualize_data(df):
    plt.figure(figsize=(14, 7))
    
    # Plot release dates
    plt.subplot(1, 3, 1)
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
    plt.savefig('video_data.png')
    plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Assuming you have a DataFrame 'video_df' with the following columns:
# 'published_at' (datetime), 'language', 'country'

def analyze_and_plot_data(video_df):
    # Convert 'published_at' to datetime if it's not already
    video_df['published_at'] = pd.to_datetime(video_df['published_at'])

    # 1. **Plotting Languages**
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 2, 1)
    sns.countplot(y=video_df['language'], order=video_df['language'].value_counts().index)
    plt.title('Distribution of Video Languages')
    plt.xlabel('Count')
    plt.ylabel('Language')
    
    # 2. **Plotting Country/Region**
    plt.subplot(2, 2, 2)
    sns.countplot(y=video_df['country'], order=video_df['country'].value_counts().index)
    plt.title('Distribution of Video Countries/Regions')
    plt.xlabel('Count')
    plt.ylabel('Country/Region')
    
    # 3. **Plotting Publication Times**
    plt.subplot(2, 2, 3)
    sns.histplot(video_df['published_at'].dt.date, kde=False, bins=30)
    plt.title('Distribution of Video Release Dates')
    plt.xlabel('Date')
    plt.ylabel('Number of Videos')
    
    plt.tight_layout()
    plt.savefig('video_data2.png')
    plt.show()

    # 4. **Calculating Proportions**
    now = datetime.now()
    one_day_ago = now - timedelta(days=1)
    one_week_ago = now - timedelta(weeks=1)
    one_month_ago = now - timedelta(days=30)
    one_year_ago = now - timedelta(days=365)

    total_videos = len(video_df)

    within_one_day = len(video_df[video_df['published_at'] > one_day_ago]) / total_videos
    within_one_week = len(video_df[video_df['published_at'] > one_week_ago]) / total_videos
    within_one_month = len(video_df[video_df['published_at'] > one_month_ago]) / total_videos
    within_one_year = len(video_df[video_df['published_at'] > one_year_ago]) / total_videos

    print(f"Proportion of videos within the last day: {within_one_day:.2%}")
    print(f"Proportion of videos within the last week: {within_one_week:.2%}")
    print(f"Proportion of videos within the last month: {within_one_month:.2%}")
    print(f"Proportion of videos within the last year: {within_one_year:.2%}")

# Example usage
# Assuming 'video_df' is your DataFrame
# analyze_and_plot_data(video_df)


# Main execution
def main(file_path):
    video_ids = load_video_ids(file_path)
    video_df = get_video_details(video_ids)
    analyze_and_plot_data(video_df)
    channel_df = get_channel_details(video_df['channel_id'].unique())
    combined_df = combine_data(video_df, channel_df)
    visualize_data(combined_df)

# Run the script
if __name__ == "__main__":
    file_path = 'videos.txt'
    main(file_path)

# Time bound the sample
