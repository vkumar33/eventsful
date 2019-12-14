import requests
import pandas as pd
from bs4 import BeautifulSoup
import pymysql
from sqlalchemy import create_engine
import re

# Extracting a list of all the websites
def link_extractor():
    url = "https://www.uchicago.edu/students/events/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    all_events = []

    for post in soup.find_all("a"):
        post = str(post)
        start = post.find('"')
        stop = post.find('"',start+1)
        link = post[start+1:stop]
        all_events.append(link)
                
    return all_events
            
# Individually crawling all the websites and extracting the necessary information
def main_crawler():
    
    a = link_extractor()
    database = pd.DataFrame(columns = ['Name','Day','Time', 'Location', 'Description','Category','Contact' ,'Link']) 
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    
    for i in a:
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        page = requests.get(i, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        data = soup.find("div", attrs={"id": "main"})
        data = str(data)
        data_content = soup.find("div", attrs={"class": "content-body"})
        data_content = str(data_content)
        start_name = data.find('page-title">')
        stop_name = data.find('</h1>',start_name + 12)
        name = data[start_name+12:stop_name]
        start_day = data_content.find('date-display-single">')
        stop_day = data_content.find('<br/>',start_day + 21)
        day = data_content[start_day+21:stop_day]
        start_time = data_content.find('<br/>',start_day + 21)
        stop_time = data_content.find('</span>',start_time + 5)
        time = data_content[start_time+5:stop_time]
        start_location = data_content.find('Location</h2>')
        stop_location = data_content.find('</p>',start_location + 17)
        location = data_content[start_location+17:stop_location]
        start_cat = data_content.find('Contact')
        stop_cat = data_content.find('<br/>',start_cat + 16)
        Category = data_content[start_cat+16:stop_cat]
        start_contactemail = data_content.find('">',stop_cat)
        stop_contactemail = data_content.find('</a>',start_contactemail + 2)
        contactemail = data_content[start_contactemail+2:stop_contactemail]
        start_des = data_content.find('Description</h2>')
        Description = data_content[start_des+16:-1]
        Description = re.sub(cleanr, '', Description)
        Description = Description.replace('\n','')
            
        events = {'Name':name, 'Day':day, 'Time':time, 'Location':location, 'Description': Description,'Category':Category,'Contact':contactemail, 'Link': i}
        
        database.loc[len(database)] = events
        
    return database
    
     
Data = main_crawler()    




#mydb = create_engine('mysql+pymysql://' + user + ':' + passw + '@' + host + ':' + str(port) + '/' + database , echo=False)

#Data.to_sql(con=mydb, name='Events_UC', if_exists='replace')


            