import requests
import pandas as pd
from bs4 import BeautifulSoup
import pymysql
from sqlalchemy import create_engine
import re


def link_extractor():
    url = "https://ecc.uic.edu/events-2/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    all_events = []
    for post in soup.find_all("a"):
        if 'https://ecc.uic.edu/events/' in str(post):
                post = str(post)
                start = post.find('"')
                stop = post.find('"',start+1)
                link = post[start+1:stop]
                all_events.append(link)
                 
    return all_events
            

def main_crawler():
    
    a = link_extractor()
    database = pd.DataFrame(columns = ['Name','Day','Time', 'Location','Description','Category','Contact-Name','Contact-Phone','Contact-Email', 'Link']) 
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    for i in a:
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        page = requests.get(i, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        data = soup.find("div", attrs={"class": "l-content"})
        data = str(data)
        start_name = data.find('_name">')
        stop_name = data.find('</h1>',start_name + 7)
        name = data[start_name+7:stop_name]
        start_day = data.find('event-date">')
        stop_day = data.find('</p>',start_day + 12)
        day = data[start_day+12:stop_day]
        day = day.strip()
        start_time = data.find('event-time">')
        stop_time = data.find('</p>',start_time + 12)
        time = data[start_time+12:stop_time]
        time = time.strip()
        start_location = data.find('Location</h2>')
        stop_location = data.find('</p>',start_location + 34)
        location = data[start_location+34:stop_location]
        start_address = data.find('Address</h2>')
        stop_address = data.find('</p>',start_address + 34)
        address = data[start_address+34:stop_address]
        address = address.replace('\n','')
        start_des = data.find('class="_description u-rich-text"')
        stop_des = data.find('</div>',start_des + 37)
        Description = data[start_des+37:stop_des]
        Description = re.sub(cleanr, '', Description)
        start_contactname = data.find('_contact-name">')
        stop_contactname = data.find('</div>',start_contactname + 15)
        contactname = data[start_contactname+15:stop_contactname]
        start_contactphone = data.find('_contact-phone">')
        start_contactphone1 = data.find('">',start_contactphone + 16)
        stop_contactphone = data.find('</a>',start_contactphone1 + 2)
        contactphone = data[start_contactphone1+2:stop_contactphone]
        start_contactemail = data.find('_contact-email">')
        start_contactemail1 = data.find('">',start_contactemail + 16)
        stop_contactemail = data.find('</a>',start_contactemail1 + 2)
        contactemail = data[start_contactemail1+2:stop_contactemail]

            
        events = {'Name':name, 'Day':day, 'Time':time, 'Location':location,'Description': Description,'Category':'','Contact-Name' :contactname,'Contact-Phone': contactphone,'Contact-Email':contactemail, 'Link': i}
        
        database.loc[len(database)] = events
        
    return database
    
     
Data = main_crawler()    




#mydb = create_engine('mysql+pymysql://' + user + ':' + passw + '@' + host + ':' + str(port) + '/' + database , echo=False)

#Data.to_sql(con=mydb, name='Events_ECE', if_exists='replace')


