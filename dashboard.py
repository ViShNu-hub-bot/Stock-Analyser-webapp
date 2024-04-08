import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px 
from alpha_vantage.fundamentaldata import FundamentalData
from stocknews import StockNews

st.set_page_config(page_title="Stock Analyser by Vishnukanth K", page_icon="https://d1muf25xaso8hp.cloudfront.net/https%3A%2F%2Ff2fa1cdd9340fae53fcb49f577292458.cdn.bubble.io%2Ff1707399413438x566599438511616640%2F1698821223278%2520%25281%2529.jpeg?w=192&h=192&auto=enhance&dpr=1.5&fit=crop&q=75")

st.title('STOCK ANALYSER by Vishnukanth K')
ticker = st.sidebar.text_input('Ticker')
Start_Date = st.sidebar.date_input('Start Date')
End_Date = st.sidebar.date_input('End Date')



st.sidebar.markdown('## Connect With Me')
st.sidebar.markdown('[![View Vishnukanth K\'s LinkedIn Profile](https://img.shields.io/badge/-LinkedIn-blue?style=flat&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/vishnukanth-k-a5552327b/)](https://www.linkedin.com/in/vishnukanth-k-a5552327b/)')



selected_tab = st.sidebar.radio("Select Data Type", ["Pricing Data", "Fundamental Data", "Top 10 News","Stock Tickers"])



if selected_tab == "Stock Tickers":
   
    stock_tickers = [
        "AAPL (Apple Inc.)",
        "MSFT (Microsoft Corporation)",
        "AMZN (Amazon.com Inc.)",
        "GOOGL (Alphabet Inc. - Class A)",
        "FB (Meta Platforms Inc. - Class A)",
        "TSLA (Tesla Inc.)",
        "NVDA (NVIDIA Corporation)",
        "JPM (JPMorgan Chase & Co.)",
        "JNJ (Johnson & Johnson)",
        "V (Visa Inc. - Class A)",
        "PG (Procter & Gamble Company)",
        "PYPL (PayPal Holdings Inc.)",
        "MA (Mastercard Incorporated - Class A)",
        "HD (The Home Depot Inc.)",
        "BAC (Bank of America Corporation)",
        "DIS (The Walt Disney Company)",
        "NFLX (Netflix Inc.)",
        "NVS (Novartis AG - ADR)",
        "T (AT&T Inc.)",
        "INTC (Intel Corporation)",
        "PFE (Pfizer Inc.)",
        "VZ (Verizon Communications Inc.)",
        "MRK (Merck & Co. Inc.)",
        "CSCO (Cisco Systems Inc.)",
        "CMCSA (Comcast Corporation - Class A)",
        "XOM (Exxon Mobil Corporation)",
        "KO (The Coca-Cola Company)",
        "WMT (Walmart Inc.)",
        "NKE (NIKE Inc. - Class B)",
        "UNH (UnitedHealth Group Incorporated)",
        "CVX (Chevron Corporation)",
        "ORCL (Oracle Corporation)",
        "ADBE (Adobe Inc.)",
        "IBM (International Business Machines Corporation)",
        "CRM (Salesforce.com Inc.)",
        "MCD (McDonald's Corporation)",
        "TMO (Thermo Fisher Scientific Inc.)",
        "ABT (Abbott Laboratories)",
        "PEP (PepsiCo Inc.)",
        "SAP (SAP SE - ADR)",
        "PM (Philip Morris International Inc.)",
        "COST (Costco Wholesale Corporation)",
        "ABBV (AbbVie Inc.)",
        "BMY (Bristol-Myers Squibb Company)",
        "HON (Honeywell International Inc.)",
        "TXN (Texas Instruments Incorporated)",
        "LLY (Eli Lilly and Company)",
        "LIN (Linde plc)",
        "DHR (Danaher Corporation)",
        "NOW (ServiceNow Inc.)"
    ]

    st.write("List of Stock Tickers:")
    for i, ticker in enumerate(stock_tickers, start=1):
        st.write(f"{i}. {ticker}")

if selected_tab == "Pricing Data":
    st.header('Pricing Data')
    if not ticker:
        st.write("Please select a ticker.")
    elif not Start_Date or not End_Date:
        st.write("Please select a date range.")
    else:
        try:
            data = yf.download(ticker, start=Start_Date, end=End_Date)
            if data.empty:
                st.write("No data available for the specified date range.")
            else:
                st.write("Price Movements")
                data2 = data.copy()
                data2['% change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
                data2.dropna(inplace=True)
                st.write(data2)
                
                Annual_Return = data2['% change'].mean() * 252 * 100
                st.write('Annual Return is', Annual_Return, '%')
                
                stdev = np.std(data2['% change']) * np.sqrt(252)
                st.write('Standard Deviation is', stdev * 100, '%')
                
                risk_adj_return = Annual_Return / (stdev * 100)
                st.write('Risk-Adjusted Return is', risk_adj_return)
                
                fig = px.line(data, x=data.index, y=data['Adj Close'], title=ticker)
                st.plotly_chart(fig)
        
        except Exception as e:
            st.error(f"An error occurred: {e}")

elif selected_tab == "Fundamental Data":
    st.header('Fundamental Data')
    if not ticker:
        st.write("Please enter a ticker.")
    else:
        try:
            key = '7H33AXDC77KAVX1Z'
            fd = FundamentalData(key, output_format='pandas')
            
            st.subheader('Balance Sheet')
            balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
            bs = balance_sheet.T[2:]
            bs.columns = list(balance_sheet.T.iloc[0])
            st.write(bs)
            
            st.subheader('Income Statement')
            income_statement = fd.get_income_statement_annual(ticker)[0]
            is1 = income_statement.T[2:]
            is1.columns = list(income_statement.T.iloc[0])
            st.write(is1)
            
            st.subheader('Cash Flow Statement')
            cash_flow = fd.get_cash_flow_annual(ticker)[0]
            cf = cash_flow.T[2:]
            cf.columns = list(cash_flow.T.iloc[0])
            st.write(cf)
    
        except Exception as e:
            st.error(f"An error occurred: {e}")

elif selected_tab == "Top 10 News":
    st.header('Top 10 News')
    if not ticker:
        st.write("Please enter a ticker.")
    else:
        try:
            with st.spinner(f"Fetching news for {ticker}..."):
                st.header(f'News of {ticker}')
                sn = StockNews(ticker, save_news=False)
                df_news = sn.read_rss()
                if df_news is None or df_news.empty:
                    st.write(f"No news available for {ticker}")
                else:
                    for i in range(min(10, len(df_news))):
                        st.subheader(f'News {i+1}')
                        st.write(df_news['published'][i])
                        st.write(df_news['title'][i])
                        st.write(df_news['summary'][i])
                        title_sentiment = df_news['sentiment_title'][i]
                        st.write(f'Title Sentiment {title_sentiment}')
                        news_sentiment = df_news['sentiment_summary'][i]
                        st.write(f'News Sentiment {news_sentiment}')
        except Exception as e:
            st.error(f"An error occurred: {e}")
