import json
from datetime import date

class Holiday(object):
    '''Holiday Class'''
    def __init__(self, name, in_date):
        self.__name = name
        self.__date = date.fromisoformat(in_date)

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return f'{self.name} ({self.date})'

    @property
    def name(self):
        return self.__name

    @property
    def date(self):
        return self.__date

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @date.setter
    def date(self, new_date):
        self.__date = new_date

    def to_dict(self):
        return {'name': self.name, 'date': self.date.isoformat()}

def load(holidays_json):
    holidays_list = []

    with open(holidays_json) as jsonfile:
        holidays_in = json.load(jsonfile)
        for holiday_in in holidays_in['holidays']:
            holiday = Holiday(holiday_in['name'], holiday_in['date'])
            holidays_list.append(holiday)

    return holidays_list

def save(holidays_list):
    holidays = {'holidays': []}
    for holiday in holidays_list:
        holidays['holidays'].append(holiday.to_dict())
    
    with open('holidays_store.json', 'w') as jsonfile:
        json.dump(holidays, jsonfile, indent = 4)