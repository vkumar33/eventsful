import requests
import pandas as pd
from bs4 import BeautifulSoup
import pymysql
from sqlalchemy import create_engine
import re

# Extracting a list of all the websites
def link_extractor():
    url = "https://arts.uchicago.edu/events/search?tid%5B%5D=1&tid%5B%5D=2&tid%5B%5D=3&tid%5B%5D=192&tid%5B%5D=41&tid%5B%5D=195&tid%5B%5D=42&tid%5B%5D=43&tid%5B%5D=44&tid%5B%5D=214&title=&field_date_time_value%5Bvalue%5D%5Bdate%5D=2019-10-18&field_date_time_value2%5Bvalue%5D%5Bdate%5D=2019-12-31"
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    all_events = []
    page_count = 0
    while page_count < 12:
        for post in soup.find_all("a"):
            if '/event/' in str(post):
                post = str(post)
                start = post.find('"')
                stop = post.find('"',start+1)
                link = post[start+1:stop]
                link = 'https://arts.uchicago.edu' + str(link)
                all_events.append(link)
                
        try:
            next_button = soup.find("div", attrs={"class": "item-list"})
            next_button = str(next_button)
            link_start = next_button.find('href="')
            link_stop = next_button.find('"',link_start+6)
            next_page_link = next_button[link_start+6:link_stop]
            next_page_link = 'https://arts.uchicago.edu' + next_page_link
            
            page = requests.get(next_page_link, headers=headers)
            soup = BeautifulSoup(page.text, 'html.parser')
            page_count += 1
            
        except:
            break
                
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
            
        events = {'Name':name, 'Day':day, 'Time':time, 'Location':location, 
                  'Description': Description,'Category':Category,'Contact':contactemail, 'Link': i}
        
        database.loc[len(database)] = events
        
    return database
    
     
Data = main_crawler()    
Data1 = Data.drop_duplicates(['Name'],keep='last')



#mydb = create_engine('mysql+pymysql://' + user + ':' + passw + '@' + host + ':' + str(port) + '/' + database +'?charset=utf8mb4')


#Data1.to_csv('test.csv')
#(Data1.iloc[:24,:]).to_sql(con=mydb, name='Events_UChicago', if_exists='replace')



