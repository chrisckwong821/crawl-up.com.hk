import csv
import re
import time 
import requests
import pandas as pd 
from bs4 import BeautifulSoup

#read in url
df = list(pd.read_csv('sub_domain.csv').sub_domain)
base = "http://www.yp.com.hk"

#parse into html

with open('final_list.csv','w') as csvFile:
	fieldnames = ['Name','Tel','Fax','Email']
	writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
	writer.writeheader()

	count = 0	
	for url in df:
		count += 1
		print(count," page")
		html_doc = requests.get(base + url).text
		soup = BeautifulSoup(html_doc, 'html.parser')

		#get fax 
		bubble = soup.find_all('div',class_='bubblebox_body')
		fax_list = bubble[1::6]

		# no of fax shd equate no of company
		name_resultset = soup.find_all('span', class_="cname")
		if len(fax_list) != len(name_resultset):
			print("no of fax different from no of company")
			break

		#for each search result
		for i,x in enumerate(name_resultset):
			#get company name
			name = x.text
			#in each sub-tag
			if x.find('a'):
				#get href
				href = x.find('a').get('href')
				# match fax no by location
				fax_set = fax_list[i].find('li',class_="info")
				# go into its main page
				response = requests.get(base + href).text
				# get its email
				mail_set = re.search('mailto:([^\s]+)"',response)
				tel_set = re.search('電話([0-9 ]+)',response)

				if mail_set:
					mail = mail_set.group(1)
				else:
					mail = "/"

				if fax_set:
					fax = fax_set.text
					fax = fax[:4] + fax[5:]
				else:
					fax = "/"

				if tel_set:
					tel = tel_set.group(1)
					tel = tel[:4] + tel[5:]
				else:
					tel = "/"
			#for company with name only, no sub-tag <a>	
			else:
				href = "/"

			writer.writerow({'Name':name,
							 'Tel':tel,
							 'Fax':fax,
							 'Email':mail })
			#print(name,tel,fax,mail)
		
	#fax_set = soup.find_all('li', class_="info")





