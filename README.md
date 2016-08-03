# findnpeek
Scrapes file(s) of interest from webpage(s) of interest.

##Quick Usage
Find the pageAddress variable (currently at line 77) and add the URL of interest.

###Scrape File(s) from Given URL
If you are looking to scrape files from that URL, then go to the end of the file. Uncomment findFiles() and comment findFilesFromLinksOnPage(pageURLGrabber(), keyword).

###Parse Link(s) from Given URL
If you are just looking for other links that exist at the given URL, then go to the end of the file. Uncomment findLinks() and comment findFilesFromLinksOnPage(pageURLGrabber(), keyword).

###Parse Link(s) from Given URL, then Scrape File(s) from the Links.
If you want to scrape files from webpages to which are linked on the given URL, then uncomment findFilesFromLinksOnPage(pageURLGrabber(), keyword) and make sure the other functions are commented out. This should be the case by default, at this time.
