import requests
from bs4 import BeautifulSoup
import pandas as pd

# function to Extract the Html from indeed
def Extract(position,Location,page):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    #position = Job Name(Leave it empty for any position)     Location == city(Leave it empty for any location)
    url = f'https://www.indeed.com/jobs?q={position}&l={Location}&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content,'html.parser')
    return soup
# function to transform the html we extracted into data
def Transform(soup):
    divs = soup.find_all('div', {'class': 'job_seen_beacon'}) #locating tags and classes.(Jobs,Salaries...)
    for div in divs :
        try:
            company = div.find('span', {'class': 'companyName'}).text.strip() # Extracting company name
        except:
            company= ''

        try:
            job_title = div.find('h2', attrs={'class':'jobTitle'}).text.strip() # Extracting Job Title
        except:
            job_title = ''

        try:
            salary = div.find('div', {'class': ['attribute_snippet', 'estimated-salary']}).text.strip() # extracting salary
        except:
            salary = ''

        try:
            location = div.find('div', {'class': 'companyLocation'}).text.strip() # extracting location
        except:
            location = ''

        try:
            rating = div.find('span', attrs={'class': 'ratingNumber'}).text.strip() # Extracting rating
        except:
            rating = ''

        try:
            summary = div.find('div', attrs={'class': 'job-snippet'}).text.strip() #Extracting summary
        except:
            summary = ''
        # grab the results and putting it into a dictionary
        job = {
            'job title': job_title,
            'Company' : company,
            'Location' : location,
            'salary ' : salary,
            'rating' : rating,
            'summary' : summary
        }
        joblist.append(job) # appending the data to a list to iterate through it
    return


joblist = []
number_page = 60 #first page == 0 , second == 10 ....... 60 means 6 pages
#You can use as many pages you want, Or use a "while loop" instead ,to see it to the end...
for i in range (0,number_page,10):
    print(f"Getting pages: {i}")
    c = Extract('data science', '', 0)
    Transform(c)
print(len(joblist))

#Creating a dataframe from the results
df = pd.DataFrame(joblist)
df.to_csv('job_csv') # creating a csv file with the data extracted