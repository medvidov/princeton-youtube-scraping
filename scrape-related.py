from playwright.sync_api import sync_playwright

def get_related_videos(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the YouTube video page
        page.goto(url)

        # Wait for the video player to load
        page.wait_for_selector('.html5-video-player')

        # Seek to the end of the video (last 5 seconds)
        page.evaluate("""
            document.querySelector('video').currentTime = document.querySelector('video').duration - 5;
        """)

        # Wait for the related videos overlay to load with a longer timeout
        page.wait_for_selector('a.ytp-ce-covering-overlay', timeout=60000)

        # Extract titles and links of related videos
        related_videos = page.eval_on_selector_all(
            'a.ytp-ce-covering-overlay',
            """
            elements => elements.map(e => ({
                title: e.querySelector('div.ytp-ce-video-title').textContent.trim(),
                url: e.href
            }))
            """
        )

        if not related_videos:
            print("No related videos found with the current selector.")
        else:
            for video in related_videos:
                print(f"Title: {video['title']}\nURL: {video['url']}\n")

        browser.close()

# Example usage
video_url = 'https://www.youtube.com/watch?v=yqenbeFkQBE'
get_related_videos(video_url)
