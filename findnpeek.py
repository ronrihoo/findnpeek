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
# fileFinder()
#
#   *Note[1]: Turned urlFixer() off (commented it out) for now.
#
#   *Heads-up[1]: urlFixer(str m, str n) requires more URL analysis techniques, since
#                 it doesn't currently know if it has a full URL, or just a local
#                 directory reference that's made in the HTML code of the webpage.
#                 Current technique list:
#                   (1) ANDs the given URL, m, with the found URL, n. If the given
#                       URL is not a part of the found URL, then it concatenates m
#                       to the left (beginning) of n. This produces Bug[1].
#
#   *Bug[1]:   urlFixer(str m, str n) does not know anything about the found URL,
#              n, and it just tries to see if the given URL, m, is a part of it.
#              So if a link to an external PDF file (hosted on a different domain) 
#              is found on the webpage at the given URL, then that perfectly good 
#              URL becomes bad, since m is not a part of n and, so, urlFixer() 
#              concatenates m to n anyway. As an example:
#
#                 Given URL, m: http://cyberphit.net/
#                 Found URL, n: http://homenetworkwarrior.com/Cyber_Phit_1.1.pdf
#                 "Fixed URL" : http://cyberphit.net/http://homenetworkwarrior.com/Cyber_Phit_1.1.pdf
#
#   *Bug[2]: I'll have to come back to this later, but the PDF addresses are
#            not fixed before logging them. This will have to be corrected.
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
#                         //www.googletagmanager.com/ns.html
#
#                     This is an easy fix. I just don't care to fix it yet. Why bother when
#                     it's not clear whether anyone will need the extended sight?
#
# Author: Ron Rihoo
'''

import sys
import os
import urllib2
import webbrowser
from HTMLParser import HTMLParser

pageAddress = 'http://events.pentaho.com/field-guide-to-hadoop-registration-lis.html?'
filetype = ".pdf"                          # extension of filetype
keyword = ".html"                          # expected keyword in a link to be found in HTML code
pathname = 'findnpeek'                     # folder name

# this function will create a folder for itself if one doesn't exist in the running directory
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

# This function gives us the freedom to grab the URL in whichever way we want without having
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

# for parsing through the HTML code at the given URL
class codeParser(HTMLParser):

        def handle_starttag(self, tag, src):

                global _j
                global file_URLs

                if tag == 'a':
                
                        for word in src:
                                textx = word

                                fileLogw = open('..\\findnpeek\\fileLog.txt', 'a')

                                for texty in textx:

                                        if filetype in texty:
                                                if (_j != 0):
                                                        if (texty != file_URLs[_j-1]):
                                                                _j = _j + 1
                                                                file_URLs.append(texty)
                                                                print >> fileLogw, texty
                                                else:
                                                        _j = _j + 1
                                                        file_URLs[0] = texty
                                                        print >> fileLogw, texty


                                fileLogw.close()

# for finding files that are of the indicated filetype
def fileFinder(webpageURL = pageURLGrabber()):
        siteLogger(webpageURL)
        findings = codeParser()
        findings.feed(readRemoteHTMLFile(webpageURL))
        return

def linkFinder(keyword):
        import stringparser

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

def removeRepeatedStrings(stringList):
    temp = []
    for item in stringList:
        if item not in temp:
            temp.append(item)
    return temp

def printAllLinks(links):
    for link in links:
        print link

# for checking URLs and fixing them if necessary
# m: the original URL
# n: the address found in the HTML code for the file
def urlFixer(m, n):
        if(m and n != m):
                n = strConcat(m, n)
        
        return n

        
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

    a = webpageURL()            # a for address
    b = webbrowser.get()        # b for browser
    i = 0                       # i for iteration  -- loop counter
    k = 0                       # k for keep -- while-loop off/on state
    p = 1                       # p for pages -- the quantity of URLs to open before being prompted for more

    
    print "Finding URL(s)..."
    link_List = linkFinder(keyword)
    _j = len(link_List)

    if (link_List[0] == ''):
        print "No links containing the keyword \"" + keyword + "\" found at given webpage."
    else:
        while (i <= _j - 1):

            # Check URL and fix it if necessary
            #link_List[i] = urlFixer(a, link_List[i])

            print "found: " + link_List[i]

            print "Opening default browser..."
            b.open(link_List[i])
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

def findFilesFromLinksOnPage(webpageURL = pageURLGrabber, urlKeyword = keyword):
    i = 0                       # i for iteration  -- loop counter
    k = 0                       # k for keep -- while-loop off/on state
    p = 1                       # p for pages -- the quantity of URLs to open before being prompted for more    
    print "Finding URL(s) of webpage(s)..."
    link_List = linkFinder(urlKeyword)
    if (link_List[0] == ''):
        print "No links containing the keyword \"" + keyword + "\" found at given webpage."
    else:
        _j = len(link_List)
        print str(_j) + " URLs found with the keyword '" + keyword + "'"
        while (i <= _j - 1):
            print "Finding files from " + link_List[i]
            findFiles(link_List[i])
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

# change to or make a folder, then run the main function
folderMaker()

# the two main functionalities of findnpeek.py
#findFiles()
#findLinks()
findFilesFromLinksOnPage(pageURLGrabber(), keyword)