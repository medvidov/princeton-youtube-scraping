import os
import requests
from playwright.sync_api import sync_playwright
from collections import Counter
import matplotlib.pyplot as plt
import ssl
from dotenv import load_dotenv
import os

load_dotenv(override=True)
api_key = os.getenv('YOUTUBE_API_KEY')

# Function to get the associated channel ID from a video URL
def get_channel_from_video(video_id):

    api_key = os.getenv('YOUTUBE_API_KEY')
    
    video_api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
    response = requests.get(video_api_url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve video data: {response.status_code}")
        return None
    
    video_data = response.json()

    # Get the channel ID from the video data
    if 'items' in video_data and video_data['items']:
        channel_id = video_data['items'][0]['snippet']['channelId']
    else:
        print(f"No data found for video: {video_id}")
        return None
    
    return channel_id

if __name__ == '__main__':
    # Get list of video URLs from all_videos.txt
    with open('all-vids.txt', 'r') as f:
        video_urls = f.readlines()

    print(len(video_urls))

    # Iterate through video_urls and add channel ID to set until we have 10000 unique channel IDs
    channel_ids = set()
    for video_url in video_urls:
        channel_id = get_channel_from_video(video_url)
        if channel_id:
            channel_ids.add(channel_id)
            if len(channel_ids) % 100 == 0:
                print(f"Found {len(channel_ids)} unique channel IDs")
            if len(channel_ids) >= 500:
                break
    # For each channel, count number of videos using YouTube API
    video_counts = {}
    for channel_id in channel_ids:
        channel_api_url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}"
        response = requests.get(channel_api_url)
        if response.status_code == 200:
            channel_data = response.json()
            if 'items' in channel_data and channel_data['items']:
                video_count = channel_data['items'][0]['statistics'].get('videoCount', 0)
                video_counts[channel_id] = video_count
            else:
                print(f"No data found for channel: {channel_id}")
        else:
            print(f"Failed to retrieve channel data: {response.status_code}")

    # Make histogram of video counts
    counter = Counter(video_counts.values())
    plt.bar(counter.keys(), counter.values())
    plt.xlabel('Number of Videos')
    plt.ylabel('Number of Channels')
    plt.title('Distribution of Videos per Channel')
    # Save the plot to a file
    plt.savefig('video_count_distribution.png')
    plt.show()
