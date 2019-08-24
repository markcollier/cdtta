#!/usr/bin/env ipython
##!/usr/bin/env python3

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
    get_fillins

################################################################################
################################################################################

pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 400)
pd.set_option('display.max_colwidth', -1)

# Pennant = "Wednesday Night"
Pennant = "Thursday Night"
# Pennant = "Monday Morning"
# Pennant = "Thursday Morning"

override_draw = False #force order of matches to be that given online/printed. Future seasons will use my ordering.
override_wooden_table = False

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
    override_wooden_table = True #force table allocation to be that given online/printed. Future seasons will use my ordering.
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
#Unique_Team_Names = Wednesday_Night_Team_Names

number_rounds = 10

number_of_players = len(Unique_Player_Ranking)

number_players_per_team = 2

number_teams = int(number_of_players / number_players_per_team)

#print('number_teams=',number_teams)

number_teams_float = (number_of_players / number_players_per_team)

#print('number_teams_float=',number_teams_float)

if(number_teams_float-number_teams!=0.0):
    raise SystemExit('function: number of players not divisible by 2 for 2 person team:'+__file__+' line number: '+str(inspect.stack()[0][2]))

validated_json_directory = json_directory+'/'+'validated'

if(not os.path.exists(json_directory)):
    raise SystemExit('function: json_directory doesnt exist.'+__file__+' line number: '+str(inspect.stack()[0][2]))

if(not os.path.exists(validated_json_directory)):
    raise SystemExit('function: validated_json_directory doesnt exist.'+__file__+' line number: '+str(inspect.stack()[0][2]))

#not really necessary as live_entry will add a comment to a README if it doesn't exist.
if(not os.path.exists(json_directory+'/'+'README')):
    print('Pennant README doesnt exist, create it.')
    open(json_directory+'/'+'README','a').close()

json_orient = 'split'
json_orient = 'records'

################################################################################
################################################################################

if(number_of_games_per_match != 3 and number_of_games_per_match != 7):
    raise SystemExit('number_of_games_per_match != 3 and number_of_games_per_match != 7:'+__file__+' line number: '+str(inspect.stack()[0][2]))
    
if(number_of_matches_per_match != 5):
    raise SystemExit('number_of_matches_per_match != 5:'+__file__+' line number: '+str(inspect.stack()[0][2]))
    
if( len(Unique_Team_Names) != len(set(Unique_Team_Names)) ):
    raise SystemExit('Team name dictionary, Unique_Team_Names, might have a duplicate entry:'+__file__+' line number: '+str(inspect.stack()[0][2]))

if( len(Unique_Player_Ranking) != len(set(Unique_Player_Ranking)) ):
    raise SystemExit('Player name dictionary, player_ranking, might have a duplicate entry:'+__file__+' line number: '+str(inspect.stack()[0][2]))
    
if( len(Unique_Team_Names) < number_teams ):
    raise SystemExit('len(Unique_Team_Names) < number_teams:'+__file__+' line number: '+str(inspect.stack()[0][2]))

################################################################################
################################################################################

################################################################################
################################################################################

#from this can specify:

if(Pennant=="Wednesday Night"):
    number_teams_per_section = [6, 8, 6, 6, 6, 6, 4, 4]
elif(Pennant=="Thursday Night"):
    number_teams_per_section = [4, 6, 6, 6, 6, 4]
elif(Pennant=="Monday Morning"):
    number_teams_per_section = [6, 6, 6, 4]
elif(Pennant=="Thursday Morning"):
    number_teams_per_section = [6, 6, 6, 6]
else:
    raise SystemExit('Pennant, '+Pennant+'Does not exist:'+__file__+' line number: '+str(inspect.stack()[0][2]))

number_sections = len(number_teams_per_section)

# tables_per_section = []
# for teams in number_teams_per_section:
#     tables_per_section.append(int(teams/2))

# tables_per_section = generate_tables_per_section(diag, number_teams_per_section)

section_players_raw = []
player_index_beg = 0
for cnt,section0 in enumerate(range(number_sections)):
    if(diag): print(cnt,section0)
    player_index_end = player_index_beg + number_teams_per_section[cnt]*2 -1

    if(diag): print(player_index_beg, player_index_end)
    
    if(diag): print('Section ',section0+1,'.:')
    if(diag): print(Unique_Player_Ranking[player_index_beg:player_index_end+1])
    
    section_players_raw.append(Unique_Player_Ranking[player_index_beg:player_index_end+1])
    
    player_index_beg = player_index_end + 1

