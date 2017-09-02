from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve, quote
from urllib.parse import urljoin

start =10000
def download(genres):
	"""
	Genres is a list of genres as strings
	"""
	lowergenres = []
	for genre in genres:
		lowergenres.append(genre.lower())
	print(lowergenres)
	browser = webdriver.Chrome()

	for i in range(start,100000):
		try:
			url ='https://freemidi.org/download-'+str(i)
		
			u = urlopen(url)
			html = u.read().decode('utf-8')
			soup = BeautifulSoup(html)

			for link in soup.select('ol'):
				for genre in lowergenres:
					passed =False 
					if genre in link.getText() and not passed:
						browser.get(url)
						button =browser.find_element_by_id('downloadmidi')
						button.click()
						print('pass')
						passed= True
						print(i)
					print(i)
		except:
			continue

