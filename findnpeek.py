'''
# findnpeek.py
#
# brief: has three main functions, findFiles(), findLinks(), and findFilesFromLinksOnPage().
#
#        findFiles()
#
#           Looks for PDF file addresses at the given URL, then opens the
#           the default browser to load the PDF file address, 5 addresses
#           at a time. Two log files are created/updated in a 'findnpeek'
#           folder; one for the searched URLs and another for the PDF
#           addresses that are found.
#
#        findLinks()
#
#           Looks for URLs in a HTML files, then invokes the browser to 
#           load the URLs one at a time. No logging has yet been implemented
#           for this function.
#
#        findFilesFromLinksOnPage()
#
#           Looks for URLs of other webpages at the given URL. Then looks for 
#           PDF files at each one of the found webpage URLs, and invokes the
#           browser to load the found PDF files; however, it prompts the user 
#           to decide whether the next found URL should be searched for PDF files.
#
#
# linkFinder()
#
#   *Limitation[1]:   keyword ".html" fails for URLs that look like API calls. For instance,
#
#                         src="//www.googletagmanager.com/ns.html?id=DFE-3N24"
#
#                     -will return, 
#
#                         http//www.googletagmanager.com/ns.html
#
#                     It would be an easy update, but why add a feature that might not be used?
#
# Author: Ron Rihoo
'''

import sys
import os
import urllib2
import webbrowser
from HTMLParser import HTMLParser
import stringparser

pageAddress = ''
filetype = ".pdf"                          # extension of filetype
keyword = ".html"                          # expected keyword in a link to be found in HTML code
pathname = 'findnpeek'                     # folder name
_p = 5                                     # number of links to search for files and invoke browser per file

# Will create a folder for findnpeek if one doesn't exist in the running directory
def folderMaker():
    loop = 1

    # Allow user to change the folder name
    # pathname = raw_input('Folder name (for this run): ')
    # if (pathname == ''):
    #       pathname = 'findnpeek'

    fullpath = os.path.realpath(0) + '\\' + pathname

    while (loop <= 5):
        print "Looking for " + fullpath

        if not os.path.isdir(pathname):                                         # if pathname does not exist
            print "Directory does not exist."                               # notify user
            print "Attempting to make directory " + pathname                        
            os.makedirs(pathname)                                           # make directory based on the desired pathname
            os.chdir(pathname)                                              # change to directory
            print "\\" + pathname + " has been successfully created."
            loop = 6
        else:                                                                   # or else just change directory to it
            print "...\nIt exists."
            os.chdir(pathname)

            if os.getcwd() != fullpath:
                print("Something went wrong. [Trial %d]" % loop)
                loop = loop + 1
            else:
                loop = 6
    return

# Gives us the freedom to grab the URL in whichever way we want without having
# to mess with the main portion of the code.
def pageURLGrabber():
    # grab from command line
    #pageURL = str(sys.argv[1])

    # preset
    pageURL = pageAddress
    #pageURL = ''

    # grab from input
    #print('Please enter the URL in the complete format: http://www.example.com/')
    #pageURL = raw_input('URL: ')

    return pageURL

# for concatenating two strings
def strConcat(str1, str2):
    str3 = str1 + str2
    return str3

# for keeping track of URL's
def siteLogger(givenURL):
    url_Log = open("..\\findnpeek\\url_Log.txt", "a")               # open log file (to append into file)
    nURL = givenURL + '\n'
    url_Log.write(nURL)                                             # print the given URL into the log file
    url_Log.close()                                                 # close log file
    return


fileLogw = ''           # variable to temporarily hold file log writes
file_URLs = []          # array to later hold URLs in as strings
file_URLs.append('')
_j = 0                  # loop counter

# parses through HTML code at the given URL
class codeParser(HTMLParser):
    def handle_starttag(self, tag, src):
        global _j
        global file_URLs
        if tag == 'a':
            for word in src:
                textx = word
                for texty in textx:
                    if filetype in texty:
                        if (_j != 0):
                            if (texty != file_URLs[_j-1]):
                                _j = _j + 1
                                file_URLs.append(texty)
                        else:
                            _j = _j + 1
                            file_URLs[0] = texty

# writes all URLs to a log file
def logURLs(URL_list, logFileId):
    if (logFileId == 1):
        fileLogw = open('..\\findnpeek\\fileLog.txt', 'a')
    elif (logFileId == 2):
        fileLogw = open('..\\findnpeek\\linkLog.txt', 'a')
    else:
        fileLogw = open('..\\findnpeek\\unknownIdLog.txt', 'a')
    try:
        for URL in URL_list:
            print >> fileLogw, URL
    except:
        pass
    fileLogw.close()

