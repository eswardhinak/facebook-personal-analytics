from BeautifulSoup import BeautifulSoup
import os
import sys
import plotly

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

	print len(userNames), len(dateList)



MESSAGES_DIRECTORY = './data/facebook-eswardhinak/messages/'
for filename in os.listdir(MESSAGES_DIRECTORY):
	if filename == '1117.html':
		currentFile = open(MESSAGES_DIRECTORY + filename)
		soup = BeautifulSoup(currentFile.read())

		conversationHeaderTag = soup.html.head.title
		print filename
		analyzeConversation(soup)




