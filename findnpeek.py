'''
# findnpeek.py
#
# brief: looks for PDF file addresses at the given URL, then opens the
#        the default browser to load the PDF file address, 5 addresses
#        at a time. Two log files are created/updated in a 'findnpeek'
#        folder; one for the searched URLs and another for the PDF
#        addresses that are found.
#
# Author: Ron Rihoo
#
# Contributors: none yet.
#
# *Note[1]:     Turned urlFixer() off (commented it out) for now. School and other
#               projects have had the higher priority.
#
# *Heads-up[1]: urlFixer(str m, str n) requires more URL analysis techniques, since
#               it doesn't currently know if it has a full URL, or just a local
#               directory reference that's made in the HTML code of the webpage.
#               Current technique list:
#                 (1) ANDs the given URL, m, with the found URL, n. If the given
#                     URL is not a part of the found URL, then it concatenates m
#                     to the left (beginning) of n. This produces Bug[1].
#
# *Bug[1]:   urlFixer(str m, str n) does not know anything about the found URL,
#            n, and it just tries to see if the given URL, m, is a part of it.
#            So if a link to an external PDF file (hosted on a different domain) 
#            is found on the webpage at the given URL, then that perfectly good 
#            URL becomes bad, since m is not a part of n and, so, urlFixer() 
#            concatenates m to n anyway. As an example:
#
#               Given URL, m: http://cyberphit.net/
#               Found URL, n: http://homenetworkwarrior.com/Cyber_Phit_1.1.pdf
#               "Fixed URL" : http://cyberphit.net/http://homenetworkwarrior.com/Cyber_Phit_1.1.pdf
#
# *Bug[2]: I'll have to come back to this later, but the PDF addresses are
#          not fixed before logging them. This will have to be corrected.
#
'''

import sys
import os
import urllib2
import webbrowser
from HTMLParser import HTMLParser

filetype = ".pdf"                          # extension of filetype
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
        pageURL = ''

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
def fileFinder():

        findings = codeParser()

        sock = urllib2.urlopen(pageURLGrabber())
        
        siteLogger(pageURLGrabber())

        findings.feed(sock.read())

        sock.close()

        return

# for checking URLs and fixing them if necessary
# m: the original URL
# n: the address found in the HTML code for the file
def urlFixer(m, n):
        if(m and n != m):
                n = strConcat(m, n)
        
        return n

        
def main():

    a = pageURLGrabber()        # a for address
    b = webbrowser.get()        # b for browser
    i = 0                       # i for iteration  -- loop counter
    k = 0                       # k for keep -- while-loop off/on state
    p = 5                       # p for pages -- the quantity of URLs to open before being prompted for more

    
    print "Finding URL(s)..."
    fileFinder()

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
            
            # open only p (preset as 5) URLs at a time in the default browser (as new tabs) to not clog up the system
            # change p to any number of URLs you'd like to load before being prompted for more p-amount of URLs to open.
            if (i % p == 0 & p != 0):
                k = 1

                # error-checking needs to be improved later
                while (k == 1):
                    more = raw_input(str(i) + '/' + str(_j) + ' URLs opened. Open up more? (y/n): ')
                    if(more == 'y'): k = 0;
                    if(more == 'n'): i = _j; k = 0;

        if (i == _j):
            print "Run completed."

# change to or make a folder, then run the main function
folderMaker()
main()
