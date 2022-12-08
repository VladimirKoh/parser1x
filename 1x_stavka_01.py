import pygame
import requests
import time
import os



count = 0 # количество выполненых обновлений (индикатор работоспособности.//////)
time_ozhidaniya = 5     #время через которое делается новый запрос джсона
list_minute = [16, 17, 18, 19, 36, 37, 38, 39] # какие минуты мониторит
uslovie_number = int(input('Выберете режим работы\n(0 - большинство + любое время, 1 - Основное, 2 - все игры)')) #выбор режима работы программы 
# (0. Большинство + любое время)
# (1. Большинство + нужное время) --- основной режим
# (2. Все игры)

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
    return f"{minute}:{seconds}"

def get_minute(second):
    minute = second // 60
    return minute

def return_time_in_list_minute(second):
    minute = second // 60
    return minute in list_minute


def match_selection(json_data):
    result_fun = []
    for matchs in json_data['Value']:
        row_bolshinstva = matchs['SC'].get('I', None)
        time_round = int(matchs['SC'].get('TS', 0))
        nalichie_bolshinstva = row_bolshinstva if 'большистве' in row_bolshinstva else None
        availability_time_in_list_minute = return_time_in_list_minute(time_round)

        uslovie = [(nalichie_bolshinstva != None and ('начала' or 'Матч') not in nalichie_bolshinstva) and get_minute(time_round) > 1, 
        nalichie_bolshinstva is not None and availability_time_in_list_minute, 
        get_minute(time_round) > 1]

        if uslovie[uslovie_number]:
            name_liga = matchs['L']
            time = return_time_minute_second_round(time_round)
            score_periods = ""
            for i in matchs['SC']['PS']: # Счет в периодах!
                result_period = list(i.values())[-1]
                score_periods += f"({result_period.get('S1', 0)}-{result_period.get('S2', 0)})"
            result_fun.append(f"{name_liga}{score_periods}\n{nalichie_bolshinstva}\n{time}\n\n")

    if result_fun != []:
        pygame.init()
        song = pygame.mixer.Sound('123.mp3')
        clock = pygame.time.Clock()
        song.play()
        clock.tick(1)
    else:
        result_fun.append('Нет матчей')
        
    return result_fun

# print(match_selection(get_ice_hockey_all_json()))        

while True:
    count += 1
    print(count)
    print(*match_selection(get_ice_hockey_all_json()))
    time.sleep(time_ozhidaniya)
    os.system('clear')





#       тестовая функция для получения принтов

# def get_data_print(json_data):
#     for i in json_data['Value']:
#         print(i['L']) #название ЛИГИ
#         print(i['O1']) #название 1 команды
#         print(i['O2']) #название 2 команды
#         print(i['SC'].get('I', 'Большинства нет')) #Наличие большинства!
#         print(list(i['SC']['FS'].values())) #счет команд
#         time_round = int(i['SC']['TS']) # время игры
#         print(get_time_all_ice_hockey(time_round))
#         for i in i['SC']['PS']: # Счет в периодах!
#             result_period = list(i.values())[-1]
#             print(f"({result_period.get('S1', 0)}-{result_period.get('S2', 0)})", end=' ')
#         break

# get_data_print(get_ice_hockey_all_json())