for cnt,section0 in enumerate(range(number_sections)):
    #print(section_players_raw[cnt])
    players_1 = section_players_raw[cnt][0:number_teams_per_section[cnt]]
    players_2_tmp = section_players_raw[cnt][number_teams_per_section[cnt]::]
    players_2 = players_2_tmp[::-1]
    if(diag): print(section0+1,players_1,players_2)

section_list,team_list,team_name_list,player1_list,player2_list = [],[],[],[],[]
total_team_count = 0
for cnt,section0 in enumerate(range(number_sections)):
    for team0 in range(number_teams_per_section[cnt]):
        total_team_count += 1
        
        players_1 = section_players_raw[cnt][0:number_teams_per_section[cnt]]
        players_2_tmp = section_players_raw[cnt][number_teams_per_section[cnt]::][::-1]
        if(diag): print('section=',section0+1,' team=',team0+1,' team name=','Animal '+str(total_team_count)+ \
        ' player1='+players_1[team0]+' player2='+players_2_tmp[team0])
        section_list.append(section0+1)
        team_list.append(team0+1)
#         team_name_list.append('Animal '+str(total_team_count))
        team_name_list.append(Unique_Team_Names[total_team_count-1])
        player1_list.append(players_1[team0])
        player2_list.append(players_2_tmp[team0])
        
section_team_composition_df = pd.DataFrame({'Section': section_list, \
                   'Team' : team_list, \
                   'Team Name': team_name_list, \
                   'Player 1': player1_list, \
                   'Player 2': player2_list \
                  })

display(section_team_composition_df)

section_team_composition_df.to_html(json_directory+'/html/'+'section_team_composition_df.html', escape=False)

print(CCYAN+'Generated '+'section_team_composition_df.html'+CEND)

section_team_composition_df.to_json(json_directory+'/'+'section_team_composition.json')

################################################################################
################################################################################

YYYYMMDD = []

#print('number_teams_per_section=',number_teams_per_section)

#number_teams_per_section = [4, 6, 6, 6, 6, 4] #5 an option with 2 rounds of finals.

#number_sections = len(number_teams_per_section)

number_players_per_section = []
for cnt,section0 in enumerate(range(number_sections)):
    number_players_per_section.append(number_teams_per_section[cnt]*number_players_per_team)

one_week = timedelta(days=7)

for holiday_match in holiday_nomatches:
   if(holiday_match == first_round): \
        raise SystemExit('Set first round not to be a holiday round:'+__file__+' line number: '+str(inspect.stack()[0][2]))

found_rounds0 = 0

for round0 in range(99):
    
    current_round = first_round+one_week*round0
    
    holiday_clash=False
    for holiday_match in holiday_nomatches:
        if(holiday_match == current_round):
            if(diag): print('same')
            holiday_clash=True
        else:
            if(diag): print('not same')

    if(holiday_clash): print(CRED+'holiday_clash='+str(current_round)+CEND)
                
    if(not holiday_clash):
        found_rounds0 += 1
        YYYYMMDD.append(str(current_round))
        print(CGREEN+'round [1]='+str(found_rounds0)+' date='+str(current_round)+CEND)

        for section0 in range(number_sections):
            if(number_teams_per_section[section0]==4):
                if(found_rounds0==number_rounds):
                    finals=True
                else:
                    finals=False
            elif(number_teams_per_section[section0]==6):
                finals=False
            else:
                raise SystemExit('number of teams per section can only be 4 or 6:'+__file__+' line number: '+str(inspect.stack()[0][2]))
            print('section=',section0+1,' finals=',finals)
    
    if(found_rounds0 == number_rounds):
        print('Finished')
        break
        #raise SystemExit('Finished.')

#raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

################################################################################
################################################################################

#number_sets : the number of times the current group of matches needs to be used. If we have 4 team sections
#then there are 3, so some teams will play 2 home matches and others 1. If we have 6 team sections then all
#teams will play 1 home and 1 away match.
    
