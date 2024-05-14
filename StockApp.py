#ML SL-1 Data Visualization
#Dev. Naman, Mann, Rohan

import streamlit as st 
import pandas as pd 
import numpy as np 
import yfinance as yf 
import plotly.express as px
from stocknews import StockNews

st.title("Stock Dashboard")

#This line inputs the name of the company
ticker = st.sidebar.text_input("Ticker:") 

#This line inputs the Start Date
start_date = st.sidebar.date_input("Start Date:")

#This line inputs the End Date
end_date = st.sidebar.date_input("End Date:")

#Downloading the data for the Ticker from Yahoo Finance
data = yf.download(ticker,start = start_date, end = end_date)
fig = px.line(data,x = data.index, y = data["Adj Close"], title = ticker)
st.plotly_chart(fig)


pricing_data,per_change,volume,news = st.tabs(["Pricing Data","Percentage Change","Volume","Top 10 News"])

#TAB 1 - PRICING DATA
with pricing_data:
    st.header("Price Movements")
    data2 = data
    data2["Change %"] = data["Adj Close"] / data["Adj Close"].shift(1) - 1
    data2.dropna(inplace = True)
    st.write("These are the Price movements for {} from {} to {}".format(ticker,start_date,end_date))
    st.write(data2)
    annual_return = data2["Change %" ].mean()*252*100
    st.write("Annual Return is ",annual_return, "%")
    stdev = np.std(data2["Change %"])*np.sqrt(252)
    st.write("Standard Deviation is: ", stdev*100, "%")
    st.write("Risk Adj. Return is: ",annual_return/ (stdev*100))

#TAB 2 - ROC
with per_change:
    st.header("ROC Chart")
    fig = px.line(data2, x=data2.index, y = data2["Change %"])
    st.write("This is a Rate of Change chart calculated on daily Adj. Close of {} ".format(ticker))
    st.plotly_chart(fig)

#TAB 3 - VOLUME
with volume:
    st.header("Volume")
    fig = px.bar(data2, x = data2.index, y = data2["Volume"])
    st.write("This is a Volume chart which shows how many shares of {} were traded on a daily basic between {} and {} ".format(ticker,start_date,end_date))
    st.plotly_chart(fig)

#TAB 4 - NEWS

with news:
    st.header("News of {}".format(ticker))
    sn = StockNews(ticker, save_news = False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f"News {i+1}")
        st.write(df_news ["published" ][i])
        st.write(df_news["title"][i])
        st.write(df_news ["summary"][i])
