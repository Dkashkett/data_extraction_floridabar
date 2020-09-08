import pandas as pd 
import numpy as np 
import re
from bs4 import BeautifulSoup

#read csv
filenames=['part1.csv','part2.csv','part3.csv']
master = pd.concat([pd.read_csv(f) for f in filenames])
master = master.reset_index()

firstnames = master.Name.apply(lambda x: x.split()[0])
lastnames = master.Name.apply(lambda x: x.split()[-1])
middlenames = master.Name.apply(lambda x: x.split()[1] if len(x.split())>2 else None)
emails = master.Email

#phone number extraction
nums = list(master['Phone Numbers'])
nums_ = []
for i in nums:
    s = str(''.join(i))
    s = s.strip()
    s = s.split(':')
    s = [i.split() for i in s]
    s = sum(s,[])
    nums_.append(s)

nums = nums_

office = [None for i in range(len(nums))]
cell = [None for i in range(len(nums))]
for i in range(len(nums)):
    for j in range(len(nums[i])):
        if nums[i][j] == 'Office':
            office[i] = nums[i][j+1]
        elif nums[i][j] == 'Cell':
            cell[i] = nums[i][j+1]
        else:
            pass

#address cleaning
adds =  master['Address'].apply(lambda x: (x.split(',')[-2:]))
for i in adds:
    for j in i:
        j = j.strip()
        j = j.replace('\'','')

st = [i[-1] for i in adds]
s = ['IA', 'KS', 'UT', 'VA', 'NC', 'NE', 'SD', 'AL', 'ID', 'FM', 'DE', 'AK', 'CT', 'PR', 'NM', 'MS', 'PW', 'CO', 'NJ', 'FL', 'MN', 'VI', 'NV', 'AZ', 'WI', 'ND', 'PA', 'OK', 'KY', 'RI', 'NH', 'MO', 'ME', 'VT', 'GA', 'GU', 'AS', 'NY', 'CA', 'HI', 'IL', 'TN', 'MA', 'OH', 'MD', 'MI', 'WY', 'WA', 'OR', 'MH', 'SC', 'IN', 'LA', 'MP', 'DC', 'MT', 'AR', 'WV', 'TX']
rpat = re.compile(r'\b(' + '|'.join(s) + r')\b', re.IGNORECASE)

sts = [re.findall(rpat,i) for i in st]
states = []
for i in sts:
    if i == []:
        states.append(None)
    else:
        states.append(i[0])

c = [i[0] for i in adds]
cities = [i.replace("'",'').strip() for i in c]


barnums = master['Bar Number']
attrs = [
    firstnames,
    lastnames,
    middlenames,
    emails,
    office,
    cell,
    cities,
    states,
    barnums,
]
column_names = [
    'First',
    'Last',
    'Middle',
    'Email',
    'Office Phone',
    'Cell Phone',
    'City',
    'State',
    'Bar Number'
]

table = pd.DataFrame(list(zip(firstnames,
    lastnames,
    middlenames,
    emails,
    office,
    cell,
    cities,
    states,
    barnums,)), columns=column_names)

table.to_csv('florida_bar_scrape.csv')

















