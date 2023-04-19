from forex_python.converter import CurrencyCodes, CurrencyRates

test1 = CurrencyCodes()

cur_symbol = test1.get_symbol('TRY') # Fetches currency symbol
cur_name = test1.get_currency_name('TRY') # Fetches currency name

print('\nThe currency name is: ' + cur_name)
print('The currency symbol is: ' + cur_symbol)

print('\n' + test1.get_symbol('USD'))
print(test1.get_currency_name('USD') + '\n')

currency_input = input('Enter a currency code (e.g. TRY): ')
amount = float(input('Enter an amount: '))

test2 = CurrencyRates()

if currency_input == 'USD':
    rate = 1
else:
    rate = test2.get_rate(currency_input, 'USD') # Fetches the conversion rate
    print(f'1 {currency_input} = {rate} USD')

converted_amount = test2.convert(currency_input, 'USD', amount) # Conversion
print(f'{amount} {currency_input} is equal to {converted_amount} USD')