#overall_order_of_play_by_section = []
all_sections_all_rounds = ()
for cnt,current_number_teams_per_section in enumerate(number_teams_per_section):
    if(diag): print('cnt=',cnt)

    this_section_all_rounds = []
    if(current_number_teams_per_section==4):
        number_sets = 3
        matches_per_round = 2
    elif(current_number_teams_per_section==6):
        number_sets = 2
        matches_per_round = 3
    else:
        raise SystemExit('Only 4/6 valid:'+__file__+' line number: '+str(inspect.stack()[0][2]))

#above: doesnt matches_per_round = number_teams_per_section / number_sets?

    for number_set in range(number_sets):
        #print('number_set,number_set%number_sets=',number_set,number_set%number_sets)
        
        #alternatively switch:
        if(number_set%2==0):
            #print('normal')
            j = order_of_play_one_iteration(False, current_number_teams_per_section)
            #print('j=',j)
            
            this_section_all_rounds += chunk_them(diag, j, matches_per_round)
            
            #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))
    
        else:
            #print('reverse')
            j = order_of_play_one_iteration(False, current_number_teams_per_section)
            #print('j=',j)
            k = reverse_home_team(diag, j )
            #print('k=',k)
            this_section_all_rounds += chunk_them(diag, k, matches_per_round)
            
    if(current_number_teams_per_section==4): #this is for finals.
        this_section_all_rounds += [[[None, None], [None, None]]]
 
    if(diag): print('cnt,this_section_all_rounds=',cnt,this_section_all_rounds)
    
    all_sections_all_rounds += (this_section_all_rounds,)
    
all_sections_all_rounds = list(all_sections_all_rounds) #convert back to a list.

if(True): print('all_sections_all_rounds=',all_sections_all_rounds)

if(True): print('len(all_sections_all_rounds)=',len(all_sections_all_rounds))

#can pull out any section/round/match, currently will bomb if item doesn't exist.
SECTION0 = 5
ROUND0 = -2
MATCH0 = 0

if(diag): print(all_sections_all_rounds[SECTION0][ROUND0][MATCH0])

################################################################################
################################################################################

#tables_per_section = generate_tables_per_section(diag, number_teams_per_section)

#test data:
#ok
number_teams_per_section = [4, 6, 6, 6, 6, 4]
number_sections = len(number_teams_per_section)
groups_of_n = 3

#ok
# number_teams_per_section = [6, 6, 6, 6, 6, 6]
# number_sections = len(number_teams_per_section)
# groups_of_n = 3

#ok
# number_teams_per_section = [4, 4, 4, 4, 4, 4]
# number_sections = len(number_teams_per_section)
# groups_of_n = 2

#ok
# number_teams_per_section = [6, 4, 6, 4, 6, 4]
# number_sections = len(number_teams_per_section)
# groups_of_n = 3

#ok
# number_teams_per_section = [8, 6, 6, 6, 8]
# number_sections = len(number_teams_per_section)
# groups_of_n = 4

################################################################################

#comment out if testing above:
groups_of_n = 3 #this number is to be the size of the largest table requirement of a section.

wooden_table_max = 22 #do not allocate beyond 22. Table 23 is reserve for training, so good to keep one space at least.

wooden_table_init = 11 #start from this table, which is the first table in the new room.

all_sections_all_rounds_wooden_tables = automatic_wooden_table_allocation(diag, number_teams_per_section, number_rounds, groups_of_n, wooden_table_max, wooden_table_init)

#print('all_sections_all_rounds_tables=', all_sections_all_rounds_tables)

wooden_table_allocation_dict = {}
wooden_table_allocation_dict['Round'] = range(1,number_rounds+1)
for section0 in range(len(number_teams_per_section)):
    wooden_table_allocation_dict['Section '+str(section0+1)] = all_sections_all_rounds_wooden_tables[section0]

wooden_table_allocation_df = pd.DataFrame(wooden_table_allocation_dict)

#wooden_table_allocation_df.to_html(json_directory+'/html/'+'wooden_table_allocation_df.html', escape=False)

display(wooden_table_allocation_df)

################################################################################
################################################################################

