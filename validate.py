#!/usr/bin/env python3

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
    automatic_table_allocation, \
    check_for_empty, \
    check_match, \
    chunk_them, \
    compare_single_match, \
    current_and_remainder, \
    generate_tables_per_section, \
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
    update_team_rank

################################################################################
################################################################################

pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 400)
pd.set_option('display.max_colwidth', -1)

json_directory = 'cdtta_thursday_night_json' #where json database files are kept.
validated_json_directory = json_directory+'/'+'validated'
temporary_json_directory = json_directory+'/'+'temporary' #put files there after validation, these files can be deleted in future.

if(not os.path.exists(json_directory)):
    raise SystemExit('function: json_directory doesnt exist.'+__file__+' line number: '+str(inspect.stack()[0][2]))

if(not os.path.exists(validated_json_directory)):
    raise SystemExit('function: validated_json_directory doesnt exist.'+__file__+' line number: '+str(inspect.stack()[0][2]))

if(not os.path.exists(temporary_json_directory)):
    raise SystemExit('function: temporary_json_directory doesnt exist.'+__file__+' line number: '+str(inspect.stack()[0][2]))

json_orient = 'split'
json_orient = 'records'

full_table_df = pd.read_json(json_directory+'/'+'full_table.json') #, orient='index')

number_of_games_per_match = 7

number_of_matches_per_match = 5

################################################################################
################################################################################

################################################################################

#check if files exist in both directories, they should not.

################################################################################

input_raw_files = sorted(glob.glob(json_directory+'/section_??_round_??_match_??_data.json'))
for input_file in input_raw_files:
    file1 = json_directory+'/'+just_file_name(diag, input_file)
    file2 = validated_json_directory+'/'+just_file_name(diag, input_file)
    if(os.path.exists(file1) and os.path.exists(file2)):
       print(file1)
       print(file2)
       raise SystemExit('function case 1: file exists in both raw and validated directory.'+__file__+' line number: '+str(inspect.stack()[0][2]))
    
################################################################################

input_validated_files = sorted(glob.glob(json_directory+'/section_??_round_??_match_??_data.json'))
for input_file in input_validated_files:
    file1 = json_directory+'/'+just_file_name(diag, input_file)
    file2 = validated_json_directory+'/'+just_file_name(diag, input_file)
    if(os.path.exists(file1) and os.path.exists(file2)):
       print(file1)
       print(file2)
       raise SystemExit('function case 2: file exists in both raw and validated directory.'+__file__+' line number: '+str(inspect.stack()[0][2]))
    
################################################################################

print(CRED+'Processing '+str(len(input_raw_files))+' files:'+CEND)

if(len(input_raw_files) > 0):
    for n in range(99):
        try:
            PERSON_VALIDATING_DATA = input(CRED+'Enter your full name (person validating match results) - alpha & spaces allowed: '+CEND)
        except:
            print(CGREEN+'Try again.'+CEND)
            continue

        #print('xxx'+PERSON_VALIDATING_DATA+'xxx')
        #print(PERSON_VALIDATING_DATA.isdigit())

        if(PERSON_VALIDATING_DATA.isdigit() and int(PERSON_VALIDATING_DATA) == 0):
            print(CRED+'Exiting...'+CEND)
            exit(0)
        elif(PERSON_VALIDATING_DATA == ''):
            print(CGREEN+'No blanks, try again.'+CEND)
            continue
        elif(not PERSON_VALIDATING_DATA.replace(' ', '').isalpha()):
            print(CGREEN+'Only alphabet letters,  try again.'+CEND)
            continue
        else:
            break

TODAYS_DATE_TIME = datetime.datetime.today().strftime('YYYY-MM-DD=%Y-%m-%d HH-MM-SS=%H-%M-%S')

for cnt,input_file in enumerate(input_raw_files):
    
    input_json_file = just_file_name(diag, input_file)
    
    section, ROUND, match = section_ROUND_match_from_json_filename(diag, json_directory+'/'+input_json_file)

    print(CGREEN+str(cnt+1)+'/'+str(len(input_raw_files))+': Examining input_json_file='+input_json_file+CEND)
    
    json_match_df = pd.read_json(json_directory+'/'+input_json_file, orient=json_orient)

    #display(json_match_df)

    results = json_match_df['Result']

    if(len(results) != number_of_matches_per_match):
        raise SystemExit('function: len(results)) != number_of_matches_per_match.'+__file__+' line number: '+str(inspect.stack()[0][2]))
    
    if(True): print('results=',results)

        #here we are always overriding result with that from input so that we can display it to make a decision
        #about whether it is correct or not.

    #exit(0)

    override_result = results
        
    #print('override_result=',override_result)
        
    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

#     display(json_match_df)
    
    if(diag): print('section, ROUND, match=', section, ROUND, match)
     
#     override_result = None
    
    #heiden
    
    team_sheet_df, summary_df = match_team_summary(diag, full_table_df, section, ROUND, match, True, number_of_games_per_match, number_of_matches_per_match, override_result)

    display(team_sheet_df)

    display(summary_df)


    json_match_df['Validated'] = ['YES'] * number_of_matches_per_match
    json_match_df['Validation Person'] = [PERSON_VALIDATING_DATA] * number_of_matches_per_match
    json_match_df['Validated Date/Time'] = [TODAYS_DATE_TIME] * number_of_matches_per_match

    display(json_match_df)
        
    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

    for n in range(999):
        try:
            QUESTION = input(CRED+'Would you like to move this raw file to the validated area [y/n or 0=break]? '+CEND)
        except:
            print('Try again.')
            continue
            
        if(not QUESTION.isalpha() and int(QUESTION) == 0):
            raise SystemExit('function: Exiting Validation.'+__file__+' line number: '+str(inspect.stack()[0][2]))
        elif(QUESTION != 'y' and QUESTION != 'n'):
            print('Only "y" or "n", try again.')
            continue
        else:
            break

    if(QUESTION == 'y'):
        #could check on value of newPath
        print(CGREEN+'Move '+json_directory+'/'+input_json_file+' to '+temporary_json_directory+CEND)

        if(os.path.isfile(temporary_json_directory+'/'+input_json_file)):
             backup_file = input_json_file+'_'+datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
             print(CRED+'Moving '+temporary_json_directory+'/'+input_json_file+' to '+temporary_json_directory+'/'+backup_file+CEND)
             newPath = shutil.move(temporary_json_directory+'/'+input_json_file, temporary_json_directory+'/'+backup_file)

        newPath = shutil.move(json_directory+'/'+input_json_file, temporary_json_directory)
        print('newPath=',newPath)

        print(CGREEN+'Creating validated file from dataframe '+validated_json_directory+'/'+input_json_file+CEND)

        json_match_df.to_json(validated_json_directory+'/'+input_json_file, orient=json_orient)
        tidy_json(diag, validated_json_directory+'/'+input_json_file)

    else:
        print(CGREEN+'Not moving this raw file to validated directory.'+CEND)
    
    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

#input_json_file = 'section_'+'{0:02d}'.format(section0+1)+'_round_'+'{0:02d}'.format(round0+1)+'_match_'+'{0:02d}'.format(match0+1)+'_data.json'

# if(os.path.exists(json_directory+'/'+input_json_file)):
#     print(CRED+json_directory+'/'+input_json_file+' exists...loading'+CEND)
#     json_match_df = pd.read_json(r''+json_directory+'/'+input_json_file, orient=json_orient)
    
################################################################################
################################################################################

exit()
