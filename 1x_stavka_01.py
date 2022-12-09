from telethon import TelegramClient, events, sync, connection
import pygame
import requests
import time
import os


#telethon-----
api_id = 25026218 # Тут укажите полученый ранее api
api_hash = '35e2d83fc7ca77eb48d3200917ae85f0' # Тут укажите полученый ранее hash
#-------------

count = 0 # количество выполненых обновлений (индикатор работоспособности.//////)
time_ozhidaniya = 5     #время через которое делается новый запрос джсона
list_minute = [16, 17, 18, 19, 36, 37, 38, 39] # какие минуты мониторит
uslovie_number = int(input('Choose the mode of operation (0,1,2)')) #выбор режима работы программы 

def get_ice_hockey_all_json():
    params = {
        'sports': '2',
        'count': '50',
        'antisports': '188',
        'mode': '4',
        'country': '1',
        'partner': '51',
        'getEmpty': 'true',
        'noFilterBlockEvent': 'true',
    }
    response = requests.get('https://1xstavka.ru/LiveFeed/Get1x2_VZip', params=params)
    return response.json()


def return_time_minute_second_round(second):
    minute = second // 60
    seconds = second % 60
    return f"{str(minute).rjust(2, '0')}:{str(seconds).rjust(2, '0')}"

def get_minute(second):
    minute = second // 60
    return minute

def return_time_in_list_minute(second):
    minute = second // 60
    return minute in list_minute


def match_selection(json_data):
    result_fun = ''
    for matchs in json_data['Value']:
        row_bolshinstva = matchs['SC'].get('I', 'Ничего')
        time_round = int(matchs['SC'].get('TS', 0))
        nalichie_bolshinstva = row_bolshinstva if 'большинстве' in row_bolshinstva else None
        availability_time_in_list_minute = return_time_in_list_minute(time_round)

        uslovie = [nalichie_bolshinstva is not None and get_minute(time_round) > 1, 
        nalichie_bolshinstva is not None and availability_time_in_list_minute, 
        get_minute(time_round) > 1]

        if uslovie[uslovie_number]:
            name_liga = matchs['L']
            time = return_time_minute_second_round(time_round)
            score_periods = ""
            for i in matchs['SC']['PS']: # Счет в периодах!
                result_period = list(i.values())[-1]
                score_periods += f"({result_period.get('S1', 0)}-{result_period.get('S2', 0)})"
            result_fun += f"{name_liga}\n{nalichie_bolshinstva}\n⚽️{score_periods}🕑{time}\n\n"

    return result_fun

# print(match_selection(get_ice_hockey_all_json()))        


with TelegramClient('my', api_id, api_hash) as client:

    while True:
        for i in client.iter_messages('@hockey_strategy', limit=1):
            last_message = i     #id, message

        count += 1
        print(count)
        result_function = match_selection(get_ice_hockey_all_json())
        if result_function != '':
            if len(last_message.message) + 2 == len(result_function):
                try:
                    client.edit_message('@hockey_strategy', message=last_message.id, text=result_function)
                except:
                    print('Failed edit message Warrning #001')
                    time_ozhidaniya = 3
            else:   
                client.send_message('@hockey_strategy', message=result_function)
        time.sleep(time_ozhidaniya)
        os.system('clear')