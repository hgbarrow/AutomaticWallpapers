#coding: utf8

# Automatic Wallpapers by Henry Barrow - 9/20/2015
# Downloads the first N pages of InterfaceLIFT wallpapers to a local folder
# Choose this folder as a slideshow in desktop settings and use Windows Schuduler
# to run the script periodically

from bs4 import BeautifulSoup
from urllib2 import urlopen
import os, textwrap
import imgwrite

BASE_URL = "https://interfacelift.com"
url = 'https://interfacelift.com/wallpaper/downloads/date/wide_16:9/1920x1080/'
pages = 8 # Number of pages to scrape
max_files = 80 # Maximum number of files to store on drive
writeOn = True # Print info on image

def make_soup(url):
	html = urlopen(url).read()
	return BeautifulSoup(html, 'html.parser')
	
def get_img_data(url):
	soup = make_soup(url)
	elems = soup.select(".item")
	image_data = []
	for elem in elems:
		title = unicode(elem.h1.text)
		dl = elem.select('.download')[0]
		link = BASE_URL + dl.a.get('href')
		by = unicode('by ') + elem.select('.details')[0].find_all('a')[1].text
		text = elem.find('p').text
		lines = textwrap.wrap(text, width = 100, break_long_words = False)
		text = '\n'.join(lines)
		text = '\n'.join([by, text])
		picinfo = [title, text, link]
		image_data.append(picinfo)		
	return image_data

	
try:
	os.chdir(os.getcwd() + "\wallpapers")
	
except OSError as e:
	os.makedirs(os.getcwd() + "\wallpapers")
	os.chdir(os.getcwd() + "\wallpapers")

data = []
for i in range(1, pages + 1):
	data += get_img_data(url + unicode('index') + unicode(i))

for set in data:
	link = set[2]
	filename = link[link.rfind('/') + 1:]
	try:
		print unicode('\n') + set[0]
	except UnicodeError, e:
		print e
		
	print filename
	if os.path.isfile(filename):
		print "Already Saved"
	else:
		f = open(filename, 'wb')
		f.write(urlopen(link).read())
		f.close()
		
		if writeOn:
			imgwrite.wallpaper(filename, set[0], set[1])
		
files = os.listdir(os.getcwd())
if len(files) > max_files:
	for i in range(0, len(files) - max_files):
		try:
			os.remove(files[i])
		except OSError as e:
			print e