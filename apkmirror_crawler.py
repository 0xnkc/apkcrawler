import cfscrape
import requests
import os
from bs4 import BeautifulSoup


#Download
def download(url, file_name):
    file_name = file_name[:15]+".apk"
    os.system('wget --user-agent="Mozilla" -O {0} {1}'.format(file_name, url))


#Home Url
base_url = "https://www.apkmirror.com"
#Config
session = requests.session()
session.headers = 'content-type'
session.mount("http://", cfscrape.CloudflareScraper())
scraper = cfscrape.create_scraper(sess=session)
req = scraper.get(base_url).content

#BeautifulSoup define
soup = BeautifulSoup(req,'lxml')
home_link = soup.find_all("a", {"class": "downloadLink"})
home_link = home_link[2:]

for link in home_link:
    app_links = link['href']
#     print(app_links)
# print(len(app_links))

req = scraper.get(base_url+app_links).content
soup = BeautifulSoup(req, 'lxml')
div = soup.find_all("div", {"class": "table-row headerFont"})
# print(div)
for tag in div:
    app_link_2 = tag.find_all("a")
    # print(app_link_2)
for link in app_link_2:
    download_link = link['href']
download_link = download_link[1:]
# print(base_url+"/"+download_link+"download")
req = scraper.get(base_url+"/"+download_link+"download").content
soup = BeautifulSoup(req, 'lxml')
newlink = soup.find_all("a", {"rel": "nofollow"})
u = "https://www.apkmirror.com"+newlink[1]['href']
title = str(soup.title.text+".apk").replace(' ', '-').replace('/', '')
# print(u+"\n"+title)
download(u, title)
