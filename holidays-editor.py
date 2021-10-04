import holidays
from datetime import date
from datetime import datetime
import requests

holidays_list = holidays.load('holidays_store.json')
changes = False

#Decorator
def del_message(func):
    def inner(ref):
        func(ref)
        print(f'\nSuccess\n'
              f'{ref.name} has been removed from the list.\n')
    return inner

@del_message
def delete_entry(holiday):
    try:
        holidays_list.remove(holiday)
        return True
    except:
        return False

def get_forecasts():
    weather_response = requests.get('https://api.weather.gov/gridpoints/MPX/113,70/forecast',
                                    headers={'Accept': 'application/ld+json'})
    weather_dicts = weather_response.json()
    forecasts = {}
    for weather_dict in weather_dicts['periods']:
        if weather_dict['isDaytime']:
            date = datetime.fromisoformat(weather_dict['startTime']).date().isoformat()
            forecast = weather_dict['shortForecast']
            forecasts[date] = forecast
    return forecasts

print(f'Holiday Management\n'
      f'==================\n'
      f'There are {len(holidays_list)} holidays stored in the system.\n')

def add_holiday():
    print('\nAdd a Holiday\n'
          '=============')
    name = input('Holiday Name (c to cancel): ').strip()
    if name == 'c':
        print('\nCancelling holiday addition.\n')
    else:
        while True:
            date = input(f'Date for {name} (YYYY-MM-DD) (c to cancel): ')
            if date == 'c':
                print('\nCancelling holiday addition.\n')
                break
            try:
                datetime.fromisoformat(date)
                holiday = holidays.Holiday(name, date)
                if holiday in holidays_list:
                    print('\nError:\n'
                          'Holiday already in list.\n')
                else:
                    holidays_list.append(holiday)
                    print('\nSuccess:\n'
                          f'{holiday} has been added to the holiday list.\n')
                    global changes
                    changes = True
                break
            except:
                print('\nError:\n'
                      'Invalid date. Please try again.\n')

def remove_holiday():
    print('\nRemove a Holiday\n'
            '================')
    while True:
        name = input('Holiday Name (c to cancel): ').strip()
        if name == 'c':
            print('\nCancelling holiday removal.\n')
            break
        date = input('Year (YYYY-MM-DD) (c to cancel): ').strip()
        if date == 'c':
            print('\nCancelling holiday removal.\n')
            break
        for holiday in holidays_list:
            if holiday.name == name and str(holiday.date) == date:
                delete_entry(holiday)
                global changes
                changes = True
                break
        else:
            print('\nError:\n'
                f'{name} ({date}) not found.\n')
            continue
        break

def save_holidays():
    print('\nSaving Holiday List\n'
          '===================')
    global changes
    if changes:
        while True:
            selection = input('Are you sure you want to save your changes? [y/n]: ').strip().lower()
            if selection == 'y':
                holidays.save(holidays_list)
                changes = False
                print('\nSuccess:\n'
                    'Your changes have been saved.\n')
                break
            elif selection == 'n':
                print('\nCanceled:\n'
                    'Holiday list file save canceled.\n')
                break
            else:
                print('\nError:\n'
                    'Invalid selection. Please try again.\n')
    else:
        print('No changes to be saved.\n')

def view_holidays():
    print('\nView Holidays\n'
          '=============')
    year = input('Which year?: ')
    week = input('Which week? #[1-52, Leave blank for the current week]: ')
    if week == '':
        week = str(date.today().isocalendar()[1])
    weather = False
    if year == str(date.today().isocalendar()[0]) and week == str(date.today().isocalendar()[1]):
        while True:
            selection = input("Would you like to see this week's weather? [y/n]: ").strip().lower()
            if selection == 'y':
                weather = True
                break
            elif selection == 'n':
                break
            else:
                print('\nError:\n'
                      'Invalid selection. Please try again.\n')
    forecasts = get_forecasts()
    out = ''
    if weather:
        for holiday in holidays_list:
            if ((holiday.date - date.today()).days >= 0 
                and (holiday.date - date.today()).days < 6):
                out += f'{holiday} - {forecasts[holiday.date.isoformat()]}\n'
        if len(out) == 0:
            print(f'\nNo holidays found for {year} week #{week}\n')
        else:
            print(f'\nThese are the holidays for this week:')
            print(out)
    else:    
        out = list(filter(lambda x: str(x.date.isocalendar()[0:2]) == f'({year}, {week})', holidays_list))
        if len(out) == 0:
            print(f'\nNo holidays found for {year} week #{week}\n')
        else:
            print(f'\nThese are the holidays for {year} week #{week}:')
            for holiday in out:
                print(holiday)
            print()

def exit():
    while True:
        print('\nExit\n'
              '====')
        if changes:
            print('Your changes will be lost.')
        selection = input('Are you sure you want to exit? [y/n]: ').strip().lower()
        if selection == 'y':
            print()
            return True
        elif selection == 'n':
            print()
            return False
        else:
            print('\nError:\n'
                  'Invalid selection. Please try again.')

while True:
    while True:
        print('Holiday Menu\n'
              '============\n'
              '1. Add a Holiday\n'
              '2. Remove a Holiday\n'
              '3. Save Holiday List\n'
              '4. View Holidays\n'
              '5. Exit\n')
        selection = input().strip()
        if not selection.isdecimal() or int(selection) not in range(1,6):
            print('\nError:\n'
                  'Invalid selection. Please try again.\n')
        else:
            selection = int(selection)
            break
    
    if selection == 1:
        add_holiday()
    elif selection == 2:
        remove_holiday()
    elif selection == 3:
        save_holidays()
    elif selection == 4:
        view_holidays()
    else:
        if exit():
            print('Goodbye!')
            break