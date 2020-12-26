from autoscraper import AutoScraper
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fake_useragent import UserAgent
from fp.fp import FreeProxy


# Initialize backend server
app = FastAPI(
    title='FastAPI Backend',
    description='Backend for data serving and filtering',
    version='0.1.0',
    docs_url='/docs',
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

# Screener url
domain = 'https://finance.yahoo.com'
uri = '/cryptocurrencies/'

# Load stored scraper
scraper = AutoScraper()
scraper.load('yahoo_crypto')

# Request headers
useragent = UserAgent(cache=False, use_cache_server=False, verify_ssl=False)
proxy = FreeProxy(country_id=['US', 'GB', 'DE'], timeout=1, anonym=True, rand=True)

scraper.request_headers.update({
    'User-Agent': useragent.firefox,
    'Proxies': proxy.get()
})


def get_yahoo_crypto_data():
    # Scrape entries from all subpages
    data = pd.DataFrame([], columns=['Symbol', 'Name', 'Price', 'Logo', 'MarketCap'])
    n_page = 0
    rows_per_page = 100
    while data.shape[0] % rows_per_page == 0 and n_page < 10:
        url = f'{domain}{uri}?offset={n_page*rows_per_page}&count={rows_per_page}'
        try:
            ret = scraper.get_result_similar(url, group_by_alias=True, keep_order=True)
            ret['Logo'] = ret['Logo'] + [''] * (len(ret['Symbol']) - len(ret['Logo']))  # TODO: temp handling of none in logo
            data = pd.concat([data, pd.DataFrame(ret)], ignore_index=True)
            n_page += 1
        except:
            break
    return data


def get_yahoo_crypto_news():
    # Scrape news from page
    url = f'{domain}{uri}'
    ret = scraper.get_result_similar(url, group_by_alias=True, keep_order=True)
    data = pd.DataFrame(ret, columns=['News', 'Urls'])
    return data


@app.get('/cryptos')
def crypto_data_api():
    # Api endpoint for retrieving yahoo crypto data
    data = get_yahoo_crypto_data()
    return data.to_dict()


@app.get('/cryptonews')
def crypto_news_api():
    data = get_yahoo_crypto_news()
    return data.to_dict()


if __name__ == "__main__":
    uvicorn.run('api:app', host="0.0.0.0", port=8080, reload=True)
