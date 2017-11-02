from bs4 import BeautifulSoup
import re
import urllib2
from operator import itemgetter
import time
import sys
import requests
import os
global restaurants

newpath = r'TripAdv'
if not os.path.exists(newpath):
	os.makedirs(newpath)

response = requests.get('https://www.tripadvisor.com/RestaurantSearch-g60713-oa0-San_Francisco_California.html#EATERY_OVERVIEW_BOX')
a = response.text 				#Only the first page of restaurants
soup = BeautifulSoup(a, 'lxml')
restaurants = soup.findAll('a', {'class': re.compile('property_title')})

for p in range(1,5):			#Second page and ahead
	pagelink = 'https://www.tripadvisor.com/RestaurantSearch-g60713-oa'+str(p*30)+'-San_Francisco_California.html#EATERY_OVERVIEW_BOX'
	response = requests.get(pagelink)
	html = response.text
	soup = BeautifulSoup(html, "lxml")
	rest = soup.findAll('a', {'class': re.compile('property_title')})
	restaurants += rest
# print len(restaurants)			#Total Number of Restaurants
g = open('TripAdv/RestaurantList.txt','a')
for i in range(100):
	res = restaurants[i].contents[0]
	res = res.strip()
	f=open('TripAdv/'+str(res)+'.txt','w')
	print str(i)+str(res) + ":\n"				#Name of Restaurants
	g.write(str(res)+"\n")
	link = 'https://www.tripadvisor.com' + restaurants[i].get('href')
	response = requests.get(link)
	ResContent = response.text
	revsoup = BeautifulSoup(ResContent, "lxml")
	page = revsoup.find('span',{'class':'pageNum last taLnk '})
	finalpage = int(page.string)
	if finalpage >= 10:
		finalpage = 10
	for p2 in range(finalpage):
		if p2==0:
			revs = revsoup.findAll('a',{'href':re.compile('/ShowUserReviews')})
			for r in revs:
				title_review = re.findall(r'<span class="noQuotes">(.*?)</span>',str(r))
				print(title_review)
				try:
					f.write(title_review[0]+"\n")
				except IndexError:
					print ""
				link_rev = 'https://www.tripadvisor.com/' + r.get('href')
				response = requests.get(link_rev)
				Webcontent_rev = response.text
				reviewPage = BeautifulSoup(Webcontent_rev, "lxml")
				rating = reviewPage.findAll('span',{'class':re.compile('ui_bubble_rating')})    #Scrapping rating from the review
				reviewRating = rating[0].get('alt')
				f.write("Rating: ")
				#print(reviewRating)
				j=0
				while (reviewRating[j] != ' '):
					#print('while')
					f.write(reviewRating[j])             #Writing Rating in file
					j = j + 1
				f.write("\n")
				f.write("Date: ")
				date = reviewPage.findAll('span',{'class':re.compile('ratingDate')})      #Scrapping date
				try:
					reviewDate = date[0].get('title')
					#print(reviewDate)
					f.write(reviewDate)                                            #Writing Date to the file
					f.write("\n")
				except Exception as e:
					p = re.compile(r'<.*?>')
					datetest = p.sub('',str(date[0]))
					dateTest = datetest.replace("Reviewed ","")
					#print(dateTest)

					f.write(dateTest)
					f.write("\n")
				review_content = reviewPage.findAll('div',{'class':'entry'})             #Finding Review content
				for div in review_content:
					elem = div.find('p')
					if elem:
						#print(elem.text)
						try:
							f.write(elem.text)
						except UnicodeEncodeError:
							print("123")
						f.write("\n\n")
						break
		else:
			#print ("heelo")
			link = link + '#REVIEWS'                                                          #To create link to Navigate in review pages
			#print (link)
			first = re.findall(r'(.*?)Reviews',str(link))
			last = re.findall(r'Reviews(.*?)REVIEWS',str(link))
			#print (first)
			#print (last)
			finalLink = first[0]+'Reviews-or'+str(p2*10)+last[0]+'REVIEWS'                  #To create link to Navigate in review pages
			response = requests.get(finalLink)
			Webcontent_rev = response.text
			reviewPage = BeautifulSoup(Webcontent_rev, "lxml")
			revs = reviewPage.findAll('a',{'href':re.compile('/ShowUserReviews')})
			for r in revs:
				title_review = re.findall(r'<span class="noQuotes">(.*?)</span>',str(r))
				print(title_review)
				try:
					f.write(title_review[0]+"\n")
				except IndexError:
					print ""
				link_rev = 'https://www.tripadvisor.com/' + r.get('href')
				response = requests.get(link_rev)
				Webcontent_rev = response.text
				reviewPage = BeautifulSoup(Webcontent_rev, "lxml")
				rating=reviewPage.findAll('span',{'class':re.compile('ui_bubble_rating')})    #Scrapping rating from the review
				reviewRating=rating[0].get('alt')
				f.write("Rating: ")
				#print(reviewRating)
				j=0
				while (reviewRating[j] != ' '):
					#print('while')
					f.write(reviewRating[j])             #Writing Rating in file
					j = j + 1
				f.write("\n")
				f.write("Date: ")
				date = reviewPage.findAll('span',{'class':re.compile('ratingDate')})      #Scrapping date
				try:
					reviewDate = date[0].get('title')
					#print(reviewDate)
					f.write(reviewDate)                                            #Writing Date to the file
					f.write("\n")
				except Exception as e:
					p = re.compile(r'<.*?>')
					datetest = p.sub('',str(date[0]))
					dateTest = datetest.replace("Reviewed ","")
					#print(dateTest)

					f.write(dateTest)
					f.write("\n")
				review_content = reviewPage.findAll('div',{'class':'entry'})             #Finding Review content
				for div in review_content:
					elem = div.find('p')
					if elem:
						#print(elem.text)
						try:
							f.write(elem.text)
						except UnicodeEncodeError:
							print("123")
						f.write("\n\n")
						break
	f.close()