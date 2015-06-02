# NeopianStockScraper
Script to scrape the current ticker prices for all the stocks in your portfolio and alert you when you need to sell. If you want to run this periodically, you'll need to get it set up on a unix system with cron available. In a terminal, enter the following to add the job to cron:  
sudo crontab -u root -e  
then add the line "*/30 * * * * sh \<path-to-repo\>/autorun.sh > \<path-to-repo\>/error_log" and save.

This uses mechanize, so you need to install it from http://wwwsearch.sourceforge.net/mechanize/

It also uses BeautifulSoup (bs4), which comes with most modern installations of Debian, Ubuntu, or Fedora. 
If you need to install it, you can get it at http://www.crummy.com/software/BeautifulSoup/

Since the script sends it's email through GMAIL smtp services, you may need to lower your security settings to accept access from "less secure" applications (since this just uses python's smtplib, not google's libraries, which afaik don't work with Python 3 yet). I'd recommend setting up the "user" as an empty new account that you don't care too much about, rather than risking a security issue with your primary.
