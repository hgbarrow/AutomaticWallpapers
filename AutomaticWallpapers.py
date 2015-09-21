# Automatic Wallpapers by Henry Barrow - 9/20/2015
# Downloads the first N pages of InterfaceLIFT wallpapers to a local folder
# Choose this folder as a slideshow in the desktop settings for best results

from bs4 import BeautifulSoup
from urllib2 import urlopen
import os

BASE_URL = "https://interfacelift.com"
url = 'https://interfacelift.com/wallpaper/downloads/date/wide_16:9/1920x1080/'
pages = 1 # Number of pages to scrape
max_files = 30 # Maximum number of files to store on drive

def make_soup(url):
	html = urlopen(url).read()
	return BeautifulSoup(html, 'lxml')
	
def get_img_links(url):
	soup = make_soup(url)
	links = soup.find_all("a")
	link_out = []
	for link in links:
		link = str(link.get('href'))
		if '.jpg' in link:
			link_out.append(BASE_URL + link)
			
	return link_out

	
try:
	os.chdir(os.getcwd() + "\wallpapers")
	
except OSError as e:
	os.makedirs(os.getcwd() + "\wallpapers")
	os.chdir(os.getcwd() + "\wallpapers")

links = []
for i in range(1, pages + 1):
	links += get_img_links(url + 'index' + str(i))

for link in links:
	filename = link[link.rfind('/') + 1:]
	print filename
	if os.path.isfile(filename):
		print "Already Saved"
	else:
		f = open(filename, 'wb')
		f.write(urlopen(link).read())
		f.close()
		
files = os.listdir(os.getcwd())
print len(files)
if len(files) > max_files:
	for i in range(0, len(files) - max_files):
		try:
			os.remove(files[i])
		except OSError as e:
			print e