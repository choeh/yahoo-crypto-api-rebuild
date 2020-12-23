from autoscraper import AutoScraper
import requests

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

# Build scraper
result = scraper.build(url, wanted_dict=wanted_dict)

# Set rule aliases
scraper.keep_rules(['rule_5e8i', 'rule_q71n', 'rule_hpoe', 'rule_vb9o', 'rule_oaed'])
scraper.set_rule_aliases({'rule_5e8i': 'Symbol', 'rule_q71n': 'Name', 'rule_hpoe': 'Price', 'rule_vb9o': 'Logo', 'rule_oaed': 'MarketCap'})

# Store scraper in file
scraper.save('yahoo_crypto')
