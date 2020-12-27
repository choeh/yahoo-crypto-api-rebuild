from autoscraper import AutoScraper
import requests
from fake_useragent import UserAgent
from fp.fp import FreeProxy

# Same rule ids for each run
import random
random.seed(42)


def init_request_args(headers, url: str = '', randomize: bool = True, cookies: bool = True):
    args = {}
    if randomize:
        # Get randomized user-agent
        useragent = UserAgent(cache=False, use_cache_server=False)
        args['headers'] = {'User-Agent': useragent.random}
        # Get randomized proxy
        proxy = FreeProxy(country_id=['US', 'GB', 'DE'], timeout=1, anonym=True, rand=True)
        proxy = proxy.get()
        if 'There are no working proxies' not in proxy:
            args['headers']['Proxies'] = proxy

    if cookies:
        # Initialize cookie
        session = requests.session()
        session.get(url, headers=headers)
        args['cookies'] = session.cookies.get_dict()
    return args


def build_scraper(wanted: dict = {}, model_name: str = None, auto_ruling: bool = True, **request_args):
    # Build scrapers
    scraper = AutoScraper()
    request_args = init_request_args(headers=scraper.request_headers, url=url, **request_args)
    scraper.build(url, wanted_dict=wanted, request_args=request_args)

    if auto_ruling:
        # Retrieve unique rules and rule aliases computationally
        result = scraper.get_result_exact(url, grouped=True)
        unique_rules = {val[0]: key for key, val in result.items()}
        rules_matching_wanted = {alias: rule_id for rule_value, rule_id in unique_rules.items() for alias, wanted_values in wanted.items() if rule_value in wanted_values}

        # Set used rules
        rules_to_keep = list(rules_matching_wanted.values())
        scraper.keep_rules(rules_to_keep)

        # Set used rule aliases
        rule_aliases = {rule_id: alias.title() for alias, rule_id in rules_matching_wanted.items()}
        scraper.set_rule_aliases(rule_aliases)

    if model_name:
        # Store scraper in file
        scraper.save(model_name)


# Screener url
domain = 'https://finance.yahoo.com'
uri = '/cryptocurrencies/'

url = f'{domain}{uri}'

# Yahoo Crypto Data Scraper
data_wanted = dict(
    symbol=['BTC-USD'],
    name=['Bitcoin USD'],
    price=['23,620.90'],
    logo=['https://s.yimg.com/uc/fin/img/reports-thumbnails/1.png'],
    marketcap=['438.857B']
)
build_scraper(wanted=data_wanted, model_name='yahoo_crypto_data')

# Yahoo Crypto News Scraper
news_wanted = dict(
    news=['Bitcoin Tops $24.6K on Christmas Day, Sets New All-Time High',
          'Can Bitcoin Hit $100,000 in 2021? Regulators and the Bulls may have to Battle it out!', 'The Crypto Daily – Movers and Shakers – December 25th, 2020'],
    urls=['https://finance.yahoo.com/news/bitcoin-sets-time-high-24-125722098.html', 'https://finance.yahoo.com/news/bitcoin-hit-100-000-2021-051215840.html',
          'https://finance.yahoo.com/news/crypto-daily-movers-shakers-december-010607662.html']
)
build_scraper(wanted=news_wanted, model_name='yahoo_crypto_news')
