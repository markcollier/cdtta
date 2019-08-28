#!/usr/bin/env python3

import glob
import os

files = glob.glob('cdtta_thursday_night_json/section_??_round_??_match_??_data.json')
for file in files:
    os.remove(file)

files = glob.glob('cdtta_thursday_night_json/validated/section_??_round_??_match_??_data.json')
for file in files:
    os.remove(file)

files = glob.glob('cdtta_thursday_night_json/temporary/section_??_round_??_match_??_data.json_????-??-??-??-??-??')
for file in files:
    os.remove(file)

exit()
