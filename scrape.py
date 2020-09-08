import requests
from bs4 import BeautifulSoup
from difflib import get_close_matches
from selenium import webdriver
import pandas as pd
import time

#decode emails function
def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email


names = []
barnums = []
emails = []
officephones = []
cellphones = []
addresses = []
phones = []
test = []

for i in range(1,1791):
    
    page_number = str(i)

    response = requests.get('https://www.floridabar.org/directories/find-mbr/?lName=&sdx=N&fName=&eligible=Y&deceased=N&firm=&locValue=United+States&locType=N&pracAreas=&lawSchool=&services=&langs=&certValue=&pageNumber='+page_number+'&pageSize=50')
    time.sleep(2)
    soup = BeautifulSoup(response.text, 'html.parser')

    id_contents = soup.findAll('div',{'class':'profile-identity'})
    contact_contents = soup.findAll('div',{'class':'profile-contact'})
    #get names
    for i in id_contents:
        name = i.find('div',{'class':'profile-content'})
        name = name.find('p',{'class':'profile-name'})
        name = name.text 
        names.append(name)
    # get bar numbers 
    for i in id_contents:
        num = i.find('div',{'class':'profile-content'})
        num = num.find('p',{'class':'profile-bar-number'})
        num = num.text 
        num = num.split('#')[-1]
        barnums.append(num)
    #get emails
    for i in contact_contents:
        ele = i.find('a',{'class':'icon-email'})
        try:
            email = ele.get('href')
            email = email.split('/')[3].split('#')[1]
            email = cfDecodeEmail(email)
            emails.append(email)
        except:
            emails.append(ele)

    #get raw address data
    for i in contact_contents:
        ad = i.findAll('p')[0]
        ad = [str(i) for i in ad]
        addresses.append(ad)

    #get raw phone number data
    for i in contact_contents:
        
        leg = i.findAll('p')
        try:
            leg2 = i.findAll('p')[1].text
            # ele2 = ele.findAll('a')[:2]
            phones.append(leg2)
        except:
            phones.append(leg[0])
    
    #to track progress
    print(page_number)
  

atr_list = ['Name', 'Email', 'Address', 'Bar Number', 'Phone Numbers']
 
table = pd.DataFrame(list(zip(names, emails, addresses, barnums, phones)), columns=atr_list)

table.to_csv('raw_data.csv')

print('finished succesfuly')