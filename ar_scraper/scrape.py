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


def search_all(html, word):
    lines = html.text.split('\n')
    for line in lines:
        for word_ in line.split(' '):
            if word_.lower() == word.lower():
                return word


def search_top_click_links_pages_for_tickers(words, debug=True):
    main_links = get_mainpage_links()
    top_clicks_link = find_top_clicks_link(main_links)
    links_to_search_for_tickers = get_top_clicks_links_to_search(top_clicks_link)

    found = []

    for idx, link in enumerate(links_to_search_for_tickers):
        response = fetch_html(url=link)
        print(idx, 'scraping:',  link)

        with tqdm(total=len(words)) as pbar:

            for word in words:
                # print('.', end='', flush=True)
                result = search_all(response.html, word)
                if result:
                    found.append(word)
                pbar.update(1)
            else:
                print()

            words = [word for word in words if word not in found]

            if debug:
                break
    return found
