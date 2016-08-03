# stringparser.py
#
# Ronald Rihoo

def findFirstQuotationMarkFromTheLeft(string):
	for i in xrange(len(string) - 1, 0, -1):
		if string[i] == '"':
			return i

def findFirstQuotationMarkFromTheRight(string):
	for i in range(len(string)):
		if string[i] == '"':
			return i

def splitLeftAspect_toChar(string, fromIndex, char):
	string = string[0:fromIndex]
	for i in xrange(len(string) - 1, 0, -1):
		if string[i] == char:
			return string[i:].replace("\\", "")

def splitRightAspect_toChar(string, fromIndex, char):
	string = string[fromIndex:]
	for i in xrange(len(string)):
		if string[i] == char:
			return string[:i+1].replace("\\", "")

def splitLeftAspect_toSubstring(string, fromIndex, chars):
	string = string[0:fromIndex]
	l = len(chars)
	for i in xrange(len(string) - 1, 0, -1):
		if i < len(string) - l:
			if string[i:i+l] == chars:
				return string[i:]

def splitRightAspect_toSubstring(string, fromIndex, chars):
	string = string[fromIndex:]
	l = len(chars)
	for i in xrange(len(string)):
		if string[i:i+l] == chars:
			return string[:i+l]

def getFullQuoteViaKeywordLaterals(string, keyword):
	if keyword in string:
		i = string.index(keyword)
		x = splitLeftAspect_toChar(string, i, '"')
		y = splitRightAspect_toChar(string, i, '"')
		try: return x + y
		except: return "No results"

def removeBackslashes(string):
	return string.replace("\\", "")

def getHtmlLinkViaKeywordLaterals(string, keyword):
	if keyword in string:
		i = string.index(keyword)
		y = splitRightAspect_toChar(string, i, '"')
		# if string = ...somewebpage.html"	<- notice double-quotation mark placement
		if (y[len(y)-5:] == '.html'):
			x = splitLeftAspect_toChar(string, i, '"')[1:]
			# expected: string = somecode"somelink...	<- notice double-quotation mark placement
			try: 
				return x + y
			except: 
				# expected: string = somecodehttp://somelink... 	<- notice no double-quotation mark
				try:
					x = splitLeftAspect_toSubstring(string, i, 'http')
					return x + y
				except: 
					return "Not found."
		# if string = ...somewebpage.html > some text ..."	<- notice double-quotation mark placement
		elif (y[:5] == '.html'):
			y = y[:5]
			x = splitLeftAspect_toChar(string, i, '"')
			# expected: string = somecode"somelink... 	<- there exists a double-quotation mark
			try: 
				return x[1:] + y
			except:
				try: 
					# expected: string = somecodehttp://somelink... 	<-  no double-quotation mark
					x = splitLeftAspect_toSubstring(string, i, 'http')
					return x + y
				except: 
					return "Not found."
		else:
			try: 
				x = splitLeftAspect_toSubstring(string, i, 'http')
				y = splitRightAspect_toSubstring(string, i, '.html')
				return x + y
			except:
				return "Not found."
	return