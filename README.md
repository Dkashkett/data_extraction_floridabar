# data_extraction_floridabar
Motivation

This is a project I worked on for Upwork. The client wanted to scrape the contact information for all of the lawyers licensed by the California Bar Association. At the time there were around 89,000 listings across 1,800 pages. 

Code 

I used BeautifulSoup and Requests for the html parsing and wrote custom rules for the florida bar website. Scrape.py contaings all of the code to run the scraper. If you'd like to run the script you just need to update the max page count. The output is called master.csv. 

Clean.py is a custom script for cleaning the data and can be run as is. Its output is called florida_bar_scrape.csv