# finds files that are of the indicated filetype
def fileFinder(webpageURL = pageURLGrabber()):
    global file_URLs
    siteLogger(webpageURL)
    findings = codeParser()
    findings.feed(readRemoteHTMLFile(webpageURL))
    file_URLs = urlFixer(file_URLs, webpageURL)
    logURLs(file_URLs, 1)

# returns a URL list
def linkFinder(keyword):
    loop = False
    s = readRemoteHTMLFile(pageURLGrabber())
    a = 0
    b = 0
    t = ''
    linkArray = []
    link = stringparser.getHtmlLinkViaKeywordLaterals(s, keyword)
    if link != None:
        linkArray.append(link)
        loop = True
    # while link != None, but "loop = True/False" will look better for some
    while loop == True:
        # index of the link in the string (the string holds the HTML code)
        a = s.index(link)
        b = len(link)
        # temp string from the end of the last found link to the end of the string
        t = s[a+b:]
        link = stringparser.getHtmlLinkViaKeywordLaterals(t, keyword)
        if (link == "Not found." or link == None):
            loop = False
        else:
            linkArray.append(link)
    for item in linkArray:
        linkArray[linkArray.index(item)] = stringparser.removeBackslashes(item)
    linkArray = removeRepeatedStrings(linkArray)
    for link in linkArray:
        siteLogger(link)
    return linkArray

# returns a string
def readRemoteHTMLFile(remoteAddress):
    sock = urllib2.urlopen(remoteAddress)
    string = sock.read()
    sock.close()
    return string

# returns a string
def readLocalHTMLFile(directory):
    import codecs
    return codecs.open(directory, 'r').read()

# returns a string list
def removeRepeatedStrings(stringList):
    temp = []
    for item in stringList:
        if item not in temp:
            temp.append(item)
    return temp

# prints URLs
def printAllLinks(links):
    for link in links:
        print link

def urlFixer(url_List, webpageUrl):
    for i in xrange(len(url_List)):
        URL = url_List[i]
        temp = urlChecker(URL)
        # if the test fails, then we've found a local directory address
        if (temp == "failed"):
            # get the domain of the original webpage URL
            domain = urlDomainSplitter(webpageUrl)
            if (domain != "failed"):
                # concatenate the original domain to the URL found
                print domain + URL
                url_List[i] = domain + URL
            else:
                print "urlFixer: failed"
                url_List[i] = ""
    return url_List

def urlChecker(URL):
    arr = [ "com", "net", "org", "biz", "io" ];
    temp = ""
    #simple test
    if "http" in URL:
        if URL.index("http") == 0:
            return URL
    elif "www." in URL:
        if URL.index("www.") == 0:
            return URL
        temp = urlBareMinimum(URL)
    elif temp == "failed":
        return "failed"
    else:
        return URL

# uses a variety of tests to split the domain out of the provided URL
def urlDomainSplitter(URL):
    arr = [ "com", "net", "org", "biz", "io" ];
    if "http" in URL:
        # add artificial slash for cases that don't already have one at the end: 
        # e.g., http://www.example.com
        URL = URL + "/"
        index = URL.index("//") + 2
        domain = stringparser.splitRightAspect_toSubstring(URL, index, "/")
        return URL[0:index] + domain
    elif "www." in URL:
        # add artificial slash for cases that don't already have one at the end
        URL = URL + "/"
        index = URL.index("www.") + 4
        domain = stringparser.splitRightAspect_toSubstring(URL, index, "/")
        return URL[0:index] + domain
    else:
        urlBareMinimum(URL)

def urlBareMinimum(URL):
        # add artificial slash for cases that don't already have one at the end
        URL = URL + "/"
        temp = ""
        domain = stringparser.splitRightAspect_toSubstring(URL, 0, "/")
        for a in arr:
            if a in domain:
                temp = domain
                return temp
        if temp == "":
            return "failed"
        
def findFiles(webpageURL = pageURLGrabber()):
    a = webpageURL              # a for address
    b = webbrowser.get()        # b for browser
    i = 0                       # i for iteration  -- loop counter
    k = 0                       # k for keep -- while-loop off/on state
    p = 5                       # p for pages -- the quantity of URLs to open before being prompted for more

    print "Finding URL(s) of file(s)..."
    fileFinder(a)

    if (file_URLs[0] == ''):
        print "No link to a " + filetype + " file found at given webpage."
    else:
        while (i <= _j - 1):

            # Check URL and fix it if necessary
            #file_URLs[i] = urlFixer(a, file_URLs[i])

            print "found a " + filetype + " file at: " + file_URLs[i]

            print "Opening default browser..."
            b.open(file_URLs[i])
            i = i + 1
            
            # open only p (preset to 5) URLs at a time in the default browser (as new tabs) to not clog up the system
            # change p to any number of URLs you'd like to load before being prompted for more p-amount of URLs to open.
            if (i % p == 0 and p != 0):
                k = 1

                # error-checking needs to be improved later
                while (k == 1):
                    more = raw_input(str(i) + '/' + str(_j) + ' URLs opened. Open up more? (y/n): ')
                    if(more == 'y'): k = 0;
                    if(more == 'n'): i = _j; k = 0;

        if (i == _j):
            print "Run completed."

