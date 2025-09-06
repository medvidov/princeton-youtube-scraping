import os
import random
import string
import requests
import json

# Set up the YouTube Data API key
API_KEY = os.getenv('YOUTUBE_API_KEY')

# Function to generate a base 3-character prefix and derive 4- and 5-character prefixes
# Ex. abc, abcd, adcde
def generate_prefixes(k=4):
    watch_prefix = 'watch?v='
    base_prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=k))
    prefix_5 = base_prefix + random.choice(string.ascii_lowercase + string.digits)
    prefix_6 = prefix_5 + random.choice(string.ascii_lowercase + string.digits)
    return watch_prefix+base_prefix, watch_prefix+prefix_5, watch_prefix+prefix_6

# Returns the number of results that populate in YouTube search for a given prefix
# This is an important sanity check. In theory, a prefix of length 3 should return more results than the corresponding prefix of length 4, and so on.
# Additionally, the results for a prefix of length 3 should include all results for the corresponding prefix of length 4, and so on. (Searching abc would also get me abcd because abcd contains abc)
def get_num_results(prefix):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={prefix}&type=video&maxResults=50&key={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve search results: {response.status_code}")
        return 0
    data = response.json()
    return data["pageInfo"]["totalResults"]

# Function to perform a search on YouTube using a prefix
# This is an important sanity check. In theory, a prefix of length 3 should return more results than the corresponding prefix of length 4, and so on.
# Additionally, the results for a prefix of length 3 should include all results for the corresponding prefix of length 4, and so on. (Searching abc would also get me abcd because abcd contains abc)
def search_youtube(prefix):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={prefix}&type=video&maxResults=50&key={API_KEY}"
    results = []

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve search results: {response.status_code}")
        return results
    data = response.json()

    # Save data results to file
    with open(f'{prefix}.json', 'w') as f:
        f.write(json.dumps(data, indent=4))
    
    total_results = data["pageInfo"]["totalResults"]
    print(f"Total results for prefix: {prefix} - {total_results}")
    while url:
        
        # results.extend(data.get('items', []))
        video_ids = [i["id"]["videoId"] for i in data.get('items', [])]
        results.extend(video_ids)
        
        # Check if we've hit the 1,000 result limit
        # if len(results) >= 1000:
        #     print(f"Hit the 1,000 result limit for prefix: {prefix}")
        #     break
        
        # Get the next page token if more results are available
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={prefix}&type=video&maxResults=50&pageToken={data.get('nextPageToken', '')}&key={API_KEY}" if 'nextPageToken' in data else None

    # Save data to file
    with open(f'{prefix}.txt', 'w') as f:
        for item in results:
            f.write(str(item)+'\n')

    return results

# Function to check proportion of X+1 digit subset that appears in the X digit superset
def calculate_proportion(broader_sample: list, specific_sample: list):
    broader_ids = set(broader_sample)
    specific_ids = set(specific_sample)
    intersection_count = len(specific_ids.intersection(broader_ids))
    return intersection_count / len(specific_ids) if specific_ids else 0

# Main function to perform random prefix sampling and analysis
def random_prefix_sampling_analysis():
    k_counts = []
    k_plus1_counts = []
    k_plus2_counts = []

    for _ in range(500):  # Generate 10 sets of prefixes
        prefix_k, prefix_kplus1, prefix_kplus2 = generate_prefixes()
        print(prefix_k)
        k_counts.append(get_num_results(prefix_k))
        k_plus1_counts.append(get_num_results(prefix_kplus1))
        k_plus2_counts.append(get_num_results(prefix_kplus2))


        # print(f"\nAnalyzing prefixes: {prefix_3}, {prefix_4}, {prefix_5}")
        
        # # Search with 3-character prefix
        # sample_3 = search_youtube(prefix_3)
        # print(f"Searching with 3-character prefix: {prefix_3} - Total Results: {len(sample_3)}")
        
        # # Search with 4-character prefix
        # sample_4 = search_youtube(prefix_4)
        # print(f"Searching with 4-character prefix: {prefix_4} - Total Results: {len(sample_4)}")
        # proportion_4_in_3 = calculate_proportion(sample_3, sample_4)
        # print(f"Proportion of 4-character sample in 3-character sample: {proportion_4_in_3:.2%}")
        
        # # Search with 5-character prefix
        # sample_5 = search_youtube(prefix_5)
        # print(f"Searching with 5-character prefix: {prefix_5} - Total Results: {len(sample_5)}")
        # proportion_5_in_4 = calculate_proportion(sample_4, sample_5)
        # print(f"Proportion of 5-character sample in 4-character sample: {proportion_5_in_4:.2%}")

    # Get % of samples that hit 1,000,000 results
    k_million = sum([1 for c in k_counts if (c <= 50 and c >= 38)]) / len(k_counts)
    k_plus1_million = sum([1 for c in k_plus1_counts if (c <= 50 and c >= 38)]) / len(k_plus1_counts)
    k_plus2_million = sum([1 for c in k_plus2_counts if (c <= 50 and c >= 38)]) / len(k_plus2_counts)

    print(f"Proportion of samples with about 1 page of (38-50) results: 4 - {k_million:.2%}, 5 - {k_plus1_million:.2%}, 6 - {k_plus2_million:.2%}")

    # Plot k_counts, k_plus1_counts, k_plus2_counts
    import matplotlib.pyplot as plt
    plt.hist(k_counts, bins=10, alpha=0.5, label='4')
    plt.hist(k_plus1_counts, bins=10, alpha=0.5, label='5')
    plt.hist(k_plus2_counts, bins=10, alpha=0.5, label='6')
    plt.legend(loc='upper right')
    plt.savefig('prefix-sampling.png')
    plt.show()

# Run the analysis
random_prefix_sampling_analysis()
