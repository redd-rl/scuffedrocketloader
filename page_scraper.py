from pprint import pprint
from typing import Union
from bs4 import BeautifulSoup
import bs4
import requests
import time
def scrapePage(depth_limit=None):
    modifiableUrl = "https://lethamyr.com"
    base_url = "https://lethamyr.com/mymaps"
    new_page = base_url
    maps = []
    count = 0
    while True:
        if count == depth_limit:
            break
        page = requests.get(new_page)
        print(page)
        while page.status_code != 200:
                page = requests.get(new_page)
                print("encountered timeout!")
                time.sleep(2)
        with open("page.html", "wb") as handle:
            handle.write(page.content)
        soup = BeautifulSoup(page.text, "html.parser")
        older_button = soup.find("div", class_="older")
        pageMaps = soup.find_all("article", class_="blog-basic-grid--container entry blog-item")
        for rlmap in pageMaps:
            rlmap: Union[bs4.Tag, bs4.NavigableString]
            
            string = rlmap.find('a', class_="image-wrapper").get('href')
            DownloadPage = requests.get(modifiableUrl + string)
            print(DownloadPage)
            while DownloadPage.status_code != 200:
                DownloadPage = requests.get(modifiableUrl + string)
                print("encountered timeout!")
                time.sleep(2)
            soupp = BeautifulSoup(DownloadPage.text, "html.parser")
            try:
                downloadLink = soupp.find('a', class_="sqs-block-button-element--large sqs-button-element--secondary sqs-block-button-element").get('href')
            except:
                downloadLink = soupp.find('a',class_='sqs-block-button-element--medium sqs-button-element--primary sqs-block-button-element').get('href')
            downloadLink = downloadLink.split('/')
            reformattedLink = f"https://drive.google.com/u/0/uc?id={downloadLink[5]}&export=download"
            activeMap = {
                "name": rlmap.find('h1', class_='blog-title').find('a').text.strip(),
                "identifier": string.replace("/mymaps/",""),
                "desc": rlmap.find('div', class_='blog-excerpt').find('p').text,
                "img": rlmap.find('div').find('img', class_='image').get('data-src'),
                "download-url": reformattedLink
            }
            maps.append(activeMap)
            time.sleep(1/5)
        if older_button == None:
            print("could not find an older button, breaking out of loop.")
            break
        try:
            href = older_button.find("a").get('href')
        except AttributeError:
            print("found no button, breaking!")
            break
        except:
            print("unknown error occured")
            break
        new_page = f"{modifiableUrl}{href}"
        time.sleep(1.5)
        count +=1
    return maps