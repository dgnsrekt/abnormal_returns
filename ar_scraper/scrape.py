from .tools import get_year_and_month
from requests_html import HTMLSession
from tqdm import tqdm

year, month = get_year_and_month()

URL = f'https://abnormalreturns.com/{year}/{month:02d}/'


def fetch_html(url):
    session = HTMLSession()
    response = session.get(url=url)
    return response


def find_top_clicks_link(links):
    match = '/top-clicks-this-week-on-abnormal-returns-'
    for link in links:
        if match in link:
            return link


def filter_bad_links(links, bad_links):
    good_links = []
    for link in links:
        for b in bad_links:
            if b in link:
                break
        else:
            good_links.append(link)

    return list(set(good_links))


def get_mainpage_links():
    mainpage = fetch_html(URL)
    links = list(mainpage.html.links)
    return links


def get_top_clicks_links_to_search(links):
    response = fetch_html(links)
    html = response.html.find('div.links')[0]
    return filter_bad_links(html.links, ['http://getpocket.com/',
                                         'https://twitter.com/',
                                         'https://www.instapaper.com/',
                                         'https://stocktwits.com/',
                                         'http://stocktwits.com/'])
