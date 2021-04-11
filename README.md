# real_estate_crawler
Crawling new offers and sending emails with info

## bazos_scraping.sh
runs Scripts from script/ folder and then moves today offers to folder of yesterday offers which are deleted

## Data 
two folders with json files 
code is comparing offers scraped today to offers scraped yesterday

## Scripts

### crawler.py
crawling the website and taking all offers with their details and storing them as json files

### send_email.py
comparing today offers (newly crawled json)with yesterday offers (previously crawled json) and if there are any new offers send an email
some error cathing of the data as well and in case of an error sends a separate email and does not send emails to usual recipient
 
