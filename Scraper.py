import mechanize
import cookielib
from bs4 import BeautifulSoup
import re
import time

# Your personal sell value
threshold = 60

def strip(s):
	return re.sub(r'\W+', '', s)
def main():
	# Browser
	br = mechanize.Browser()
	
	# Cookie Jar
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)
	
	# Browser options
	br.set_handle_equiv(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
	
	br.addheaders = [('User-agent', 'Chrome')]
	
	print('Connecting to Login')
	
	# The site we will navigate into, handling it's session
	br.open('http://neopets.com/login/')
	
	# Select the login form
	br.select_form(nr=0)
	
	# User credentials
	# TODO: MAKE SURE YOU FILL THESE IN YOU DINGUS
	br.form['username'] = ''
	br.form['password'] = ''
	
	# Login
	br.submit()
	print('Login submitted\nConnecting to Stock Market...')
	
	lows = []
	highs = []

	# Grab the stock market page and, because the people that make neopets don't
	# use classes or id's in their CSS (WTF), get all the tables in the page.
	# The only table that has "align: center" is the stock list, so we grab that one.
	full_stocks = br.open('http://www.neopets.com/stockmarket.phtml?type=list&full=true')
	table_soup = BeautifulSoup(full_stocks)
	s_tables = table_soup.find_all('table')
	
	for t in s_tables:
		if t.get('align') == 'center':
			stock_table = t.prettify()
			stocks = stock_table.split('<tr>');
			for stock_entry in stocks[2:]:
				stock = stock_entry.split('<td')
				
				# Ticker Symbol
				ticker = stock[2]
				ticker = ticker[ticker.find('<b>') + 3 : ticker.find('</b>')]
				ticker = strip(ticker)
	
				# Name
				name = stock[3]
				name = name[name.find('>') + 1 : name.find('<')]
				name = strip(name)
	
				# Current Price
				price = stock[5]
				price = price[price.find('<b>') + 3 : price.find('</b>')]
				price = strip(price)
				
				if int(price) > 14 and int(price) < 18:
					lows.append(ticker + ' ' + name + ': ' + price);

	# Okay, so the portfolio page on Neopets is ACTUAL garbage right now.
	# The response I'm getting back on this request has content AFTER a 
	# closing HTML tag. I have no clue what the hell is going on but someone
	# at Neopets should be fired. Along with the person who's still using
	# tables to lay out a page...
	#
	# For now, since the table items in the portfolio table are the only items
	# colored the way they are, I'm using those color values to grab them.
	# I KNOW THIS IS BAD, but sometimes you have to fight cludge with cludge.
	portfolio = br.open('http://www.neopets.com/stockmarket.phtml?type=portfolio')
	p_soup = BeautifulSoup(portfolio)
	p_entries = p_soup.find_all('tr')
	
	for t in p_entries:
		if t.get('bgcolor') == '#EEEEFF' or t.get('bgcolor') == '#FFFFFF':
			stock_entry = t.prettify()
			
			stock = stock_entry.split('<td')

			# Ticker Symbol
			ticker = stock[2]
			ticker = ticker[ticker.find('<a ') : ticker.find('</a>')]
			ticker = ticker[ticker.find('>') + 1 : ]
			ticker = strip(ticker)
			
			# Current Price
			price = stock[4]
			price = price[price.find('>') + 1 : price.find('<')]
			price = strip(price)
			
			if int(price) >= threshold:
				highs.append(ticker + ': ' + price);
			
	print(lows)
	print(highs)

if __name__ == '__main__':
	main()
