#!/usr/bin/env python3

#need to run create_pennant.py to ensure results sections are up-to-date.

diag = True
diag = False

CRED = '\033[91m'
CGREEN = '\033[32m'
CBLUE = '\033[34m'
CCYAN = '\033[36m'
CEND = '\033[0m'

import pandas as pd
import numpy as np
from datetime import date
from datetime import timedelta
import datetime
import inspect
import itertools
import sys
#import psutil
#import ipywidgets as widgets
#from ipywidgets import Layout, interact, interact_manual, HBox, VBox
from IPython.display import display
from IPython.core.display import display, HTML
import json
import IPython
import os
import glob
import shutil

from src.cdtta_funcs import \
    automatic_wooden_table_allocation, \
    check_for_empty, \
    check_match, \
    chunk_them, \
    compare_single_match, \
    current_and_remainder, \
    generate_wooden_tables_per_section, \
    just_file_name, \
    keyboard_entry, \
    live_match, \
    make_draw, \
    match_5xN, \
    match_team_summary, \
    minimum_games_in_match, \
    order_of_play_one_iteration, \
    pad_score, \
    pennant_names, \
    populate_scores, \
    print_player_table, \
    print_team_table, \
    process_single_match, \
    reduce_size_to_section_size, \
    reset_team_player_rank, \
    reverse_home_team, \
    section_ROUND_match_from_json_filename, \
    sort_matches_list_of_tuples, \
    sort_matches_list_of_tuples, \
    string_list_to_integer_list, \
    tidy_json, \
    tuple_pair_to_list, \
    update_player_rank, \
    update_team_rank, \
    append_df_to_html, \
    concat_files, \
    find_fillins, \
    unpack_fillin_string

################################################################################
################################################################################

# Pennant = "Wednesday Night"
Pennant = "Thursday Night"
# Pennant = "Monday Morning"
# Pennant = "Thursday Morning"

override_draw = False #force order of matches to be that given online/printed. Future seasons will use my ordering.
override_table = False

#json_status = 0 #ignore files in main_draw_df creation.
#json_status = 1 #read only validated files
#json_status = 2 #read only raw files
json_status = 3 #read both validated and raw files

if(not json_status in [0,1,2,3]):
    raise SystemExit('function: json_status invalid.'+__file__+' line number: '+str(inspect.stack()[0][2]))

if(Pennant=="Wednesday Night"):
    Unique_Team_Names = Wednesday_Night_Team_Names
    Unique_Player_Ranking = Wednesday_Night_Player_Ranking
    holiday_nomatches = [None]
    first_round = datetime.date(2019,7,18)
    number_of_games_per_match = 7
    number_of_matches_per_match = 5

elif(Pennant=="Thursday Night"):
    Unique_Team_Names = pennant_names(diag, 'Team_Names', 'Thursday_Night')

    Unique_Player_Ranking = pennant_names(diag, 'Player_Names', 'Thursday_Night')

    json_directory = 'cdtta_thursday_night_json' #where json database files are kept.
    holiday_nomatches = [datetime.date(2019,8,1), datetime.date(2019,8,8)]
    holiday_nomatches = [None]
    first_round = datetime.date(2019,7,18)
    number_of_games_per_match = 7
    number_of_matches_per_match = 5
    override_draw = True #force order of matches to be that given online/printed. Future seasons will use my ordering.
    override_table = True #force table allocation to be that given online/printed. Future seasons will use my ordering.
    #override_table = False
    
elif(Pennant=="Monday Morning"):
    Unique_Team_Names = Monday_Morning_Team_Names
    Unique_Player_Ranking = Monday_Morning_Player_Ranking
    json_directory = 'cdtta_monday_morning_json' #where json database files are kept.
    holiday_nomatches = [None]
    first_round = datetime.date(2019,7,18)
    number_of_games_per_match = 3
    number_of_matches_per_match = 5
    
    #here, for the 4 team section, there are only 9 rounds, so one day is a holiday (e.g. 2nd week)
    #bye's are played out accordingly.
    
elif(Pennant=="Thursday Morning"):
    Unique_Team_Names = Thursday_Morning_Team_Names
    Unique_Player_Ranking = Thursday_Morning_Player_Ranking
    json_directory = 'cdtta_thursday_morning_json' #where json database files are kept.
    holiday_nomatches = [None]
    first_round = datetime.date(2019,7,18)
    number_of_games_per_match = 3
    number_of_matches_per_match = 5
    
else:
    raise SystemExit('Pennant, '+Pennant+'Does not exist:'+__file__+' line number: '+str(inspect.stack()[0][2]))

section_team_composition_df = pd.read_json(json_directory+'/'+'section_team_composition.json')

full_table_df = pd.read_json(json_directory+'/'+'full_table.json')

#perhaps go through the full_table_df looking for fillins, then add these to the section_team_composition_df.
#it is possible that a fillin can appear in more than one section.
#a fillin could fillin for multiple teams in the same section, however, they would get points as if they were in the one team.

