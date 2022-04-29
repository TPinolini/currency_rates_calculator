import requests
import pandas as pd
from datetime import date

url = "http://api.exchangeratesapi.io/v1/latest?base=EUR&access_key=a33926c0f0263fce70c6531ece3ecdc5"
r = requests.get(url)

df = pd.DataFrame(r.json()).reset_index()
df.pop('success')
df.pop('timestamp')
df.pop('base')
df.pop('date')
df.rename(columns = {'index': 'Currency', 'rates':'Rate'}, inplace = True)
print(df.head())

to_save_file = f'{date.today()}.csv'
df.to_csv(to_save_file)
