
import requests, json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import os

os.getcwd()
os.chdir(r'/home/takis/Desktop/sckool/lol-tft-api')

# TODO : check whether the api provides live dadta ; during the match

def url_puuid_by_name(region,name):
    return 'https://{region}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{name}'.format(region=region,name=name)

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

# ============================================================================================
# LOAD STATIC DATA
# ============================================================================================

hexes = pd.read_json('hexes.json')
items = pd.read_json('items.json')
traits = pd.read_json('traits.json')
champions = pd.read_json('champions.json')

# create binary columns for each trait
traits_list = list(set([item for sublist in list(champions.traits) for item in sublist]))
chmp = champions.copy()

for t in traits_list:
    chmp['trait_' + t] = chmp.traits.apply(lambda x : 1 if t in x else 0)

# ============================================================================================
# OBTAIN AND PARSE API DATA
# ============================================================================================

APIKEY = 'RGAPI-4326cd61-46aa-45a7-8436-04c5a23a531a'
# Expires: Sun, Mar 8th, 2020 @ 1:44am (PT) in 23 hours and 59 minutes
COUNT = 50
REGION = 'eun1' # euw1
NAME = '1PlsQ5hETM'

PUUID = request_endpoint(url_puuid_by_name(REGION,NAME)).json().get('puuid')
# 1PlsQ5hETM
# PUUID = 'E-EdFlxIcUyJbOSNbiWb4M9MOhGT6d_v29hEuA91BvHz6JkYJ6Xdq6IETJfC_uY3egZJf5h81HWTxg'
# PaulMich
# puuid = 'UTJPDclizM2higGOwckRamzVdhkUj6DvW-FPq585vvGgauG70Lg3OXeEZ1roSNjEJ4BhaCYE1xCgTg'

list_matches = request_endpoint(url_list_matches(PUUID)).json()
selected_match_id = list_matches[0]
match_details = request_endpoint(url_match_details(selected_match_id)).json()

# Parse json data
match_id = match_details["metadata"].get("match_id")
participants_puuids = match_details["metadata"].get("participants")
timestamp = human_timestamp(match_details)
game_length = f'{round(match_details["info"].get("game_length")/60,2)} mins'
game_version = match_details["info"].get("game_version")
queue_id = match_details["info"].get("queue_id")
tft_set_number = match_details["info"].get("tft_set_number")
participants = match_details["info"].get("participants")

# participants dataframe
my_cols = ['puuid', 'gold_left', 'last_round', 'level', 'placement', 'players_eliminated', 'time_eliminated', 'total_damage_to_players']
participants_df = pd.DataFrame({c : [p.get(c) for p in participants] for c in my_cols})

# units dataframe
units_df = pd.concat(pd.DataFrame(participant.get('units')).assign(puuid = participant.get('puuid')) for participant in participants)
units_df['name_adj'] = units_df['character_id'].apply(lambda x : x.split("_")[1])

# traits dataframe
traits_df = pd.concat(pd.DataFrame(participant.get('traits')).assign(puuid = participant.get('puuid')) for participant in participants)

# aggregations
traits_df[['puuid','name','num_units','tier_total','tier_current']].sort_values(by=['puuid','tier_total','tier_current'])
traits_df.groupby('name').size().sort_values(ascending=True).plot(kind='barh')
units_df.groupby('name_adj').size().sort_values(ascending=True).plot(kind='barh')
