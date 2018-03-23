@echo off

rem CD into relevant directory
pushd "H:\"
cd "H:\HBS Data\Crawlers\pricebot"

rem Add conda to PATH, for the moment
set PATH=%PATH%;C:\Users\ela\Anaconda3;C:\Users\ela\Anaconda3\Scripts\
rem Activating scrapy env
call activate scrapy
echo Activated conda scrapy environment


scrapy crawl bilka_prices
scrapy crawl elgiganten_prices
scrapy crawl power_links
scrapy crawl power_prices
scrapy crawl punkt1_links
scrapy crawl punkt1_prices
scrapy crawl skousen_prices
scrapy crawl whiteaway_prices
scrapy crawl wupti_prices

call deactivate
echo Done scraping
