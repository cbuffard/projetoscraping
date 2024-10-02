# importing what we need
import pandas as pd
import sqlite3
from datetime import datetime

# defining JSONL file path
# pd.read_json('..data/data.jsonl', lines=True)
df = pd.read_json('../data/data.jsonl', lines=True)
print(df)

# set pandas to display all columns
pd.options.display.max_columns = None

# Reading data from JSONL file and Displaying it in a Dataframe
 #  $ python transformacao/main.py

# Adding a coluna_source with a fixed value
df['_source'] = "https://lista.mercadolivre.com.br/tenis-corrida-masculino"

# Adding a coluna_data_coleta with a date and current time
df['_data_coleta'] = datetime.now()

# Treating the null values for the numeric and text columns

df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

# Removing the parentheses from column 'reviews_amount'
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)  #removing ()
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)   #tranforming into int

# Treating prices as Float and calculate total amounts
df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100

# Removing the old price columns
df.drop(columns=['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos'])

# Connecting to SQLite database (or create a new one)
conn = sqlite3.connect('../data/quotes.db')

# Saving the dataframe in SQLite database
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

# End connection with database
conn.close()

print(df.head())
          
    