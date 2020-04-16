from flask import Flask
from flask_restful import Resource, Api
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
api = Api(app)

class Crypto(Resource):
    def get(self):
        url = 'https://coinmarketcap.com/'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        results = []

        resultsRow = soup.find_all('tr', {'class' : 'cmc-table-row'})

        for resultRow in resultsRow:
            rank = resultRow.find('div', {'class', ''}).text
            currency = resultRow.find('a', {'class', 'cmc-link'}).text
            market_cap = resultRow.find('td', {'class', 'cmc-table__cell--sort-by__market-cap'}).text
            price = resultRow.find('td', {'class', 'cmc-table__cell--sort-by__price'}).text
            volume = resultRow.find('td', {'class', 'cmc-table__cell--sort-by__volume-24-h'}).text
            circulating_supply = resultRow.find('td', {'class', 'cmc-table__cell--sort-by__circulating-supply'}).text.replace('*', '')
            change = resultRow.find('td', {'class', 'cmc-table__cell--sort-by__percent-change-24-h'}).text

            results.append({
                'currency': currency,
                'rank': rank,
                'market_cap': market_cap,
                'price': price,
                'volume': volume,
                'circulating_supply': circulating_supply,
                'change': change
            })
        return results
api.add_resource(Crypto, '/crypto')

if __name__ == "__main__":
    app.run(debug=True)