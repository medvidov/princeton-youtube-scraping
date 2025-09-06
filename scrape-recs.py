# from playwright.sync_api import sync_playwright

# with sync_playwright() as p:
#     # Launch the browser in headless mode
#     browser = p.chromium.launch(headless=True)
#     page = browser.new_page()

#     # Navigate to the YouTube video page
#     video_url = 'https://www.youtube.com/watch?v=yqenbeFkQBE'
#     page.goto(video_url)

#     # Wait for the sidebar to load
#     page.wait_for_selector('a#thumbnail')

#     # Extract all recommendation links
#     recommendation_links = page.eval_on_selector_all('a#thumbnail', "elements => elements.map(e => e.href)")

#     # Print the recommendation links
#     for link in recommendation_links:
#         print(link)

#     # Close the browser
#     browser.close()

import urllib.request
from bs4 import BeautifulSoup


goto = "https://www.youtube.com/watch?v=yqenbeFkQBE"
body = urllib.request.urlopen(goto)
soup = BeautifulSoup(body, features='html.parser', from_encoding=body.info().get_param('charset'))
recommended_urls =[]
for link in soup.find_all('a', href=True):
    if "/watch?" in link['href']:
        recommended_urls.append(link['href'])
list(set(recommended_urls))

print(recommended_urls)
