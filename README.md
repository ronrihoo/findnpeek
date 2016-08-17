# findnpeek
##Brief
Scrapes file(s) of interest from webpage(s) of interest.

##Quick Usage
Find the `pageAddress` variable (currently at line 50) and add the URL of interest.
```Python
pageAddress = 'http://www.example.com/webpage.html'
```

###Scrape File(s) from Given URL
If you are looking to scrape files from that URL, then go to the end of the file. Uncomment `findFiles()` and comment out `findFilesFromLinksOnPage(pageURLGrabber(), keyword)`.

```Python
findFiles()
#findLinks()
#findFilesFromLinksOnPage(pageURLGrabber(), keyword)
```
**Results:** invokes browser to load the files of interest (for instance, PDF files).

###Parse Link(s) from Given URL
If you are just looking for other links that exist at the given URL, then go to the end of the file. Uncomment `findLinks()` and comment out `findFilesFromLinksOnPage(pageURLGrabber(), keyword)`.

```Python
#findFiles()
findLinks()
#findFilesFromLinksOnPage(pageURLGrabber(), keyword)
```
**Results:** invokes browser to load the URLs of interest.

###Parse Link(s) from Given URL, then Scrape File(s) from the Links.
If you want to scrape files from webpages to which are linked on the given URL, then uncomment `findFilesFromLinksOnPage(pageURLGrabber(), keyword)` and make sure the other functions are commented out. This should be the case by default, at this time.

```Python
#findFiles()
#findLinks()
findFilesFromLinksOnPage(pageURLGrabber(), keyword)
```
**Results:** invokes browser to load the files of interest (for instance, PDF files).

## Extended Use
Where there is the will to write Python code, **findnpeek** is capable of providing a powerful start for your scraping projects. It already has for other Python projects. 

## Motivation
In 2015, Ronald Rihoo was writing a proof-of-concept paper for the W2CW (Warrior to Cyber Warrior) community. And he required the use of a script that could scrape files from webpages (just for viewing, hence "peek"). So he did the unspeakable: he recycled Python code from another one of his projects.

```findnpeek.py``` was derived from **Surfin' Man**, which is one of Ron's larger private projects. Originally, ```findnpeek.py``` is a modified version of ```findnkeep.py```, which scrapes for keeps and organizes files in directories that it automatically manages. 

Now, **findnpeek** is a project of its own, since it can serve as a web scraper for data analysts. And given its original purpose, project leaders can use **findnpeek** to test the work of web developers for scrape vulnerabilities. 

## Contributors
Feel free to become a part of this project and help advance it. If any potential is being missed, then please join and help make it happen.

When enough interest has been gained, the code will be cleaned up and some other parts of ```findnkeep.py``` will be pulled into this repository. 

## Thank You
Your interest in viewing this project is appreciated. 
