from BeautifulSoup import BeautifulSoup
import os
import sys
import matplotlib.dates as dates
import matplotlib.pyplot as plt
from datetime import datetime

def analyzeConversation(soup):
	allTagsList = soup.html.body.div.findAll(recursive=False)
	allCorrectTags = []
	divCounter = 0
	parCounter = 0

	divTags = []
	parTags = []
	lastTagWasDiv = False
	for tag in allTagsList:
		tagAsString = str(tag)
		if (tagAsString.startswith('<div ')):
			lastTagWasDiv = True
			divCounter += 1
			divTags.append(tagAsString)
		if (tagAsString.startswith('<p>')):
			if (lastTagWasDiv):
				parCounter += 1
				parTags.append(tagAsString)
			lastTagWasDiv = False

	print divCounter, parCounter
	print len(divTags), len(parTags)

	userNames = []
	dateList = []
	for div in divTags:
		bsReader = BeautifulSoup(div)
		userName = bsReader.fetch('span', {'class':'user'})[0].string
		userNames.append(userName)
		date = bsReader.fetch('span', {'class':'meta'})[0].string
		dateList.append(date)

	parsedParTags = []
	for par in parTags:
		updatedPar = par[3:-4]
		parsedParTags.append(updatedPar)
	return dateList, userNames, parsedParTags

def getDateNoTimeStamp(date):
	return date.split(' at ')[0]

def getDatesWithNumberOfWords(dateList, messagesList):
	dateToTexts = {}
	for i in range(0, len(dateList)):
		date = dateList[i]
		message = messagesList[i]

		if (date not in dateToTexts):
			dateToTexts[date] = [message]
		else:
			dateToTexts[date].append(message)
	uniqueDates = dateToTexts.keys()
	wordNumbers = []
	for date in dateToTexts:
		currentDaysWords = dateToTexts[date]
		totalMessages = 0
		for message in currentDaysWords:
			totalMessages += len(message.split())
		wordNumbers.append(totalMessages)
	return uniqueDates, wordNumbers

def getDateTimeObject(date):
	datetime_object = datetime.strptime(date, "%A, %B %d, %Y")
	return datetime_object

MESSAGES_DIRECTORY = './data/facebook-eswardhinak/messages/'
for filename in os.listdir(MESSAGES_DIRECTORY):
	currentFile = open(MESSAGES_DIRECTORY + filename)
	soup = BeautifulSoup(currentFile.read())

	conversationHeaderTag = soup.html.head.title
	if (conversationHeaderTag.string.endswith('Aviv Redlich')):
		print filename
		# sys.exit()
		dateList, userNames, parTags = analyzeConversation(soup)
		dateListAscii = list(map(lambda date:date.encode('ascii', 'ignore'), dateList))
		datesNoTimeStampList = list(map(getDateNoTimeStamp, dateListAscii))

		uniqueDates, wordNumbers = getDatesWithNumberOfWords(datesNoTimeStampList, parTags)
		uniqueDateObjects = list(map(getDateTimeObject, uniqueDates))
		uniqueSortedDateObjects, sortedWordCounts = zip(*sorted(zip(uniqueDateObjects, wordNumbers)))

		# print uniqueSortedDateObjects, sortedWordCounts
		matplotlibDates = dates.date2num(uniqueSortedDateObjects)
		plt.plot_date(matplotlibDates, sortedWordCounts, '-o')
		plt.show()
		print "Done"
