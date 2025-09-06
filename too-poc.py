# import os
# import requests

# def get_channel_id(channel_url):
#     """Extracts the channel ID from a YouTube channel URL."""
#     return channel_url.split("/")[-1]

# def get_recent_videos(channel_id):
#     api_key = os.getenv('YOUTUBE_API_KEY')
    
#     # Get the upload playlist ID for the channel
#     channel_url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={api_key}"
#     channel_response = requests.get(channel_url)
    
#     if channel_response.status_code != 200:
#         print(f"Failed to retrieve channel details: {channel_response.status_code}")
#         return []

#     channel_data = channel_response.json()
#     upload_playlist_id = channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
#     # Get the most recent 20 videos from the upload playlist
#     playlist_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={upload_playlist_id}&maxResults=20&key={api_key}"
#     playlist_response = requests.get(playlist_url)
    
#     if playlist_response.status_code != 200:
#         print(f"Failed to retrieve videos: {playlist_response.status_code}")
#         return []

#     playlist_data = playlist_response.json()
#     videos = [
#         {
#             'video_id': item['snippet']['resourceId']['videoId'],
#             'title': item['snippet']['title']
#         }
#         for item in playlist_data['items']
#     ]
    
#     return videos

# def get_subscriber_count(channel_id):
#     api_key = os.getenv('YOUTUBE_API_KEY')
    
#     channel_url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}"
#     response = requests.get(channel_url)
    
#     if response.status_code != 200:
#         print(f"Failed to retrieve subscriber count: {response.status_code}")
#         return None
    
#     channel_data = response.json()
#     subscriber_count = channel_data['items'][0]['statistics']['subscriberCount']
    
#     return int(subscriber_count)

# def get_video_count(channel_id):
#     api_key = os.getenv('YOUTUBE_API_KEY')
    
#     channel_url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}"
#     response = requests.get(channel_url)
    
#     if response.status_code != 200:
#         print(f"Failed to retrieve video count: {response.status_code}")
#         return None
    
#     channel_data = response.json()
#     video_count = channel_data['items'][0]['statistics']['videoCount']
    
#     return int(video_count)

# def get_video_statistics(video_id):
#     api_key = os.getenv('YOUTUBE_API_KEY')
    
#     video_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={api_key}"
#     response = requests.get(video_url)
    
#     if response.status_code != 200:
#         print(f"Failed to retrieve video statistics: {response.status_code}")
#         return None
    
#     video_data = response.json()
#     snippet = video_data['items'][0]['snippet']
#     statistics = video_data['items'][0]['statistics']
    
#     video_info = {
#         'title': snippet['title'],
#         'date_posted': snippet['publishedAt'],
#         'comment_count': int(statistics.get('commentCount', 0)),
#         'like_count': int(statistics.get('likeCount', 0))
#     }
    
#     return video_info

# def main():
#     channel_url = 'https://www.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA'
#     channel_id = get_channel_id(channel_url)
    
#     # Fetch channel statistics
#     subscriber_count = get_subscriber_count(channel_id)
#     video_count = get_video_count(channel_id)
    
#     print(f"Channel ID: {channel_id}")
#     print(f"Subscriber Count: {subscriber_count}")
#     print(f"Total Video Count: {video_count}")
    
#     # Fetch recent videos
#     recent_videos = get_recent_videos(channel_id)
    
#     if recent_videos:
#         print("\nRecent Videos:")
#         for video in recent_videos:
#             print(f"Title: {video['title']} (Video ID: {video['video_id']})")
        
#         # Fetch detailed statistics for each video
#         print("\nDetailed Video Statistics:")
#         for video in recent_videos:
#             stats = get_video_statistics(video['video_id'])
#             print(f"Title: {stats['title']}")
#             print(f"Date Posted: {stats['date_posted']}")
#             print(f"Comments: {stats['comment_count']}")
#             print(f"Likes: {stats['like_count']}\n")
#     else:
#         print("No recent videos found.")

# if __name__ == "__main__":
#     main()

import os
import requests
from playwright.sync_api import sync_playwright

# Function to extract the channel ID from a channel URL
def get_channel_id(channel_url):
    return channel_url.split("/")[-1]

# Function to get a specified number of recent videos posted to a channel
def get_recent_videos(channel_id, max_results=20):
    api_key = os.getenv('YOUTUBE_API_KEY')
    channel_url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={api_key}"
    channel_response = requests.get(channel_url)
    
    if channel_response.status_code != 200:
        print(f"Failed to retrieve channel details: {channel_response.status_code}")
        return []

    channel_data = channel_response.json()
    upload_playlist_id = channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    playlist_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={upload_playlist_id}&maxResults={max_results}&key={api_key}"
    playlist_response = requests.get(playlist_url)
    
    if playlist_response.status_code != 200:
        print(f"Failed to retrieve videos: {playlist_response.status_code}")
        return []

    playlist_data = playlist_response.json()
    videos = []
    
    for item in playlist_data['items']:
        video_id = item['snippet']['resourceId'].get('videoId')
        
        if video_id and isinstance(video_id, str):
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append({
                'video_id': video_id,
                'title': item['snippet']['title'],
                'url': video_url
            })
        else:
            print(f"Invalid video data encountered: {item}")

    for video in videos:
        print(video)
    
    return videos



