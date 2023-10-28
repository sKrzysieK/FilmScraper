# *FilmScraper* 
FilmScraper is a webscraper created to collect information about films from Filmweb database.
It processes every film's data and formats it nicely. 
Finaly, it saves all gathered info to json file and to a mongodb database. 


## Getting started
In order to setup scraper you need to replace placeholders in settings.py and provide your mongodb database data. 
Then type `scrapy crawl filmspider` in your terminal to run a spider.

## How do I change output file name or format? 
In settings.py go to OUTPUT FILE SETTING section and change your output file name or format.


## What if I don't want to use database?
In such situation you can simply comment out MongoDBPipeline line in settings.py ( in ITEM_PIPELINES object )


