import json
import os

import requests
from bs4 import BeautifulSoup

from constant import (END_DATE, START_DATE,
                      SYMBOLS_FILENAME)

from src.utils import normalize_date, normalize_price



# Stockbiz API
STOCKBIZ_API_URL = 'https://www.stockbiz.vn/Stocks/{symbol}/HistoricalQuotes.aspx'
PARAM_NAME = 'Cart_ctl00_webPartManager_wp1770166562_wp1427611561_callbackData_Callback_Param'
HEADERS = {
        'authority': 'www.stockbiz.vn',
        'accept': '*/*',
        'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://www.stockbiz.vn',
        'referer': 'https://www.stockbiz.vn/Stocks/DMC/HistoricalQuotes.aspx',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
}
COOKIES = {
        '.ASPXANONYMOUS': 'SUaW-HNN2QEkAAAAZDVhNjE2ZjYtODJhYS00NmY2LWJhOTQtNzdhOGNjZDBkZWRlrP2H1-fHuvCDbjm89r038eKosH41',
        'ASP.NET_SessionId': 'z0dh2245ygcoaea30lcghq2t',
        '__utmc': '161726307',
        '__utmz': '161726307.1671808905.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
        'ED_Popup': 'true',
        '__gads': 'ID=66656657a26781b5-22ab421e03d9004a:T=1671808849:RT=1671808849:S=ALNI_MY5p3g0-nHbWQDpqTVM0FfONgXqYA',
        '__gpi': 'UID=00000b966199a528:T=1671808849:RT=1671808849:S=ALNI_MZcuu78NNO3lAdJo6HBST6Iu-nACg',
        '__utma': '161726307.2081516909.1671808905.1671808905.1671811904.2',
        '__utmb': '161726307.1.10.1671811904',
}

def get_symbol_data(symbol):
    url = STOCKBIZ_API_URL.format(symbol=symbol)

    result_data = {}
    idx = 1

    # loop will run until data don't return any row data
    while True:
        # param của request
        data = {
            PARAM_NAME: [
                START_DATE,
                END_DATE,
                str(idx),
            ],
        }

        # collect data from api
        response = requests.post(url, headers=HEADERS, cookies=COOKIES, data=data)
        text = response.text

        # delete this character because BeautifulSoup is unreadable
        text = text.replace('<![CDATA[', '')
        text = text.replace(']]', '')

        # put to BeautifulSoup
        soup = BeautifulSoup(text, 'html.parser')

        # find table containing data
        table = soup.select('.dataTable')
        if not table:
            break
        table = table[0]

        # remove header
        rows = table.select('tr')
        rows = rows[1:]

        # if don't have any row data, break the loop
        if len(rows) == 0:
            break

        # add each row to result data
        for row in rows:
            # 0, 5 is number of date and closing price in table , strip for no extra character
            date = row.select('td')[0].text.strip()
            price_close = row.select('td')[5].text.strip()
            result_data[normalize_date(date)] = normalize_price(price_close)

        idx += 1

    return result_data



# Vcbs API
LIMIT = 100
VCBS_API_URL = 'https://quotes.vcbs.com.vn/f/parser/Stocks.js?v=20220911'

def get_stock_symbols():

    # if file is existed, get data from the file
    if os.path.isfile(SYMBOLS_FILENAME):
        f = open(SYMBOLS_FILENAME, encoding='utf8')
        json_data = f.read()
        symbols = json.loads(json_data)
        return symbols

    # get file script include symbols from https://quotes.vcbs.com.vn/a/exchange.html?symbol=HSX
    res = requests.get(VCBS_API_URL)
    text = res.text

    # find position of [ ] to get array of symbols json format
    start = text.find('[')
    end = text.find(']')
    json_data = text[start:end+1]

    # parse json to list in python
    list_data = json.loads(json_data)

    # get symbol fields from list_data, put in symbols
    symbols = []
    i = 0
    while len(symbols) < LIMIT:
        symbol = list_data[i]['SYMBOL']
        if 3 <= len(symbol) <= 5: 
            symbols.append(symbol)
        
        i += 1

    # write to the file when run, don't need to request again
    with open(SYMBOLS_FILENAME, 'w', encoding='utf8') as f:
        json.dump(symbols, f)

    return symbols