all_sections_all_rounds_wooden_tables_override = [ \
[ [11,12],    [14,15],    [17,18],    [20,21],    [1, 2],     [4,5],      [11,12],    [14,15],    [17,18],    [20,21] ], \
[ [13,14,15], [16,17,18], [19,20,21], [1,2,3],    [3,4,5],    [11,12,13], [13,14,15], [16,17,18], [19,20,21], [1,2,3] ], \
[ [16,17,18], [19,20,21], [1,2,3],    [4,5,6],    [11,12,13], [14,15,16], [16,17,18], [19,20,21], [1,2,3],    [4,5,6] ], \
[ [19,20,21], [1,2,3],    [4,5,6],    [11,12,13], [14,15,16], [17,18,19], [19,20,21], [1,2,3],    [4,5,6],    [11,12,13] ], \
[ [1,2,3],    [4,5,6],    [11,12,13], [14,15,16], [17,18,19], [20,21,1],  [1,2,3],    [4,5,6],    [11,12,13], [14,15,16] ], \
[ [4,5],      [11,12],    [14,15],    [17,18],    [20,21],    [2,3],      [4,5],      [11,12],    [14,15],    [17,18] ], \
]

wooden_table_allocation_dict = {}
wooden_table_allocation_dict['Round'] = range(1,number_rounds+1)
for section0 in range(len(number_teams_per_section)):
    wooden_table_allocation_dict['Section '+str(section0+1)] = all_sections_all_rounds_wooden_tables_override[section0]

wooden_table_allocation_override_df = pd.DataFrame(wooden_table_allocation_dict)

display(wooden_table_allocation_override_df)

if(override_wooden_table):
    print(CRED+'Override wooden_tables to comform to printed/online version...'+CEND)
    all_sections_all_rounds_wooden_tables = list(all_sections_all_rounds_wooden_tables_override)

wooden_table_allocation_df = pd.DataFrame(wooden_table_allocation_dict)

wooden_table_allocation_df.to_html(json_directory+'/html/'+'wooden_table_allocation_df.html', escape=False)

print(CCYAN+'Generated '+json_directory+'/html/'+'wooden_table_allocation_df.html'+CEND)
    
#section,ROUND,match = 1,1,1

#print(all_sections_all_rounds_wooden_tables[section-1][ROUND-1][match-1]) #.split(',')[0])

################################################################################
################################################################################

sections_1and6 = [ \
                  [[1, 3], [2, 4]], \
                  [[4, 1], [3, 2]], \
                  [[1, 2], [4, 3]], \
                  [[3, 1], [2, 4]], \
                  [[1, 4], [2, 3]], \
                  [[2, 1], [3, 4]], \
                  [[1, 3], [2, 4]], \
                  [[4, 1], [3, 2]], \
                  [[3, 4], [2, 1]], \
                  [[None, None], [None, None]] \
                 ]

sections_2to5 = [ \
                 [[1, 6], [2, 5], [3, 4]], \
                 [[5, 1], [4, 2], [6, 3]], \
                 [[1, 4], [3, 2], [5, 6]], \
                 [[3, 1], [2, 6], [4, 5]], \
                 [[1, 2], [5, 3], [6, 4]], \
                 [[6, 1], [5, 2], [4, 3]], \
                 [[1, 5], [2, 4], [3, 6]], \
                 [[4, 1], [2, 3], [6, 5]], \
                 [[1, 3], [6, 2], [5, 4]], \
                 [[2, 1], [3, 5], [4, 6]] \
                ]

all_sections_all_rounds_override = ( sections_1and6,)
all_sections_all_rounds_override += ( sections_2to5,)
all_sections_all_rounds_override += ( sections_2to5,)
all_sections_all_rounds_override += ( sections_2to5,)
all_sections_all_rounds_override += ( sections_2to5,)
all_sections_all_rounds_override += ( sections_1and6,)

print('all_sections_all_rounds_override=',all_sections_all_rounds_override)
print('len(all_sections_all_rounds_override)=',len(all_sections_all_rounds_override))

if(override_draw):
    print(CRED+'Override section/match orders to comform to printed/online version...'+CEND)
    all_sections_all_rounds = list(all_sections_all_rounds_override)

################################################################################
################################################################################

draw_all_df = make_draw(diag, all_sections_all_rounds, YYYYMMDD)

#raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

#exit(0)

#print(len(draw_all_df))

if(os.path.exists(json_directory+'/html/'+'draw_all.html')):
    os.remove(json_directory+'/html/'+'draw_all.html')

