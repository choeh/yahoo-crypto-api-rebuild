from autoscraper import AutoScraper
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from scraper import init_request_args


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

url = f'{domain}{uri}'

scraper = AutoScraper()
request_args = init_request_args(url=url)


def get_yahoo_crypto_data():
    # Load stored scraper
    scraper.load('yahoo_crypto_data.json')

    # Scrape table entries from all subpages
    data = pd.DataFrame([], columns=['Symbol', 'Name', 'Logo', 'Price', 'Change_Relative', 'Marketcap', 'Volume_24H', 'Supply_Circulating'])
    n_page = 0
    rows_per_page = 100
    while data.shape[0] % rows_per_page == 0 and n_page < 10:
        url_paged_query = f'{url}?offset={n_page*rows_per_page}&count={rows_per_page}'
        try:
            ret = scraper.get_result_similar(url_paged_query, group_by_alias=True, keep_order=True, request_args=request_args)
            ret['Logo'] = ret['Logo'] + [''] * (len(ret['Symbol']) - len(ret['Logo']))  # TODO: temp handling of none in logo
            data = pd.concat([data, pd.DataFrame(ret)], ignore_index=True)
            n_page += 1
        except:
            break
    return data


def get_yahoo_crypto_news():
    # Load stored scraper
    scraper.load('yahoo_crypto_news.json')

    # Scrape news from page
    ret = scraper.get_result_similar(url, group_by_alias=True, keep_order=True, request_args=request_args)
    data = pd.DataFrame(ret, columns=['News', 'Urls'])
    return data


@app.get('/cryptos')
def crypto_data_api():
    # Api endpoint for retrieving yahoo crypto data
    data = get_yahoo_crypto_data()
    return data.to_dict()


@app.get('/cryptonews')
def crypto_news_api():
    # Api endpoint for retrieving yahoo crypto news
    data = get_yahoo_crypto_news()
    return data.to_dict()


if __name__ == "__main__":
    uvicorn.run('api:app', host="0.0.0.0", port=8080, reload=True)
