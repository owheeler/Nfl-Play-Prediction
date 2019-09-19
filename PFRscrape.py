# Packages
import pandas as pd
import requests 
from bs4 import BeautifulSoup 
from datetime import datetime
startTime = datetime.now()

years = range(2015, 2019)
week_numbers = range(1,17)
quarters = range(1,4)
downs = [1,2,3]
yards = range(0, 100, 50)
rush_directions = ['LE', 'LT', 'LG', 'M', 'RG', 'RT', 'RE']
pass_locations = ['SL', 'SM','SR', 'DL', 'DM', 'DR']
game_locations = ['H', 'R', 'N']

data = pd.DataFrame()

for year in years:
    for week in week_numbers:
        for game_location in game_locations:
            #for down in downs:
                #for yard in yards:
                    for rush_direction in rush_directions:
                        address = f'https://www.pro-football-reference.com/play-index/play_finder.cgi?request=1&match=summary_all&year_min={year}&year_max={year}&game_type=R&game_location={game_location}&game_num_min=0&game_num_max=99&week_num_min={week}&week_num_max={week}&quarter%5B%5D=1&quarter%5B%5D=2&quarter%5B%5D=3&quarter%5B%5D=4&minutes_max=15&seconds_max=00&minutes_min=00&seconds_min=00&down%5B%5D=1&down%5B%5D=2&down%5B%5D=3&yards_min=0&yards_max=99&field_pos_min_field=team&field_pos_max_field=team&end_field_pos_min_field=team&end_field_pos_max_field=team&type%5B%5D=RUSH&is_sack=N&include_kneels=N&no_play=N&turnover_type%5B%5D=interception&turnover_type%5B%5D=fumble&score_type%5B%5D=touchdown&score_type%5B%5D=field_goal&score_type%5B%5D=safety&rush_direction%5B%5D={rush_direction}&order_by=yards'

                        #print(f'Year: {year} Week: {week} Quarter: {quarter} Down: {down}, Yard: {yard} Direction: {rush_direction}')
                        print(f'Year: {year} Week: {week} Direction: {rush_direction} Game Location: {game_location}')

                        r = requests.get(address) 
                        soup = BeautifulSoup(r.content, 'html5lib') 
                        table = soup.find('table', attrs = {'id':'all_plays'})
                        if table != None:
                            #print(table)
                            df = pd.read_html(table.prettify())[0]
                            df['play'] = 'Rush'
                            df['playlocation'] = rush_direction
                            df['HomeAway'] = game_location
                            data = data.append(df)
                            print(f'Success. Data Rows:{len(data)}')


for year in years:
    for week in week_numbers:
        for game_location in game_locations:
            #for down in downs:
                #for yard in yards:
                    for pass_location in pass_locations:
                        address = f'https://www.pro-football-reference.com/play-index/play_finder.cgi?request=1&match=summary_all&year_min={year}&year_max={year}&game_type=R&game_location={game_location}&game_num_min=0&game_num_max=99&week_num_min={week}&week_num_max={week}&quarter%5B%5D=1&quarter%5B%5D=2&quarter%5B%5D=3&quarter%5B%5D=4&minutes_max=15&seconds_max=00&minutes_min=00&seconds_min=00&down%5B%5D=1&down%5B%5D=2&down%5B%5D=3&yards_min=0&yards_max=99&field_pos_min_field=team&field_pos_max_field=team&end_field_pos_min_field=team&end_field_pos_max_field=team&type%5B%5D=PASS&is_sack=N&include_kneels=N&no_play=N&turnover_type%5B%5D=interception&turnover_type%5B%5D=fumble&score_type%5B%5D=touchdown&score_type%5B%5D=field_goal&score_type%5B%5D=safety&&pass_location%5B%5D={pass_location}&order_by=yards'

                        #print(f'Year: {year} Week: {week} Quarter: {quarter} Down: {down}, Yard: {yard} Direction: {rush_direction}')
                        print(f'Year: {year} Week: {week} Direction: {pass_location} Game Location: {game_location}')

                        r = requests.get(address) 
                        soup = BeautifulSoup(r.content, 'html5lib') 
                        table = soup.find('table', attrs = {'id':'all_plays'})
                        if table != None:
                            #print(table)
                            df = pd.read_html(table.prettify())[0]
                            df['play'] = 'Pass'
                            df['playlocation'] = pass_location
                            df['HomeAway'] = game_location
                            data = data.append(df)
                            print(f'Success. Data Rows:{len(data)}')


data.to_csv('Data/PlayData.csv')

print(datetime.now() - startTime)
"""
## Rush

f'https://www.pro-football-reference.com/play-index/play_finder.cgi?request=1&match=summary_all&year_min={year}&year_max={year}&game_type=R&game_num_min=0&game_num_max=99&week_num_min={week}&week_num_max={week}&quarter%5B%5D={quarter}&minutes_max=15&seconds_max=00&minutes_min=00&seconds_min=00&down%5B%5D={down}&yards_min={yard}&yards_max={yard}&field_pos_min_field=team&field_pos_max_field=team&end_field_pos_min_field=team&end_field_pos_max_field=team&type%5B%5D=RUSH&is_sack=N&include_kneels=N&no_play=N&turnover_type%5B%5D=interception&turnover_type%5B%5D=fumble&score_type%5B%5D=touchdown&score_type%5B%5D=field_goal&score_type%5B%5D=safety&rush_direction%5B%5D={rush_direction}&order_by=yards'

## Pass

f'https://www.pro-football-reference.com/play-index/play_finder.cgi?request=1&match=summary_all&year_min={year}&year_max={year}&game_type=R&game_num_min=0&game_num_max=99&week_num_min={week}&week_num_max={week}&quarter%5B%5D={quarter}&minutes_max=15&seconds_max=00&minutes_min=00&seconds_min=00&down%5B%5D={down}&yards_min={yard}&yards_max={yard}&field_pos_min_field=team&field_pos_max_field=team&end_field_pos_min_field=team&end_field_pos_max_field=team&type%5B%5D=PASS&is_sack=N&include_kneels=N&no_play=N&turnover_type%5B%5D=interception&turnover_type%5B%5D=fumble&score_type%5B%5D=touchdown&score_type%5B%5D=field_goal&score_type%5B%5D=safety&&pass_location%5B%5D={pass_location}&order_by=yards'

"""