for draw_one_df in draw_all_df:
    display(draw_one_df)
    append_df_to_html(diag, draw_one_df, json_directory+'/html/'+'draw_all.html')

print(CCYAN+'Generated '+json_directory+'/html/'+'draw_all.html'+CEND)

#raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))
        
################################################################################
################################################################################

#json_status = 0 #ignore files in main_draw_df creation.
#json_status = 1 #read only validated files
#json_status = 2 #read only raw files
#json_status = 3 #read both validated and raw files

if(json_status == 0):
    print('Ignoring all json files.')
elif(json_status == 1):
    print('Reading only validated json files (if the exist).')
elif(json_status == 2):
    print('Reading only raw json files (if the exist).')
elif(json_status == 3):
    print('Reading both validated and raw json files (if the exist).')
else:
    raise SystemExit('function: invalid json_status value.'+__file__+' line number: '+str(inspect.stack()[0][2]))
    
unique_match0 = -1
unique_matchs0 = []
rounds0 = []
sections0 = []
matchs0 = []
results0 = []
dates0 = []
tables0 = []

team1_player1s0 = []
team1_player2s0 = []

team2_player1s0 = []
team2_player2s0 = []

team1_fillin1s0 = []
team1_fillin2s0 = []

team2_fillin1s0 = []
team2_fillin2s0 = []

team1s0 = []
team2s0 = []

empty_5xN = [         [[], []],  \
                      [[], []], \
                      [[], []], \
                      [[], []], \
                      [[], []], ]

empty_11xN = [         [[], []],  \
                      [[], []], \
                      [[], []], \
                      [[], []], \
                      [[], []], \
                      [[], []], \
                      [[], []], \
                      [[], []], \
                      [[], []], \
                      [[], []], \
                      [[], []], ]

current_entries = 0

simple_wooden_table = True #create simple table allocation, will not be functinal though.
simple_wooden_table = False

for round0 in range(number_rounds):
    wooden_table_this_round0 = -1
    for section0 in range(len(number_teams_per_section)):
        for match0 in range(int(number_teams_per_section[section0]/number_players_per_team)):
            wooden_table_this_round0 +=1
            
            unique_match0 += 1

            #print('unique_match0,round0,section0,match0=',unique_match0,round0,section0,match0)
            unique_matchs0.append(unique_match0+1)
            rounds0.append(round0+1)
            dates0.append(YYYYMMDD[round0])
            sections0.append(section0+1)
            matchs0.append(match0+1)
            
#             section,ROUND,match = 1,1,1

#             print(all_sections_all_rounds_tables[section-1][ROUND-1][match-1]) #.split(',')[0])

                #heiden

            if(simple_wooden_table):
                tables0.append(wooden_table_this_round0+1)
            else:
                tables0.append(all_sections_all_rounds_wooden_tables[section0][round0][match0])
            #results0.append(empty_5xN)
            
########################################################################################################################################################################################

            input_json_file = 'section_'+'{0:02d}'.format(section0+1)+'_round_'+'{0:02d}'.format(round0+1)+'_match_'+'{0:02d}'.format(match0+1)+'_data.json'
            #test json files and load data if required:
            file1 = json_directory+'/'+input_json_file
            file2 = validated_json_directory+'/'+input_json_file
            if(os.path.exists(file1) and os.path.exists(file2)):
                raise SystemExit('os.path.exists(file1) and os.path.exists(file2), sort this out before we can continue.'+__file__+' line number: '+str(inspect.stack()[0][2]))

            iswitch = 0
            if(json_status > 0):
                if(os.path.exists(json_directory+'/'+input_json_file) and (json_status == 2 or json_status == 3)):
                    iswitch += 1
                    print(CRED+json_directory+'/'+input_json_file+' exists...loading unvalidated (raw) file...'+CEND)
                    json_match_df = pd.read_json(r''+json_directory+'/'+input_json_file, orient=json_orient)
                    results0.append(match_5xN(diag, json_match_df, number_of_games_per_match, number_of_matches_per_match))

                    #display(json_match_df)

                    #j=json_match_df['Player Names'].values
                    #k=json_match_df['Fillin Player Names'].values

                    #for cnt,x in enumerate(j):
                    #    print(j[cnt],k[cnt])

                    team1_fillins1, team1_fillins2, team2_fillins1, team2_fillins2 = \
                        get_fillins(diag, json_match_df['Player Names'].values.tolist(), json_match_df['Fillin Player Names'].values.tolist())
                    team1_fillin1s0.append(team1_fillins1)
                    team1_fillin2s0.append(team1_fillins2)
                    team2_fillin1s0.append(team2_fillins1)
                    team2_fillin2s0.append(team2_fillins2)
