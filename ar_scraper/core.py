from .scrape import get_mainpage_links, find_top_clicks_link, get_top_clicks_links_to_search, fetch_html
from .tickers import TickerSearch
from .tools import clean, remove_punctuation
from tqdm import tqdm


def clean_and_parse(text):
    parsed = []
    lines = text.split('\n')
    for line in lines:
        for word in line.split(' '):
            cleaned = clean(word.replace(' ', ''))
            if len(cleaned) > 0:
                parsed += cleaned
    parsed = list(set(parsed))
    parsed.sort()
    return parsed


def search_top_click_links_pages_for_tickers(debug=True):
    main_links = get_mainpage_links()
    top_clicks_link = find_top_clicks_link(main_links)
    links_to_search_for_tickers = get_top_clicks_links_to_search(top_clicks_link)

    found = []
    tickers = []

    TS = TickerSearch()
    search_words = TS.all_strings

    for idx, link in enumerate(links_to_search_for_tickers):
        response = fetch_html(url=link)
        cleaned = clean_and_parse(response.html.text)
        print(idx, 'scraping:',  link)

        with tqdm(total=len(cleaned)) as pbar:
            for c in cleaned:
                try:
                    ticker = TS[c]['symbol']
                    tickers.append(ticker)
                except KeyError:
                    pass
                finally:
                    pbar.update(1)

        print(len(tickers))
        break
    print(tickers)


def run():
    # TS = TickerSearch()
    # search_words = TS.all_strings
    found = search_top_click_links_pages_for_tickers()
    # for word in found:
    # print(word)
    # print(TS[word])
