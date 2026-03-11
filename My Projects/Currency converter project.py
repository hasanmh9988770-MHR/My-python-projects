import warnings
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL")
import requests

class CurrencyConverter:
    rates = {}

    def __init__(self, url):
        data = requests.get(url).json()
        if data.get("success") == False:
            print("Error fetching data:", data.get("error"))
            return
        self.rates = data["rates"]

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        if from_currency != 'EUR':
            amount = amount / self.rates[from_currency]


        amount = round(amount * self.rates[to_currency], 2)
        print(f'{initial_amount} {from_currency} = {amount} {to_currency}')

if __name__ == "__main__":
    YOUR_ACCESS_KEY = "e79c7b79d3afe3823f10fad71a0f8855"
    url = f'http://data.fixer.io/api/latest?access_key={YOUR_ACCESS_KEY}'

    converter = CurrencyConverter(url)

    if converter.rates:  # Check if rates loaded successfully
        amount = float(input("Amount: "))
        from_currency = input("From Currency (e.g., USD): ").upper()
        to_currency = input("To Currency (e.g., EUR): ").upper()
        converter.convert(from_currency, to_currency, amount)