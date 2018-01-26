from BeautifulSoup import BeautifulSoup
import os

MESSAGES_DIRECTORY = './data/facebook-eswardhinak/messages/'
for filename in os.listdir(MESSAGES_DIRECTORY):
	if filename.endswith('.html'):
		currentFile = open(MESSAGES_DIRECTORY + filename)
		soup = BeautifulSoup(currentFile.read())

		conversationHeaderTag = soup.html.head.title
		if (conversationHeaderTag.string.endswith('Sharon Yeh')):
			print filename