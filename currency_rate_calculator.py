from requests import get
from pprint import PrettyPrinter

BASE_URL = "https://free.currconv.com/"
API_KEY =  "4bdbf00b660100a4995a"

printer = PrettyPrinter()

def get_data():
    endpoint = f"api/v7/currencies?apiKey={API_KEY}"
    url = BASE_URL + endpoint
    data = get(url).json()['results']
    return data

def get_currencies_list():
    endpoint = f"api/v7/currencies?apiKey={API_KEY}"
    url = BASE_URL + endpoint
    data = get(url).json()['results']
    data = list(data.items())
    data.sort()
    return data

def print_currencies(currencies):
    for name, currency in currencies:
        name = currency['currencyName']
        _id = currency['id']
        symbol = currency.get("currencySymbol", "")
        print(f"{_id} - {name} - {symbol}")

def exchange_rate(currency1, currency2):
    endpoint = f"api/v7/convert?q={currency1}_{currency2}&compact=ultra&apiKey={API_KEY}"
    url = BASE_URL + endpoint
    currencies = get_data()
    name1, name2, symbol1, symbol2 = [currencies[currency1]['currencyName'], currencies[currency2]['currencyName'], currencies[currency1]['currencySymbol'], currencies[currency2]['currencySymbol']]
    response = get(url)
    data = response.json()
    rate = list(data.values())[0]
    returner = [name1, symbol1, name2, symbol2, rate]
    print(f"The rate from {name1} to {name2} is {rate}")
    return returner


def convert(currency1, currency2, amount):
    transaction = exchange_rate(currency1, currency2)
    name1 = transaction[0]
    symbol1 = transaction[1] 
    name2  = transaction[2]
    symbol2 = transaction[3] 
    rate = transaction[4]
    
    if rate is None:
        return
    try:
        amount = float(amount)
    except:
        print('Oops! Invalid amount! Try again...')
        return
    if amount < 0:
        print('Oops! Invalid amount! Try again...')
        return

    converted_amount = rate * amount
    print(f"{symbol1}{amount} {name1} is equal to {symbol2}{converted_amount} {name2}s.")


def main():
    currencies_list = get_currencies_list()

    print("Welcome to the currency converter!")
    print("List - lists the different currencies")
    print("Convert - convert from one currency to another")
    print("Rate - get the exchange rate of two currencies")
    print("Q - to quit")
    print()

    while True:
        command = input(">>> ").lower()

        if command == "q":
            break
       
        elif command == "list":
            print_currencies(currencies_list)
       
        elif command == "convert":
            currency1 = input("Enter a base currency: ").upper()
            amount = input(f"Enter an amount in {currency1}: ")
            currency2 = input("Enter a currency to convert to: ").upper()
       
            try:
                convert(currency1, currency2, amount)
            except KeyError:
                print("Oops! That was no valid currency. Try again...")
       
        elif command == "rate":
            currency1 = input("Enter a base currency: ").upper()
            currency2 = input("Enter a currency to convert to: ").upper()
       
            try:
                exchange_rate(currency1, currency2)
            except KeyError:
                print("Oops! That was no valid currency. Try again...")
       
        else:
            print("Unrecognized command!")

main()


