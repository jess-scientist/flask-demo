from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import simplejson as json
from datetime import datetime
from bokeh.plotting import figure, show, output_file

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  return render_template('index.html')

def make_figure(tag,opening,closing,adjopen,adjclose):
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

  output_file('templates/input.html')  
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
  

@app.route('/input',methods=['POST'])
def read_input():
  opening,closing,adjopen,adjclose = False,False,False,False
  tag = request.form['ticker']
  if request.form.get('open'):
    opening=True
  if request.form.get('close'):
    closing=True
  if request.form.get('adjopen'):
    adjopen = True
  if request.form.get('adjclose'):
    adjclose = True
  make_figure(tag,opening,closing,adjopen,adjclose)
  return render_template('input.html')



if __name__ == '__main__':
  app.run(port=33507)
