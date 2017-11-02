from bs4 import BeautifulSoup
import re
import urllib2
from operator import itemgetter
import time
import sys
import requests
import os

def run(url):
	print url

	for i in range(5):
		try:
			response = requests.get(url)
			html=response.content
			break
		except Exception as e:
			print 'failed attempt',i
			time.sleep(2)
			ss=input("No internet, Enter Anything")
		if not html:
			continue
	soup = BeautifulSoup(html, "lxml") #parse the html
	page_rest = soup.find('div',{'class':'page-of-pages arrange_unit arrange_unit--fill'})              #To find the total page number of reviews for each restaurant to Navigate
	# print page_rest
	pagenum = re.findall(r'Page 1 of (.*)',str(page_rest))                                                 #Pagenum gives the number of page to navigate
	print pagenum
	if pagenum :
		for p in range(5):
			if p==0:
				print 'first'
				pageLink = url
			else:
				pageLink = url+'?start='+str(p*20)
			for i in range(5):
				try:
					response = requests.get(pageLink)
					html = response.content
					break
				except Exception as e:
					print 'failed attempt',i
					time.sleep(2)
					ss=input("No internet, Enter Anything")
				if not html:continue # couldnt get the page, ignore
			revsoup = BeautifulSoup(html, "lxml")# parse the html
			#print revsoup
			review_content = revsoup.findAll('div',{'class': 'review-content'})        #Find review content with rating and date
			#print review_content
			for div in review_content:
				review_rating = review_content[0].find('img',{'class': 'offscreen'})
				rating_soup = BeautifulSoup(str(review_rating), "lxml")
				rating = rating_soup.img['alt'].split()[0]
				print rating
				f.write("Rating: "+rating+"\n")
				"""review_date=revsoup.findAll('span',{'class':re.compile('rating-qualifier')})
				date=str(review_date[0])
				d1=re.findall(r'class="rating-qualifier"> (.*)',str(date))
				print d1"""
				date = div.find('span')                                           #Scrapping date from review content
				if date:
					# print date.text.strip()
					f.write("Date: "+date.text.strip()+"\n")                                 #Writing date to the file
				elem = div.find('p')                                              #Scrappng review text from review content
				if elem:
					# print elem.text
					try:
						f.write(elem.text + "\n\n")                                         #Writting review Text to the file
					except UnicodeEncodeError:
						print "123"
	f.close()                                                                 #Closing file


if __name__=='__main__':
	newpath = r'Yelp'                                   #Creating folder for elp to store the restaurant reviews
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	path = 'TripAdv/RestaurantList.txt'    #Reading the file from which the restaurants names are taken to search in Yelp and Scrape the reviews
	fin = open(path)
	for line in fin:
		words = line.lower().strip()
		restaurant_name = words
		print restaurant_name
		f = open('Yelp/'+str(restaurant_name)+'.txt','w')      #New file Created by Restaurant name to store the reviews
		restaurant_name = str(restaurant_name).replace(" ","-")
		restaurant_name = str(restaurant_name).replace("'","")
		restaurant_name = str(restaurant_name).replace("&","and")
		url='https://www.yelp.com/biz/'+restaurant_name+'-san-francisco'           #Creating URL for restaurant
		#url='https://www.yelp.com/search?find_desc=Restaurants&find_loc=San+Francisco%2C+CA&ns=1'
		run(url)