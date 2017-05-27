import requests
import pandas as pd
import simplejson as json
from datetime import datetime

#User input data
tag = "FB"
opening=True
closing=False
adjopen = True
adjclose = False

urlstart = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?&ticker='
urlend = '&api_key=NBc3xNer5L7B91m3q1Cn'
url = urlstart+tag+urlend
r = requests.get(url)

data = json.loads(r.content)

stocks = pd.DataFrame.from_dict(data['datatable']['data'])
cols = pd.DataFrame.from_dict(data['datatable']['columns'])
stocks.columns = cols['name']

onestock = stocks.loc[stocks['ticker'] == tag]
stockdate = []
for strdate in onestock.date:
     stockdate.append(datetime.strptime(strdate,'%Y-%m-%d'))

from bokeh.plotting import figure, show, output_file
output_file("line.html")
p1 = figure(width=500,plot_height=500,title="Stock "+tag,x_axis_type="datetime")
if opening==True:
    p1.line(stockdate,onestock.open,color='blue',legend="Opening Price")
if closing==True:
    p1.line(stockdate,onestock.close,color='red',legend="Closing Price")
if adjopen==True:
    p1.line(stockdate,onestock.adj_open,color='green',legend="Ajusted Opening Price")
if adjclose==True:
    p1.line(stockdate,onestock.adj_close,color='navy',legend="Ajusted Closing Price")

p1.legend.location = "top_left"
p1.xaxis.axis_label = "Date"
p1.yaxis.axis_label = 'Price'

show(p1)
