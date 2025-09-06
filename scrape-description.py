
import re
from bs4 import BeautifulSoup
import requests

soup = BeautifulSoup(requests.get('https://www.youtube.com/watch?v=yqenbeFkQBE').content)
pattern = re.compile('(?<=shortDescription":").*(?=","isCrawlable)')
description = pattern.findall(str(soup))[0].replace('\\n','\n')
print(description)