#think best to keep a list of:
#player team win low total
#so that for the case of fillins a player who fills in for multiple teams is captured. They can be added together in the final table if necessary.

# pass fill in info. to reset_team_player so that it gets added in.

fillins_list = find_fillins(diag, full_table_df)

#raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

team_rank,player_rank = reset_team_player_rank(diag, section_team_composition_df, fillins_list)

print(player_rank)

#raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

#print('j=',j)
#raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

#print('team_rank=',team_rank)

full_table_df_shape = full_table_df.shape
#print( full_table_df.info(verbose=False) )
#print( full_table_df_shape )

for unique_match_no0 in range(full_table_df_shape[0]):
    #print('unique_match_no0=',unique_match_no0)
    
    section = full_table_df.loc[unique_match_no0,:]['Section']
    ROUND = full_table_df.loc[unique_match_no0,:]['Round']
    match = full_table_df.loc[unique_match_no0,:]['Match']
    
    #print('section,ROUND,match=',section,ROUND,match)
    
    override_result = None
    team_sheet_df, summary_df = match_team_summary(diag, full_table_df, section, ROUND, match, False, number_of_games_per_match, number_of_matches_per_match, override_result)
    
    if(type(team_sheet_df) == type(None) and type(summary_df) != type(None)):
        raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))
    if(type(team_sheet_df) != type(None) and type(summary_df) == type(None)):
        raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))
        
    if(type(team_sheet_df) != type(None) and type(summary_df) != type(None)):
    #will only come in here if there is a result to update...:

        team_sheet_df.to_html(json_directory+'/html/'+'team_sheet_df.html')
        summary_df.to_html(json_directory+'/html/'+'summary_df.html')

        print(CCYAN+'Generated '+json_directory+'/html/'+'team_sheet_df.html'+CEND)
        print(CCYAN+'Generated '+json_directory+'/html/'+'summary_df.html'+CEND)

        print('unique_match_no0=',unique_match_no0)
        print(CRED+'updating team/player ranking...'+CEND)

        player_rank = update_player_rank(diag, team_sheet_df, player_rank, number_of_games_per_match, number_of_matches_per_match, section)

        team_rank = update_team_rank(diag, team_sheet_df, summary_df, team_rank, number_of_games_per_match, number_of_matches_per_match)

        #print('player_rank=',player_rank)
        #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))
        #print('team_rank=',team_rank)
        
    #print(team_sheet_df,summary_df)
    
if(diag): print('team_rank=',team_rank)
if(True): print('player_rank=',player_rank)

#raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

################################################################################
################################################################################

number_sections = 6 #get rid of this later...automate.

team_table_html = 'cdtta_thursday_night_json/html/team_table_df.html'

player_table_html = 'cdtta_thursday_night_json/html/player_table_df.html'

if(os.path.exists(team_table_html)):
    os.remove(team_table_html)

if(os.path.exists(player_table_html)):
    os.remove(player_table_html)

for section0 in range(number_sections):
    team_table = {}
    section_stuff = section_team_composition_df.loc[section_team_composition_df['Section'] == section0+1].values
    
    for cnt in range(len(section_stuff)):
        team_name = section_stuff[cnt][2]
        #print(cnt,team_name)
        team_table[team_name] = team_rank[team_name]
    
    #print(section0+1,team_table)
    print_team_table(diag, team_table, section0+1, team_table_html)

#print('xxx=',player_rank['B#$M_Bandicoot_1_1'])

for section0 in range(number_sections):

    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

    player_table = {}
    section_stuff = section_team_composition_df.loc[section_team_composition_df['Section'] == section0+1].values
    
    print('section_stuff=',section_stuff)
    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

    #add in fillins to the player ranking for the particular section...
    #later these will be processed/formatted so that fillins are put to the bottom of the list, and
    #separate values for every team/section they play for.

    print('fillins_list=',fillins_list)
    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

    if(type(fillins_list) != type(None)):
        for fillin in fillins_list:
            player,team_name,section_number,team_number = unpack_fillin_string(diag, fillin)
            if(section_number==section0+1):
                #print('player,team_name,section_number,team_number=',player,team_name,section_number,team_number)
                #j = player_rank[fillin]
                #print(j)
                #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))
                #print('fillin=',fillin)
                #player_table[player] = player_rank[fillin] #use unpacked player name, player.
                player_table[fillin] = player_rank[fillin] #use unpacked player name, player.

        #add in regular players for the particular section...

    for cnt in range(len(section_stuff)):
        player_names = section_stuff[cnt][3:4+1]
        #print('player_names=',player_names)
        #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))
        for player_name in player_names:
            player_table[player_name] = player_rank[player_name]

    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

    print(section0+1,player_table)
    print_player_table(diag, player_table, section0+1, player_table_html)

print(CCYAN+'Generated '+team_table_html+CEND)
print(CCYAN+'Generated '+player_table_html+CEND)

#raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

################################################################################
################################################################################

exit(0)