#heiden

                    #j = match_5xN(diag, json_match_df, number_of_games_per_match, number_of_matches_per_match)
                    #print('j=',j)
                    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

                if(os.path.exists(validated_json_directory+'/'+input_json_file) and (json_status == 1 or json_status == 3)):
                    iswitch += 1
                    print(CRED+validated_json_directory+'/'+input_json_file+' exists...loading validated file...'+CEND)
                    json_match_df = pd.read_json(r''+validated_json_directory+'/'+input_json_file, orient=json_orient)

                    print(json_match_df)

                    results0.append(match_5xN(diag, json_match_df, number_of_games_per_match, number_of_matches_per_match))

            #print('hello')
            #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

            if(iswitch == 0):
                results0.append(empty_5xN)
                team1_fillin1s0.append('NO')
                team1_fillin2s0.append('NO')
                team2_fillin1s0.append('NO')
                team2_fillin2s0.append('NO')

########################################################################################################################################################################################
      
                #print(match_5xN(False, j_df, number_of_games_per_match))
            
            extract_one = all_sections_all_rounds[section0][round0][match0]
    
            #print('extract_one=',extract_one)
            #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))
            
            if(extract_one[0]==None):
                team1s0.append('Team A Dummy')
                team1_player1s0.append('Player1 Dummy')
                team1_player2s0.append('Player2 Dummy')
            
            else:
                section_teamA = section_team_composition_df.query('Section == '+str(section0+1)).query('Team == '+str(extract_one[0])).values
                team1_player1s0.append(section_teamA[0][3])
                team1_player2s0.append(section_teamA[0][4])
                team1s0.append('Team ' + str(extract_one[0])+': '+section_teamA[0][2])
                
                #print('xxx=',section_teamA[0][2])
                #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

            if(extract_one[1]==None):
                team2s0.append('Team B Dummy')
                team2_player1s0.append('Player1 Dummy')
                team2_player2s0.append('Player2 Dummy')
            
            else:
                section_teamB = section_team_composition_df.query('Section == '+str(section0+1)).query('Team == '+str(extract_one[1])).values
                team2_player1s0.append(section_teamB[0][3])
                team2_player2s0.append(section_teamB[0][4])
                team2s0.append('Team ' + str(extract_one[1])+': '+section_teamB[0][2])
        
#             print('section_teamA=',section_teamA)
#             print('section_teamB=',section_teamB)
            
            #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

print('unique_match0=',unique_match0)

#section_team_composition_df.loc[ (section_team_composition_df['Section'] == 1) & (section_team_composition_df['Team Name'] == 'Bandicoot') ]

full_table_df = pd.DataFrame({ \
                        'Unique match': unique_matchs0, \
                        'Round': rounds0, \
                        'Match Date' : dates0, \
                        'Section' : sections0, \
                        'Match' : matchs0, \
                        'Table' : tables0, \
                        'Team1' : team1s0, \
                        'Team1 Player1': team1_player1s0, \
                        'Team1 Player2': team1_player2s0, \
                        'Team2': team2s0, \
                        'Team2 Player1': team2_player1s0, \
                        'Team2 Player2': team2_player2s0, \
                        'Team1 Fillin1': team1_fillin1s0, \
                        'Team1 Fillin2': team1_fillin2s0, \
                        'Team2 Fillin1': team2_fillin1s0, \
                        'Team2 Fillin2': team2_fillin2s0, \
                        'Result': results0, \
                  })


display(full_table_df)

full_table_df.to_html(json_directory+'/html/'+'full_table_df.html', escape=False)

print(CCYAN+'Generated '+json_directory+'/html/'+'full_table_df.html'+CEND)

full_table_df.to_json(json_directory+'/'+'full_table.json')

################################################################################
################################################################################

exit()
