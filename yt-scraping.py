import json
import urllib.request
import string
import random
import ssl
from dotenv import load_dotenv
import os

# Number of videos to fetch in total
total_videos = 500
# Number of videos to fetch per API request (maximum is 50)
max_results_per_request = 50

# Your API key here
API_KEY = os.getenv('YOUTUBE_API_KEY')

# File to store video IDs
output_file = "videos.txt"

# Initialize a counter for total videos fetched
videos_fetched = 0

# Create an SSL context to bypass SSL verification
context = ssl._create_unverified_context()

# Function to generate a random query
def generate_random_query():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

try:
    # Open the file in append mode
    with open(output_file, "a") as f:
        while videos_fetched < total_videos:
            # Generate a new random query string
            random_query = generate_random_query()

            # Construct the initial API URL
            urlData = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&maxResults={max_results_per_request}&part=snippet&type=video&q={random_query}"

            while videos_fetched < total_videos:
                # Open the URL with SSL context
                webURL = urllib.request.urlopen(urlData, context=context)

                # Read the response
                data = webURL.read()
                # Get the encoding format
                encoding = webURL.info().get_content_charset('utf-8')
                # Parse JSON data
                results = json.loads(data.decode(encoding))

                # Iterate over the items in the result
                for data in results.get('items', []):
                    videoId = data['id'].get('videoId')
                    if videoId:
                        f.write(videoId + '\n')
                        videos_fetched += 1

                        # Stop if we have fetched the required number of videos
                        if videos_fetched >= total_videos:
                            break

                # Get the nextPageToken to fetch more results
                next_page_token = results.get('nextPageToken')

                if not next_page_token:
                    # Break the loop if there are no more pages to fetch for this query
                    break

                # Construct the URL for the next page
                urlData = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&maxResults={max_results_per_request}&part=snippet&type=video&q={random_query}&pageToken={next_page_token}"
                
                # Stop if we have fetched the required number of videos
                if videos_fetched >= total_videos:
                    break

except urllib.error.URLError as e:
    print(f"Failed to fetch data: {e.reason}")
except Exception as e:
    print(f"An error occurred: {e}")

