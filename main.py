
import requests, json
import pandas as pd

# TODO : check whether the api provides live dadta ; during the match

# Expires: Sun, Mar 8th, 2020 @ 1:44am (PT) in 23 hours and 59 minutes
APIKEY = 'RGAPI-4326cd61-46aa-45a7-8436-04c5a23a531a'
COUNT = 50

# 1PlsQ5hETM
PUUID = 'E-EdFlxIcUyJbOSNbiWb4M9MOhGT6d_v29hEuA91BvHz6JkYJ6Xdq6IETJfC_uY3egZJf5h81HWTxg'
# PaulMich
# puuid = 'UTJPDclizM2higGOwckRamzVdhkUj6DvW-FPq585vvGgauG70Lg3OXeEZ1roSNjEJ4BhaCYE1xCgTg'

def url_list_matches(puuid,count=20):
    return 'https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count={count}'.format(puuid = puuid, count=count)

def url_match_details(match_id):
    return 'https://europe.api.riotgames.com/tft/match/v1/matches/{match_id}'.format(match_id = match_id)

def request_endpoint(url):
    response = requests.get(url,
                            headers={
                                "Origin": "https://developer.riotgames.com",
                                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                                "X-Riot-Token": APIKEY,
                                "Accept-Language": "en-GB,en;q=0.9,el-GR;q=0.8,el;q=0.7,en-US;q=0.6"
                                      }
                            )
    return response

def human_timestamp(response):
    from datetime import datetime
    timestamp = response.get('info').get('game_datetime')
    timestamp = int(str(timestamp)[:-3])
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# TODO : obtain items and champions data


# TODO : process to parse match_details ; either functional or oop way


list_matches = request_endpoint(url_list_matches(PUUID)).json()
selected_match_id = list_matches[0]
match_details = request_endpoint(url_match_details(selected_match_id)).json()


match_details.keys()
match_details['metadata']
match_details['info']
match_details['info'].keys()
keys = list(match_details['info'].keys())

# explore json data
for key in keys:
    print(f'>> KEY : {key}')
    print(match_details['info'].get(key),"\n")


participants_puuids = match_details["metadata"].get("participants")
timestamp = human_timestamp(match_details)
game_length = f'{round(match_details["info"].get("game_length")/60,2)} mins'
game_version = match_details["info"].get("game_version")
queue_id = match_details["info"].get("queue_id")
tft_set_number = match_details["info"].get("tft_set_number")
participants = match_details["info"].get("participants")

participants[3].keys()
participants[3].get('gold_left')
participants[3].get('last_round')
participants[3].get('level')
participants[3].get('placement')
participants[3].get('players_eliminated')
participants[3].get('puuid')
participants[3].get('time_eliminated')
participants[3].get('total_damage_to_players')
participants[3].get('traits')
participants[3].get('units')

# pd.DataFrame(participants[3].get('traits')).set_index('name')
# pd.DataFrame(participants[3].get('units'))

units_df = pd.concat(pd.DataFrame(x) for x in [participant.get('units') for participant in participants])
traits_df = pd.concat(pd.DataFrame(x) for x in [participant.get('traits') for participant in participants])

traits_df.to_clipboard()
traits_df.groupby('name').size().sort_values(ascending=False)

units_df.to_clipboard()
units_df.groupby('character_id').size().sort_values(ascending=False)
