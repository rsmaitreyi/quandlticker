# Import Dependencies
import config as con
import datetime
import quandl
import pandas as pd
import os
from bokeh.charts import output_file, TimeSeries
from bokeh.plotting import figure
from bokeh.embed import components
from flask import Flask, render_template, request, redirect, flash, url_for

import sys
import logging

app=Flask(__name__)

# These two lines are to get the error displayed heroku app
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)



#app.config.from_object(__name__)

# Retrieved Quandl API key by referring https://www.quandl.com/tools/python
quandl.ApiConfig.api_key = con.QUANDL_API_KEY
current_month = datetime.date.today().month
prior_month = current_month - 1
year = datetime.date.today().year


# ---------------------------------------------------------------------------
@app.route('/')
def main():
  return redirect('/index')


@app.route('/index', methods=['GET', 'POST'])
def index():
	 
	if request.method == 'POST':
		ticker = request.form['ticker'].upper()

		ticker_data = quandl.get('WIKI/' + ticker, collapse='daily')

		# Bokeh plot 
		title = ('Data for Stock ' + ticker)
		ts_plot = TimeSeries(ticker_data.Close[-30:], title = title, xlabel = 'Date', ylabel = 'Price ($ USD)')
		script, div = components(ts_plot)
		return render_template('graph.html', script=script, div=div)
	else:
		return render_template('index.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
