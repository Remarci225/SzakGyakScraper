from bs4 import BeautifulSoup, SoupStrainer
from requests import Session
import cchardet
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

KEYWORDS = ["Java", "Python"]
formattedKeywords = [keyword.lower() for keyword in KEYWORDS]

results = {}
maxResultLength = 0

def scrape(anchor):
    global results
    global maxResultLength
    
    text = anchor.text.strip()
    href = anchor["href"].strip()
    
    subpage = session.get(href)
    subSoup = BeautifulSoup(subpage.text, "lxml")
    
    for keyword in formattedKeywords:
        for string in subSoup.stripped_strings:
            if keyword in string.lower():
                resultLength = len(text)
                if resultLength > maxResultLength:
                    maxResultLength = resultLength
                    
                if text in results:
                    results[text].append(keyword)
                else:
                    results[text] = [keyword]
                    
                break

print("\n[SzakGyakScraper]")

session = Session()
page = session.get("https://www.inf.elte.hu/bsc-kepzes/szakmai-gyakorlati-helyek?m=220")
soup = BeautifulSoup(page.text, "lxml", parse_only=SoupStrainer("div", attrs={"class": ["col-xs-12 subpage-description"]}))

anchors = soup.select("li a")
with ThreadPoolExecutor(cpu_count() * 2) as threadPoolExecutor:
    threadPoolExecutor.map(scrape, anchors)

print("\n")
sortedResults = sorted(list(results))
keywordCount = len(KEYWORDS)
for result in sortedResults:
    foundKeywords = results[result]
    print(f"{result: <{maxResultLength}} | [{len(foundKeywords)}/{keywordCount}] ({', '.join(foundKeywords)})")
print("\n")