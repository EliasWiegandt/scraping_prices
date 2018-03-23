@echo off

rem CD into relevant directory
pushd "H:\"
cd "H:\HBS Data\Crawlers\pricebot"

rem Add conda to PATH, for the moment
set PATH=%PATH%;C:\Users\ela\Anaconda3;C:\Users\ela\Anaconda3\Scripts\
rem Activating scrapy env
call activate scrapy
echo Activated conda environment


REM python "run_crawler_process_selenium.py"
REM if errorlevel 1 pause

REM python "run_crawler_process.py"
REM if errorlevel 1 pause
REM
REM echo Scraped the data
REM call deactivate
REM pause

scrapy crawl power_links
scrapy crawl power_prices
scrapy crawl elgiganten_prices
scrapy crawl skousen_prices
