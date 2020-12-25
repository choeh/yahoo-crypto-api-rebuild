from autoscraper import AutoScraper
import requests
from fake_useragent import UserAgent
from fp.fp import FreeProxy
from copy import copy

# Same rule ids for each run
import random
random.seed(42)


def initialize_request_args(url: str = ''):
  # Initialize randomized user-agent and proxy
  useragent = UserAgent(cache=False, use_cache_server=False)
  proxy = FreeProxy(country_id=['US', 'GB', 'DE'], timeout=1, anonym=True, rand=True)
  headers = {
      'User-Agent': useragent.firefox,
      'Proxies': proxy.get()
  }
  scraper_template.request_headers.update(headers)

  # Initialize cookie
  session = requests.session()
  session.get(url, headers=scraper_template.request_headers)
  return dict(
    cookies = session.cookies.get_dict(),
    headers = headers
  )


def build_scraper(wanted: dict = {}, model_name: str = 'yahoo_crypto'):
  # Build scrapers
  scraper = copy(scraper_template)
  scraper.build(url, wanted_dict=wanted, request_args=initialize_request_args(url))
  
  # Display rules and get user input on which rules to keep and rule aliases
  result = scraper.get_result_exact(url, grouped=True)
  print([(key, value[0]) for key, value in result.items()])
  rules_to_keep = [rule_id.strip() for rule_id in input('Enter rules to keep (comma separated): ').split(',')]
  rule_aliases = {rule_id: alias.strip().title() for rule_id, alias in zip(rules_to_keep, input('Enter rule alias given rules (comma separated: ').split(','))}

  # Set used rules and rule aliases 
  scraper.keep_rules(rules_to_keep)
  scraper.set_rule_aliases(rule_aliases)

  # Store scraper in file
  scraper.save(model_name)


# Initialize autoscraper
scraper_template = AutoScraper()

# Screener url
domain = 'https://finance.yahoo.com'
uri = '/cryptocurrencies/'

url = f'{domain}{uri}'

# Yahoo Crypto Scraper
wanted = dict(
    symbol=['BTC-USD'],
    name=['Bitcoin USD'],
    price=['23,620.90'],
    logo=['https://s.yimg.com/uc/fin/img/reports-thumbnails/1.png'],
    marketcap=['438.857B']
)
build_scraper(wanted=wanted, model_name='yahoo_crypto_2')
