# findnpeek
##Brief
Scrapes file(s) of interest from webpage(s) of interest.

##Quick Usage
Find the pageAddress variable (currently at line 77) and add the URL of interest.
```Python
pageAddress = 'http://www.example.com/webpage.html'
```

###Scrape File(s) from Given URL
If you are looking to scrape files from that URL, then go to the end of the file. Uncomment findFiles() and comment findFilesFromLinksOnPage(pageURLGrabber(), keyword).

```Python
findFiles()
#findLinks()
#findFilesFromLinksOnPage(pageURLGrabber(), keyword)
```
**Results:** invokes browser to load the files of interest (for instance, PDF files).

###Parse Link(s) from Given URL
If you are just looking for other links that exist at the given URL, then go to the end of the file. Uncomment findLinks() and comment findFilesFromLinksOnPage(pageURLGrabber(), keyword).

```Python
#findFiles()
findLinks()
#findFilesFromLinksOnPage(pageURLGrabber(), keyword)
```
**Results:** invokes browser to load the URLs of interest.

###Parse Link(s) from Given URL, then Scrape File(s) from the Links.
If you want to scrape files from webpages to which are linked on the given URL, then uncomment findFilesFromLinksOnPage(pageURLGrabber(), keyword) and make sure the other functions are commented out. This should be the case by default, at this time.

```Python
#findFiles()
#findLinks()
findFilesFromLinksOnPage(pageURLGrabber(), keyword)
```
**Results:** invokes browser to load the files of interest (for instance, PDF files).

## Extended Usage
Where there is the will to write Python code, findnpeek is capable of providing a powerful start for your scraping projects. It has been for one of my own private Python projects. 

## Motivation
```findnpeek.py``` was derived from one of my larger private projects. It's a modified version of a file that's originally named ```findnkeep.py```. In 2015, I was writing a proof-of-concept paper for the W2CW (Warrior to Cyber Warrior) community, and I needed a script that could scrape files from webpages (just for viewing, hence "peek"). 

So I recycled ```findnkeep.py``` from my enormous Python project, Surfin' Man.

In the case that I notice there is interest for this project, I will clean the code up and share other parts of it. Until then, I will continue to use the time for my personal endeavors.

## Contributors
Feel free to become a part of this project. I am not emotionally attached to it. And I would like to see it grow.

## Thank You
I appreciate your interest in viewing this project. I hope that it will be just as useful to you as it has been to me.
