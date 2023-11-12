# Putusan Mahkamah Agung Data Scrapper

This code is used for scraping data on the website: [https://putusan3.mahkamahagung.go.id/search.html](https://putusan3.mahkamahagung.go.id/search.html)

![scraping1](1.png)

![scraping2](2.png)

## Usage and How to use

usage: python scrap.py -k "your keyword" -t "098298PN333" -sd -dp -rg "5"

Note: for task from campus, i set this code only retrieve data if link download pdf from web available

```
Optional arguments:
    -sd         Sort date (Scraping from newest) Default False
    -dp         Downloadpdf (Download pdf file) Default False
    -t          Court type (Because encode from web, i just get from web then paste to variable or cmd) Default False
    -rg         Range (Limit range scraping from web based page) Default False
```

# Document Search Engine

Document Search Engine is a document retrieval based on a query, in this code I made it based on Amar Putusan by using the Euclidean Distance formula for similarity then displaying it in the command prompt based on the smallest Euclidean Distance and details of the data text and no putusan

Note: the code in main.py

