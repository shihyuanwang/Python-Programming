# Final Project - SHIH-YUAN WANG
# Scrape Yahoo Finance Data for Business Valuation Purpose 
#----------------------------------------------------------------------------------------------

import sys
import io
import re
import os
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd


# change current working directory
# os.chdir('/Users/ginawang/Desktop/Python Programming I/final-project-shihyuanwang')
# print(os.getcwd())


# 1. Download NASDAQ, NYSE, & AMEX company list files for reference

def download_company_list():

    url = 'https://www.nasdaq.com/screening/company-list.aspx'
    
    # Send get request and save it as response object
    res = requests.get(url)
    try:  # check for errors
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return ('Error: ' + str(e))

    # Pass it into the BeautifulSoup to parse the webpage
    soup = BeautifulSoup(res.text, "lxml")
    # print(soup.prettify())

    # Find the files download link through tag
    list_link = soup.find_all('a', href=re.compile(r'(.*)=download'))
    # print(list_link[0].get('href'))
    
    # Get NASDAQ, NYSE, and AMEX download link and save files
    for i in range(3):
        try:
            list_download_url = 'http://www.nasdaq.com' + list_link[i].get('href')
        except:
            return('Error: '+ str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
            raise

        list_res = requests.get(list_download_url)
        try:  # check for errors
            list_res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return ('Error: ' + str(e))

        # Save company list files for reference
        file_name = str(os.path.basename(list_download_url)) + '.csv'
        list_file = open(file_name, 'wb')
        for chunk in list_res.iter_content(100000):
            if chunk:
                list_file.write(chunk)
        list_file.close()

#---------------------------------------------------------------

# 2. Input a stock ticker to download historical stock prices and get the price on the specific day.

def scrape_price(ticker):
# Allows users to input a ticker to get historical stock prices

    # Get the historical price download url
    now = int(datetime.datetime.now().timestamp())
    price_url = "https://query1.finance.yahoo.com/v7/finance/download/" + ticker.upper() + "?period1=0&period2=" + str(now) + "&interval=1d&events=history&crumb=QGZTRYLeEZw"

    # Send post request and save it as response object
    price_res = requests.post(price_url)
    try:  # check for errors
            price_res.raise_for_status()
    except requests.exceptions.HTTPError as e:
            return ('Error: ' + str(e) + '\nPlease input the correct company ticker!')

    # Impersonate string data like a file
    f = io.StringIO(price_res.text)

    # Read data as a data frame
    price_df = pd.read_csv(f)
    return price_df


def scrape_date_price(ticker, date):
# Use the data frame from “scrape_price” to get the stock price on the specific day

    df = scrape_price(ticker)

    if not isinstance(df, pd.DataFrame):
        return ('Please input the correct company ticker!')
    else:
        date_price_df = df.loc[df['Date'] == date]

    # Check if 'df' is a data frame or HTTPError
    # And check if 'df' is an empty data frame (no such date or input error date format)
    if not date_price_df.empty :
        return date_price_df
    else:
        return ('Please input the correct date and format (YYYY-MM-DD)!')

#-----------------------------------------------------------------

# 3. Get the latest key statistics data, including valuation measures, trading information, and financial highlights.

def scrape_key_stats(*ticker):
# Allows users to input different company tickers to compare the latest statistics data

    # Create a list of statistics data frame index
    key_statistics = [
            "Market Cap (intraday)",
            "Enterprise Value",
            "Trailing P/E",
            "Forward P/E",
            "PEG Ratio (5yr expected)",
            "Price/Sales (ttm)",
            "Price/Book (mrq)",
            "Enterprise Value/Revenue",
            "Enterprise Value/EBITDA",
            "Beta (3Y Monthly)",
            "52-Week Change",
            "S&P500 52-Week Change",
            "52-Week High ",
            "52-Week Low ",
            "50-Day Moving Average",
            "200-Day Moving Average",
            "Avg Vol (3 month)",
            "Avg Vol (10 day)",
            "Shares Outstanding",
            "Float",
            "% Held by Insiders",
            "% Held by Institutions",
            "Shares Short",
            "Short Ratio",
            "Short % of Float",
            "Short % of Shares Outstanding",
            "Shares Short (prior month) ",
            "Forward Annual Dividend Rate",
            "Forward Annual Dividend Yield",
            "Trailing Annual Dividend Rate",
            "Trailing Annual Dividend Yield",
            "5 Year Average Dividend Yield",
            "Payout Ratio",
            "Dividend Date",
            "Ex-Dividend Date",
            "Last Split Factor (new per old)",
            "Last Split Date",
            "Fiscal Year Ends",
            "Most Recent Quarter (mrq)",
            "Profit Margin",
            "Operating Margin (ttm)",
            "Return on Assets (ttm)",
            "Return on Equity (ttm)",
            "Revenue (ttm)",
            "Revenue Per Share (ttm)",
            "Quarterly Revenue Growth (yoy)",
            "Gross Profit (ttm)",
            "EBITDA",
            "Net Income Avi to Common (ttm)",
            "Diluted EPS (ttm)",
            "Quarterly Earnings Growth (yoy)",
            "Total Cash (mrq)",
            "Total Cash Per Share (mrq)",
            "Total Debt (mrq)",
            "Total Debt/Equity (mrq)",
            "Current Ratio (mrq)",
            "Book Value Per Share (mrq)",
            "Operating Cash Flow (ttm)",
            "Levered Free Cash Flow (ttm)"]

    # Create a data frame to store statistics data
    stats_df = pd.DataFrame(index = key_statistics)

    # Iterate over all the tickers
    for t in ticker :

        stats_url = 'https://finance.yahoo.com/quote/' + t.upper() + '/key-statistics?p=' + t.upper()

        # Send get request and save it as response object
        stats_res = requests.get(stats_url)
        try: # check for errors
            stats_res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return ('Error: ' + str(e) + '\nPlease input the correct company ticker!')

        # Pass it into the BeautifulSoup to parse the webpage
        soup = BeautifulSoup(stats_res.text, "lxml")
        # print(soup.prettify())

        # items =soup.find_all('td', attrs={'class': re.compile(r'(.*)Miw\(140px\)|(.*)Pend\(10px\)')})
        # # print(items)
        # key_statistics = []
        # for i in items:
        #     item = i.get_text()
        #     key_statistics.append(item)
        # # print (key_statistics)

        # Find the value of each statistics element
        items_value = soup.find_all('td', attrs={'class':'Fz(s) Fw(500) Ta(end) Pstart(10px) Miw(60px)'})  # 59 items
        # print(items_value)

        # Append the value of each statistics element to a list
        statistics_value= []
        for i in items_value:
            value = i.get_text()
            statistics_value.append(value)
        # print (statistics_value)

        # Add this company's statistic data to the data frame
        try:
            stats_df[t] = statistics_value
            # print(stats_df)
        except:
            return('Please input the correct company ticker!')
            raise

    return stats_df

#-----------------------------------------------------------------

# 4. Get annual financial statement (Balance Sheet, Income Statement, and Cash Flow) data of the company.

def scrape_financials(ticker, financial_statement):
# Allows users to input a ticker and statement type to get the financial statements

    if financial_statement == 'Balance Sheet':
        financials_url = 'https://finance.yahoo.com/quote/' + ticker.upper() + '/balance-sheet?p=' + ticker.upper()

    elif financial_statement == 'Income Statement':
        financials_url = 'https://finance.yahoo.com/quote/' + ticker.upper() + '/financials?p=' + ticker.upper()

    elif financial_statement == 'Cash Flow':
        financials_url = 'https://finance.yahoo.com/quote/' + ticker.upper() + '/cash-flow?p=' + ticker.upper()

    else:
        return('Please input the correct financial statement name!')

    # Send get request and save it as response object
    financials_res = requests.get(financials_url)
    try: # check for errors
        financials_res.raise_for_status()
    except requests.exceptions.HTTPError as e:
         return ('Error: ' + str(e) + '\nPlease input the correct company ticker!')

    # Pass it into the BeautifulSoup to parse the webpage
    financials_soup = BeautifulSoup(financials_res.text, "lxml")
    # print(financials_soup.prettify())
    
    # Find all table elements on the page through tag
    try: # check for errors
        financials_table = financials_soup.select('table')[0]
        # print(financials_table)
    except:
        return('Please input the correct company ticker!')
        raise

    # Read data as a data frame
    financials_df = pd.read_html(str(financials_table))[0]
    try: # check for errors
        financials_df = financials_df.set_index(0)  # set the index to the first column
    except:
        return('Please input the correct company ticker!')
        raise

    new_header = financials_df.iloc[0]     # grab the first row for the header
    del financials_df.index.name           # delete the index name '0'
    financials_df = financials_df[1:]      # take the data except the header row
    financials_df.columns = new_header     # set the header row as the financials_df header
    # print(financials_df)
    # print(financials_df.to_string())

    return financials_df

#-----------------------------------------------------------------

# For output demonstration

download_company_list()

print(scrape_price('AAPL'))
print(scrape_price('GOOG'))

print(scrape_date_price('AAPL', '2019-08-26'))
print(scrape_date_price('GOOG', '2019-08-30'))

print(scrape_key_stats('AAPL','GOOG'))

print(scrape_financials('AAPL', 'Balance Sheet'))
print(scrape_financials('AAPL', 'Income Statement'))
print(scrape_financials('AAPL', 'Cash Flow'))
print(scrape_financials('GOOG', 'Balance Sheet'))
print(scrape_financials('GOOG', 'Income Statement'))
print(scrape_financials('GOOG', 'Cash Flow'))


# Check input error

# print(scrape_price('AAP3'))

# print(scrape_date_price('A123', '2019-08-26'))
# print(scrape_date_price('goog', '2019/08/30'))

# print(scrape_key_stats('AAPL','GOO'))

# print(scrape_financials('AAPL', 'Balance'))
# print(scrape_financials('YA', 'Balance Sheet'))


