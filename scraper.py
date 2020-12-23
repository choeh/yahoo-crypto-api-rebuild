from autoscraper import AutoScraper
import requests
from fake_useragent import UserAgent
from fp.fp import FreeProxy

# Same rule ids for each run
import random
random.seed(42)


# Initialize autoscraper
scraper = AutoScraper()

# Wanted entries (values to be updated directly before usage)
wanted_dict = dict(
    symbol=['BTC-USD'],
    name=['Bitcoin USD'],
    price=['23,620.90'],
    logo=['https://s.yimg.com/uc/fin/img/reports-thumbnails/1.png'],
    marketcap=['438.857B']
)

# Screener url
domain = 'https://finance.yahoo.com'
uri = '/cryptocurrencies/'

url = f'{domain}{uri}'

# Request headers
useragent = UserAgent(cache=False, use_cache_server=False)
proxy = FreeProxy(country_id=['US', 'GB', 'DE'], timeout=1, anonym=True, rand=True)

scraper.request_headers.update({
  'User-Agent': useragent.firefox,
  'Proxies': proxy.get()
})

session = requests.session()
session.get(url, headers=scraper.request_headers)
cookies = session.cookies.get_dict()

# Build scraper
result = scraper.build(url, wanted_dict=wanted_dict, request_args=dict(cookies=cookies))

# Set rule aliases
scraper.keep_rules(['rule_5e8i', 'rule_q71n', 'rule_hpoe', 'rule_vb9o', 'rule_oaed'])
scraper.set_rule_aliases({'rule_5e8i': 'Symbol', 'rule_q71n': 'Name', 'rule_hpoe': 'Price', 'rule_vb9o': 'Logo', 'rule_oaed': 'MarketCap'})

# Store scraper in file
scraper.save('yahoo_crypto')
