import streamlit as st
import pandas as pd
import sqlite3     # to read database

# Connecting to SQLite database
conn = sqlite3.connect('../data/quotes.db')

# Loading data from 'mercadolivre_items' table into a pandas dataframe
df = pd.read_sql_query("SELECT * FROM mercadolivre_items", conn)

# Ending conection with database
conn.close()

# Application Title
st.title('Market Research - Sports Sneakers in Mercado Livre Website')

# Improving layout with columns for KPIs
st.subheader('Main KPIs')
col1, col2, col3 = st.columns(3)

# KPI 1: Total number of items
total_itens = df.shape[0]
col1.metric(label="Total Number of Items", value=total_itens)
# KPI 2: Number of unique brands
unique_brands = df['brand'].nunique()
col2.metric(label="Number of Unique Brands", value=unique_brands)
# KPI 3: Average new price (in reais)
average_new_price = df['new_price'].mean()
col3.metric(label="New Average Price (R$)", value=f"{average_new_price:.2f}")

# Which Brands are the most common uo to page 10
st.subheader('Most common brands up to page 10')
col1, col2 = st.columns([4,2])
top_10_pages_brands = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_10_pages_brands)
col2.write(top_10_pages_brands)

# What is the average price per brand?

st.subheader('Average Price by Brand')
col1, col2 = st.columns([4,2])
average_price_by_brand = df.groupby('brand')['new_price'].mean().sort_values(ascending=False)
col1.bar_chart(average_price_by_brand)
col2.write(average_price_by_brand)

# What is the brand`s satisfaction?
st.subheader('Satisfaction per Brand')
col1, col2 = st.columns([4, 2])

# Filter reviews greater than 0
df_non_zero_reviews = df[df['reviews_rating_number'] > 0]

# Group by brand and calculate the mean satisfaction rating
satisfaction_by_brand = df_non_zero_reviews.groupby('brand')['reviews_rating_number'].mean()

# Plot bar chart in col1
col1.bar_chart(satisfaction_by_brand)

# Display the aggregated data in col2
col2.write(satisfaction_by_brand)
