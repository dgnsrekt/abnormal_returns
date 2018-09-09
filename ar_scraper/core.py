from .scrape import search_top_click_links_pages_for_tickers
from .tickers import TickerSearch


def run():
    TS = TickerSearch()
    search_words = TS.all_strings

    found = search_top_click_links_pages_for_tickers(search_words, debug=False)
    for word in found:
        print(TS[word])


if __name__ == '__main__':
    run()