def findLinks(webpageURL = pageURLGrabber()):
    a = webpageURL              # a for address
    b = webbrowser.get()        # b for browser
    i = 0                       # i for iteration  -- loop counter
    k = 0                       # k for keep -- while-loop off/on state
    p = _p                      # p for pages -- the quantity of URLs to open before being prompted for more

    print "Finding URL(s)..."
    link_List = linkFinder(keyword)
    _j = len(link_List)

    if (len(link_List) < 1):
        print "No links containing the keyword \"" + keyword + "\" found at given webpage."
    elif (link_List[0] == ''):
        print "No links containing the keyword \"" + keyword + "\" found at given webpage."
    else:
        while (i <= _j - 1):
            # Check URL and fix it if necessary
            #link_List[i] = urlFixer(a, link_List[i])

            print "found: " + link_List[i]

            #print "Opening default browser..."
            #b.open(link_List[i])
            print link_List[i]
            i = i + 1
            
            # open only p (preset to 1) URLs at a time in the default browser (as new tabs) to not clog up the system
            # change p to any number of URLs you'd like to load before being prompted for more p-amount of URLs to open.
            if (i % p == 0 and p != 0):
                k = 1

                # error-checking needs to be improved later
                while (k == 1):
                    more = raw_input(str(i) + '/' + str(_j) + ' URLs opened. Open up more? (y/n): ')
                    if(more == 'y'): k = 0;
                    if(more == 'n'): i = _j; k = 0;

        if (i == _j):
            print "Run completed."
            # And just in case someone uses findFiles() after invoking findLinks()
            _j = 0

def cleanUrls(url_List):
    prefix = "http://"
    prefix_s = "https://"
    for i in xrange(len(url_List)):
        URL = url_List[i]
        print URL
        if "http" not in URL:
            if (URL.index("//") >= 0):
                url_List[i] = prefix + URL[URL.index("//") + 2:]
            elif (URL.index("www." > 0)):
                url_List[i] = prefix + URL[URL.index("www."):]
    return url_List

def switchToSecureUrl(URL):
    try:
        return "https" + URL[URL.index("http://") + 4:]
    except:
        return "failed"

def findFilesFromLinksOnPage(webpageURL = pageURLGrabber, urlKeyword = keyword):
    f = False                   # fail test
    i = 0                       # i for iteration  -- loop counter
    k = 0                       # k for keep -- while-loop off/on state
    p = _p                      # p for pages -- the quantity of URLs to open before being prompted for more    
    print "Finding URL(s) of webpage(s)..."
    link_List = linkFinder(urlKeyword)
    try:
        assert link_List[0]
    except:
        f = True                # failed
    if (f):
        print "No links containing the keyword \"" + keyword + "\" found at given webpage."
    else:
        _j = len(link_List)
        print str(_j) + " URLs found with the keyword '" + keyword + "'"
        link_List = cleanUrls(link_List)
        while (i <= _j - 1):
            print "Finding files from " + link_List[i]
            try:
                findFiles(link_List[i])
            except:
                print "Failed to load the page from " + link_List[i]
                print "Readjusting URL to 'https'..."
                temp = switchToSecureUrl(link_List[i])
                if temp != "failed":
                    link_List[i] = temp
                    try:
                        print "Finding files from " + link_List[i]
                        findFiles(link_List[i])
                    except:
                        print "Unable to load page from " + link_List[i]
                else:
                    print "Unable to load page from " + link_List[i]
            i = i + 1
            # open only p (preset to 1) URLs at a time in the default browser (as new tabs) to not clog up the system
            # change p to any number of URLs you'd like to load before being prompted for more p-amount of URLs to open.
            if (i % p == 0 and p != 0):
                k = 1
                while (k == 1):
                    more = raw_input(str(i) + '/' + str(_j) + ' URLs opened. Open up more? (y/n): ')
                    if(more == 'y'): k = 0;
                    if(more == 'n'): i = _j; k = 0;
        if (i == _j):
            print "Run completed."
            # And just in case someone uses findFiles() after invoking findLinks()
            _j = 0

# change to or make a folder, then run the main function
folderMaker()

# the three main functionalities of findnpeek.py
#findFiles()
#findLinks()
findFilesFromLinksOnPage(pageURLGrabber(), keyword)