# Mapping *Crypto Screener* to a *Scraper Api*
The [*Cryptocurreny Screener*](https://finance.yahoo.com/cryptocurrencies/) from `Yahoo.com` is showing dynamically updated `pricing`, `volume`, `market capitalization`, etc. data for about **370 Cryptocurrencies**. Without having an api, the screener is generally limited to manual usage.

To reengineer an api for individually serving *screened data*, a simple implementation of the top-notch `Python` libraries [AutoScraper](https://github.com/alirezamika/autoscraper) & [FastAPI](https://github.com/tiangolo/fastapi) is implemented.

Inspiration originated from this [`Medium.com` article](https://medium.com/better-programming/autoscraper-and-flask-create-an-api-from-any-website-in-less-than-5-minutes-3f0f176fc4a3).

## Setup
Download or git clone this repository. Unzip the downloaded file. Open up your terminal. Change to the local copy folder of the repository. And run:
```shell
pip install -r requirements.txt
```

If [Docker](https://www.docker.com) is installed on your computer, the application can be *containerized*. To build the *Docker* image, run in your local folder:
```shell
docker build -t yahoo-crypto-api .
```
To start a *Docker* container, run:
```shell
docker run --name scraper-api yahoo-crypto-api
```

## Usage
To start the `Yahoo Cryptocurrency` *Scraper* run:
```python
python scraper.py
```
If you do so, be aware that the `wanted_dict` entries in `scraper.py` have to be updated *directly before* running the scraper.

It is best to load the existing, pretrained *Scraper*, stored in the `yahoo_crypto` file.

To start the `FastAPI` *Server* run:
```python
python api.py
```

To check if the server is running, checkout the *Api Documentation* at `http://localhost:8080/docs` in your browser.

To retrieve the current `Yahoo Cryptocurrency` data, call the `http://localhost:8080/cryptos` api endpoint via your [Postman](https://www.postman.com) or [Insomnia](https://insomnia.rest) application or use your browser.
