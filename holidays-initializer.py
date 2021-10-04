import json
from bs4 import BeautifulSoup
import requests
import holidays

months = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}

holidays_list = holidays.load('holidays.json')

def getHTML(url):
    try:
        response = requests.get(url)
        return response.text
    except:
        return False

for year in range(2020, 2025):
    html = getHTML(f'https://www.timeanddate.com/holidays/us/{year}')
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', attrs = {'id':'holidays-table'})
    for row in table.find('tbody').find_all_next('tr'):
        name = row.find('a')
        if name is not None:
            name = name.string
            month_day = row.find('th')
            if month_day is not None:
                month = months[month_day.string.split(' ')[0]]
                day = int(month_day.string.split(' ')[1])
                date = f"{year}-{month:02}-{day:02}"
                holiday = holidays.Holiday(name, date)
                if holiday not in holidays_list:
                    holidays_list.append(holiday)

holidays.save(holidays_list)