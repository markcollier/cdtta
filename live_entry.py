#!/usr/bin/env python3

#need to make sure that if entry exists in validated directory that a raw file cannot be generated, or at least a warning given.

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

json_directory = 'cdtta_thursday_night_json' #where json database files are kept.

validated_json_directory = json_directory+'/'+'validated'

if(not os.path.exists(json_directory)):
    raise SystemExit('function: json_directory doesnt exist.'+__file__+' line number: '+str(inspect.stack()[0][2]))

if(not os.path.exists(validated_json_directory)):
    raise SystemExit('function: validated_json_directory doesnt exist.'+__file__+' line number: '+str(inspect.stack()[0][2]))

json_orient = 'split'
json_orient = 'records'

full_table_df = pd.read_json(json_directory+'/'+'full_table.json')

number_of_games_per_match = 7

number_of_matches_per_match = 5

################################################################################
################################################################################

for n0 in range(999):
    print('Iteration [0] '+str(n0+1))
    live_match(diag, full_table_df, number_of_games_per_match, number_of_matches_per_match, json_directory, json_orient)

################################################################################
################################################################################

exit()
