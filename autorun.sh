TIME=`date +%T | cut -d':' -f-2`
HOUR=`echo $TIME | cut -d':' -f1`
MINUTE=`echo $TIME | cut -d':' -f2`
if [ "$HOUR" = "08" -a "$MINUTE" = "30" ]; then
	python /<path-to-repo>/Scraper.py -d
else
	python /<path-to-repo>/Scraper.py
fi 
