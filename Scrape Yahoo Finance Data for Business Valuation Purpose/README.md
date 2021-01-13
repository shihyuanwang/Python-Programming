# Scrape Yahoo Finance Data for Business Valuation Purpose 

**A.	Problem:**

A business valuation is a general process of determining the economic value of a whole business or company unit. When a company is looking to sell all or a portion of its operations or looking to merge with or acquire another company, business valuation is typically conducted. There are numerous valuation methods, such as discounted cash flow, capitalized excess earnings, and comparable publicly traded company. However, when performing comparable company analysis, analysts should make a great effort to compare the current value of a business to other similar businesses by looking at trading multiples like Price/Earning, Enterprise Value/EBITDA, or other ratios. Therefore, it is bothersome for analysts to look for different companies’ historical stock prices, valuation multiples, and financial statements to measure value. In this project, it allows users to access business valuation data faster.

**B.	The input of the project:** 

1.	NASDAQ - Company List (NASDAQ, NYSE, & AMEX) (https://www.nasdaq.com/screening/company-list.aspx)
2.	Yahoo Finance (https://finance.yahoo.com/)

**C.	The output of the project:**

1.	NASDAQ, NYSE, and AMEX company list csv files
2.	Historical stock prices and the specific day stock price
3.	Statistics: comparison of the latest key statistics data, including valuation measures, trading information, and financial highlights 

**D.	Components and functionalities implemented in the project:**

Used modules: sys / io / re / os / requests / BeautifulSoup / datetime / pandas

•	Create a function “download_company_list” to download NASDAQ, NYSE, & AMEX company list csv files on the NASDAQ website for ticker reference.
1.	Send a request to the webpage URL and pass it into the BeautifulSoup to parse the webpage.
2.	Find the NASDAQ, NYSE, and AMEX download links using regular expression, send a request to download csv files, and then save these files.

The following steps using Apple Inc. (AAPL) and Alphabet Inc. (GOOG) to demonstrate the outputs scraped from Yahoo Finance:

•	Input a stock ticker to download historical stock prices and get the price on the specific day. 

Create a function “scrape_price” that allows users to input a ticker to get historical stock prices:

1.	Use datetime module to get the historical price download URL
2.	Send a request to download the historical stock price data file and use io module to impersonate string data like a file.
3.	Read this csv file using pandas module and return a data frame.

Create a function “scrape_date_price” that allows users to input a ticker and specific date to get the stock price:
1.	Use the data frame from “scrape_price” to get the stock price on that day.

•	Get the latest key statistics data, including valuation measures, trading information, and financial highlights.

Create a function “scrape_key_stats” that allows users to input different company tickers to compare the latest statistics data.

1.	Create a data frame and index to store statistics data using pandas module.
2.	Send a request to download the company’s statistics URL and pass it into the BeautifulSoup to parse the webpage.
3.	Find the value of each statistics element and append it to a list.
4.	Add this company's statistics data list to the previous data frame and return the final data frame.

•	Get annual financial statement (Balance Sheet, Income Statement, and Cash Flow) data of the company.

Create a function “scrape_financials” that allows users to input a ticker and statement type to get the financial statements:

1.	Send a request to the Balance Sheet, Income Statement, or Cash Flow webpage and pass it into the BeautifulSoup to parse the webpage.
2.	Find all table elements on the page and read this table using pandas module.
3.	Clean up the data and return a data frame.

**E.	Flow chart of all the components:**

![image](https://github.com/shihyuanwang/Python-Programming/blob/master/Scrape%20Yahoo%20Finance%20Data%20for%20Business%20Valuation%20Purpose/Flowchart.png)
