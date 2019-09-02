import requests
import lxml.html
from typing import Iterator


def main():
    session = requests.Session()
    response = requests.get("https://gihyo.jp/dp")
    urls = scrape_list_page(response)
    for url in urls:
        response = session.get(url)
        ebook = scrape_detail_page(response)
        print(ebook)
        break
def scrape_list_page(response:requests.Response) -> Iterator[str]:

    html = lxml.html.fromstring(response.text)
    html.make_links_absolute(response.url)
    for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
        url = a.get('href')
        yield url


def scrape_detail_page(response:requests.Response) -> dict:
    html = lxml.html.fromstring(response.text)
    ebook = {
     'url':response.url,
     'title':html.cssselect('#bookTitle')[0].text_content(),
     'price':html.cssselect('.buy')[0].text.strip(),
     'content':[h3.text_content() for h3 in html.cssselect('#content > h3')]
    }
    return ebook

if __name__ == '__main__':
    main()
