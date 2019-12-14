import requests
import pandas as pd
from bs4 import BeautifulSoup
import pymysql
from sqlalchemy import create_engine
import re


def link_extractor():
    url = "https://today.uic.edu/events"
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    all_events = []
    page_count = 0
    while page_count < 12:
        for post in soup.find_all("a"):
            if 'https://today.uic.edu/events/' in str(post):
                if 'https://today.uic.edu/events/categories' not in str(post):
                    post = str(post)
                    start = post.find('"')
                    stop = post.find('"',start+1)
                    link = post[start+1:stop]
                    all_events.append(link)
        
        try:
            next_button = soup.find("a", class_="next page-numbers")
            next_button = str(next_button)
            link_start = next_button.find('href="')
            link_stop = next_button.find('"',link_start+6)
            next_page_link = next_button[link_start+6:link_stop]
            next_page_link = 'https://today.uic.edu' + next_page_link
            
            page = requests.get(next_page_link, headers=headers)
            soup = BeautifulSoup(page.text, 'html.parser')
            page_count += 1
            
        except:
            break
                
    return all_events
            

def main_crawler():
    
    a = link_extractor()
    database = pd.DataFrame(columns = ['Name','Day','Time', 'Location', 'Description','Category', 'Link']) 
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    
    for i in a:
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        page = requests.get(i, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        data = soup.find("div", attrs={"id": "content"})
        data = str(data)
        start_name = data.find('<h1>')
        stop_name = data.find('</h1>',start_name + 4)
        name = data[start_name+4:stop_name]
        start_day = data.find('event-date">')
        stop_day = data.find('</p>',start_day + 12)
        day = data[start_day+12:stop_day]
        start_time = data.find('event-time">')
        stop_time = data.find('</p>',start_time + 12)
        time = data[start_time+12:stop_time]
        start_location = data.find('href="')
        stop_location = data.find('">',start_location + 6)
        location = data[start_location+6:stop_location]
        start_des = data.find('event_description">')
        stop_des = data.find('</p>',start_des + 23)
        Description = data[start_des+23:stop_des]
        Description = re.sub(cleanr, '', Description)
        start_cat = data.find('event-categories">')
        start_cat1 = data.find('">',start_cat + 18)
        stop_cat = data.find('</a>',start_cat1 + 2)
        Category = data[start_cat1+2:stop_cat]
            
        events = {'Name':name, 'Day':day, 'Time':time, 'Location':location, 'Description': Description,'Category':Category, 'Link': i}
        
        database.loc[len(database)] = events
        
    return database
    
     
Data = main_crawler()    





#mydb = create_engine('mysql+pymysql://' + user + ':' + passw + '@' + host + ':' + str(port) + '/' + database , echo=False)

#Data.to_sql(con=mydb, name='Events_UIC', if_exists='replace')
