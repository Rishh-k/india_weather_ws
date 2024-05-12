import requests
import pandas as pd
from bs4 import BeautifulSoup
import unidecode
from datetime import date
import datetime

def scrape_weather():

    url = "https://www.timeanddate.com/weather/india"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")#.encode("utf-8")
    
    weather_table = soup.find('table', class_ ="zebra fw tb-wt zebra va-m")
    
    return weather_table

def get_data(table):  
    
    conditions = table.find_all('img')
    place_temp = table.find_all('td')
    
    location_det = [location.text.strip() for location in place_temp]
    location_det = location_det[:-4]
    
    details_sort = []
    
    for i in range(0,len(location_det),4):
        loc_det = location_det[i:i+4]
        loc_det.pop(1)
        loc_det.pop(1)
        loc_det[1] = unidecode.unidecode(loc_det[1])
        details_sort.append(loc_det)
        
    for i in range(len(conditions)):
        details_sort[i].append(conditions[i].attrs["title"])
    
    return details_sort

def dict_to_xls(data):
    
    df = pd.DataFrame(data, columns=['Location', 'Temp', 'Weather conditions'])
    df.reset_index(drop=True, inplace=True)
    df = df.sort_values('Location')
    
    today = date.today() 
    time = datetime.datetime.now()

    timestamp = str(today.day)+"-"+str(today.month)+"-"+str(today.year)+"_"+str(time.hour)+"_"+str(time.minute)+"_"+str(time.second)
    fname = timestamp + "_weather_data.xlsx"
    df.to_excel(fname, index=False)


if __name__ == "__main__":
    Weather_table = scrape_weather()
    cleaned_data = get_data(Weather_table)
    dict_to_xls(cleaned_data)