# Function to get the number of subscribers for the channel
def get_subscriber_count(channel_id):
    api_key = os.getenv('YOUTUBE_API_KEY')
    channel_url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}"
    response = requests.get(channel_url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve subscriber count: {response.status_code}")
        return None
    
    channel_data = response.json()
    subscriber_count = channel_data['items'][0]['statistics']['subscriberCount']
    
    return int(subscriber_count)

# Function to get the number of videos posted on the channel
def get_video_count(channel_id):
    api_key = os.getenv('YOUTUBE_API_KEY')
    channel_url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}"
    response = requests.get(channel_url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve video count: {response.status_code}")
        return None
    
    channel_data = response.json()
    video_count = channel_data['items'][0]['statistics']['videoCount']
    
    return int(video_count)

# Function to get video statistics: date posted, number of comments, and number of likes
def get_video_statistics(video_id):
    api_key = os.getenv('YOUTUBE_API_KEY')
    video_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={api_key}"
    response = requests.get(video_url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve video statistics: {response.status_code}")
        return None
    
    video_data = response.json()
    snippet = video_data['items'][0]['snippet']
    statistics = video_data['items'][0]['statistics']
    
    video_info = {
        'title': snippet['title'],
        'date_posted': snippet['publishedAt'],
        'comment_count': int(statistics.get('commentCount', 0)),
        'like_count': int(statistics.get('likeCount', 0))
    }
    
    return video_info

# Function to get recommended video links using Playwright with an incognito context
def get_recommended_videos(video_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()  # Create an incognito browser context
        page = context.new_page()
        page.goto(video_url)

        page.wait_for_selector('a#thumbnail')
        recommendation_links = page.eval_on_selector_all('a#thumbnail', "elements => elements.map(e => e.href)")

        context.close()  # Close the incognito context
        browser.close()

    # Print the recommendation links
    for link in recommendation_links:
        print('Video:', link)
    
    return recommendation_links


# Function to get the associated channel ID from a video URL
def get_channel_from_video(video_url):
    api_key = os.getenv('YOUTUBE_API_KEY')
    
    # Check if it's a YouTube Short
    if '/shorts/' in video_url:
        print(f"Note: The video is a Short: {video_url}")
        return None  # Skip further processing for Shorts
    
    # Ensure the video URL has a video ID
    if 'v=' not in video_url:
        print(f"Invalid video URL: {video_url}")
        return None
    
    video_id = video_url.split('v=')[-1].split('&')[0].strip()
    
    # Check if video_id is valid (not empty)
    if not video_id:
        print(f"Failed to extract video ID from URL: {video_url}")
        return None
    
    video_api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
    response = requests.get(video_api_url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve video data: {response.status_code}")
        return None
    
    video_data = response.json()
    if 'items' not in video_data or not video_data['items']:
        print(f"No data found for video: {video_api_url}")
        return None
    
    channel_id = video_data['items'][0]['snippet']['channelId']
    
    return channel_id


# Main function to run the process up to a specified depth
def main(starting_channels, max_depth=2):
    processed_channels = set()

    def process_channel(channel_id, depth):
        if channel_id in processed_channels or depth > max_depth:
            return
        processed_channels.add(channel_id)

        print(f"Processing Channel ID: {channel_id}, Depth: {depth}")
        
        # Get channel statistics
        subscriber_count = get_subscriber_count(channel_id)
        if subscriber_count < 10000:
            print(f"Skipping Channel ID {channel_id}: Less than 10,000 subscribers.")
            return
        
        video_count = get_video_count(channel_id)
        print(f"Subscriber Count: {subscriber_count}, Video Count: {video_count}")

        # Get the most recent videos
        recent_videos = get_recent_videos(channel_id)
        for video in recent_videos:
            stats = get_video_statistics(video['video_id'])
            print(f"Video Title: {stats['title']}, Date Posted: {stats['date_posted']}, Comments: {stats['comment_count']}, Likes: {stats['like_count']}")

            # Get recommended videos and their channels
            recommended_videos = get_recommended_videos(f"https://www.youtube.com/watch?v={video['video_id']}")
            for rec_video_url in recommended_videos:
                rec_channel_id = get_channel_from_video(rec_video_url)
                if rec_channel_id is None:
                    continue
                
                rec_subscriber_count = get_subscriber_count(rec_channel_id)
                
                if rec_subscriber_count >= 10000:
                    process_channel(rec_channel_id, depth + 1)
                else:
                    print(f"Skipping Recommended Channel ID {rec_channel_id}: Less than 10,000 subscribers.")

    # Process each starting channel
    for channel_url in starting_channels:
        channel_id = get_channel_id(channel_url)
        process_channel(channel_id, 1)

# Example usage with one starting channel and specified depth
starting_channels = [
    'https://www.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA'
]

if __name__ == "__main__":
    max_depth = 1  # Change this value to control the depth
    main(starting_channels, max_depth)
