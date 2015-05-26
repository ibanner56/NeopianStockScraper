import mechanize
import cookielib
from bs4 import BeautifulSoup
import re

def strip(s):
	return re.sub(r'\W+', '', s)

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

print("Connecting to Login")

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
print("Login submitted\nConnecting to Stock Market...")

# Grab the stock market page and, because the people that make neopets don't
# use classes or id's in their CSS (WTF), get all the tables in the page.
# The only table that has "align: center" is the stock list, so we grab that one.
response = br.open("http://www.neopets.com/stockmarket.phtml?type=list&full=true")
soup = BeautifulSoup(response)
tables = soup.find_all("table")

for t in tables:
	if t.get("align") == "center":
		stock_table = t.prettify()
		stocks = stock_table.split("<tr>");
		for stock_entry in stocks[1:]:
			stock = stock_entry.split("<td")
			
			# Ticker Symbol
			ticker = stock[2]
			ticker = ticker[ticker.find("<b>") + 3 : ticker.find("</b>")]
			ticker = strip(ticker)

			# Name
			name = stock[3]
			name = name[name.find(">") + 1 : name.find("<")]
			name = strip(name)

			# Sales Volume
			price = stock[5]
			price = price[price.find("<b>") + 3 : price.find("</b>")]
			price = strip(price)

			print(ticker + " - " + name)
			print("Current Stock Price: " + price)
