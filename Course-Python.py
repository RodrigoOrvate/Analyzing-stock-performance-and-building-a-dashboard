import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

#Question 1
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)

tesla_data.head()

#Question 2
url1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
response1 = requests.get(url1)
html_data1 = response1.text
#----------------------------------------------------
soup1 = BeautifulSoup(html_data1, 'html.parser')
#----------------------------------------------------
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"]) #1
table1 = soup1.find_all("tbody")[1] #2
data1 = []

for row1 in table1.find_all("tr")[1:]: #3
    cols1 = row1.find_all("td")  #4
    if len(cols1) > 1: #5
        date1 = cols1[0].get_text(strip=True)
        revenue1 = cols1[1].get_text(strip=True) 
        
        data1.append({"Date": date1, "Revenue": revenue1}) #6
        
tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame(data1)], ignore_index=True)
#----------------------------------------------------
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
tesla_revenue.tail()

#Question 3
gme = yf.Ticker("GME")
gme_data = tesla.history(period="max")
gme_data.reset_index(inplace=True)

gme_data.head()

#Question 4
url2 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
response2 = requests.get(url2)
html_data2 = response2.text
#----------------------------------------------------
soup2 = BeautifulSoup(html_data2, 'html.parser')
#----------------------------------------------------
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"]) #1
table2 = soup2.find_all("tbody")[1] #2
data2 = []

for row2 in table2.find_all("tr")[1:]: #3
    cols2 = row2.find_all("td")  #4
    if len(cols2) > 1: #5
        date2 = cols2[0].get_text(strip=True)
        revenue2 = cols2[1].get_text(strip=True) 
        
        data2.append({"Date": date2, "Revenue": revenue2}) #6
        
gme_revenue = pd.concat([gme_revenue, pd.DataFrame(data2)], ignore_index=True)
#----------------------------------------------------
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"")
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
gme_revenue.tail()

#Question 5
import numpy as np

tesla_revenue['Revenue'] = tesla_revenue['Revenue'].replace({'\$': '', ',': ''}, regex=True)
tesla_revenue['Revenue'] = tesla_revenue['Revenue'].replace('', np.nan)
tesla_revenue.dropna(subset=['Revenue'], inplace=True)
tesla_revenue['Revenue'] = tesla_revenue['Revenue'].astype(float)

make_graph(tesla_data, tesla_revenue, 'Tesla')

#Question 6
import numpy as np

gme_revenue['Revenue'] = gme_revenue['Revenue'].replace({'\$': '', ',': ''}, regex=True)
gme_revenue['Revenue'] = gme_revenue['Revenue'].replace('', np.nan)
gme_revenue.dropna(subset=['Revenue'], inplace=True)
gme_revenue['Revenue'] = gme_revenue['Revenue'].astype(float)

make_graph(gme_data, gme_revenue, 'GameStop')
