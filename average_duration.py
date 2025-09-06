import os
import requests
import isodate  # For parsing ISO 8601 durations

# Function to read video IDs from a text file
def read_video_ids(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Function to get the duration of each video in seconds
def get_video_durations(video_ids):
    api_key = os.getenv('YOUTUBE_API_KEY')
    durations_in_seconds = []
    
    # YouTube API endpoint
    base_url = "https://www.googleapis.com/youtube/v3/videos"
    
    # Process video IDs in chunks of 50 (API limit per request)
    for i in range(0, len(video_ids), 50):
        # Get a batch of 50 video IDs
        video_id_batch = video_ids[i:i+50]
        video_id_str = ','.join(video_id_batch)
        
        # Make API request
        params = {
            'part': 'contentDetails',
            'id': video_id_str,
            'key': api_key
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        # Parse durations and convert them to seconds
        for item in data.get('items', []):
            duration_str = item['contentDetails']['duration']
            duration = isodate.parse_duration(duration_str)
            duration_in_seconds = duration.total_seconds()
            durations_in_seconds.append(duration_in_seconds)
    
    return durations_in_seconds

# Function to calculate the average duration
def calculate_average_duration(durations):
    if not durations:
        return 0
    return sum(durations) / len(durations)

# Main function
def main(file_path):
    # Read video IDs from file
    video_ids = read_video_ids(file_path)
    
    # Get video durations in seconds
    durations = get_video_durations(video_ids)
    
    # Calculate the average duration
    avg_duration = calculate_average_duration(durations)
    
    print(f"Average Duration: {avg_duration} seconds")

# Path to the text file with video IDs
file_path = 'all-vids.txt'

# Run the main function
main(file_path)
