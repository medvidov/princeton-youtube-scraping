# princeton-youtube-scraping
This codebase was created while I was at Princeton University to experiment with scraping YouTube (or querying the API) for research. Much of the code is unstructured due to the random requests I received. This work required A LOT of stakeholder interaction and requirements gathering. In general I was trying to figure out three things:

## 1. Prefix Nesting
YouTube video IDs are generated as 11 character strings. Previous research has shown that prefix search (ie. searching for "abc-" yields videos that start with "abc"). Prefix nesting is the idea that searching "abc-" should also yield videos that start with "abcd" and "abcde" but the opposite should not be true a la "all squares are rectangles, but not all rectangles are squares". All "abcd"s are "abc"s, but not all "abc"s are "abcd"s. Eventually I concluded that prefixes nested, but due to constraints with YouTube's API and the number of searches it could return, it was impossible to draw meaningful results from that nesting.

## 2. Snowball Sampling
Internet content engagement generally follows a power law; the top creators get the most engagement and then it just reduces until something like 50% of internet content has 0 engagement. I attempted to scrape related and recommended videos to be able to conduct this sampling but ultimately YouTube's anti-scraping measures made it nigh impossible.

## 3. General Data Collection
Best represented by my [lovely graphs](/visualizations), I analyzed a sample of the data I queried to get a general idea of video demographics.