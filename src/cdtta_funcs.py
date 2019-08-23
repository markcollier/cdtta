##################################################################################################

def sort_matches_list_of_tuples(diag, matches):
    '''
    Creator: Mark Collier
    Last Modified: 16 August 2019
    '''
    aa = ()
    for b in matches:
        c,d = b
        aa += (tuple(sorted([c,d])),)
    sorted_matches = list(set(aa))
    return(sorted_matches) #end of sort_matches_list_of_tuples

################################################################################

def tuple_pair_to_list(diag, values):
    '''
    Creator: Mark Collier
    Last Modified: 16 August 2019
    '''
    #print('values=',values)
    #convert to a list
    newlist = []
    for v in values:
        a,b = v
        newlist.append([a,b])
    return(newlist) #end of tuple_pair_to_list

################################################################################

def current_and_remainder(diag, all_items):
    '''
    Creator: Mark Collier
    Last Modified: 16 August 2019
    
    this works by supplying a list _all_items_. It creates a _current_rounds_ list based on first entry and unique teams.
    the remaining matches _all_items_remainder_ are returned for the next iteration.
    in theory it will take an integer number of passes to produce the full set of unique matches.
    these unque matches will then be used to form the total set for the season (10 if no final=4 teams and 9 if a final=6 teams).
    '''
    
    import copy

    all_items_remainder = copy.deepcopy(all_items)
    
    current_rounds = [all_items[0]]

    #print('BEFORE MAIN LOOP:')
    if(diag): print('current_and_remainder: all_items=',all_items)
    if(diag): print('current_and_remainder: current_rounds=',current_rounds)
    if(diag): print('current_and_remainder: all_items_remainder=',all_items_remainder)

    #print('current_rounds[0]=',current_rounds[0])
    
    all_items_remainder.remove(current_rounds[0])
    
    if(diag): print('current_and_remainder: all_items_remainder=',all_items_remainder)        
    ##print('BEFORE MAIN LOOP:')
    
    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))
    
    for cnt,item in enumerate(all_items[1::]):
        if(diag): print(CRED+'cnt='+str(cnt)+CEND,'item=',item)

        #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))
        
        cnt_item_current_round = 0
        for current_round in current_rounds:
            
            if(current_round[0] in item or current_round[1] in item):
                cnt_item_current_round += 1
                if(diag): print('match a team, no good')

            else:
                cnt_item_current_round += 0
                if(diag): print('no match team, good')
 
        if(cnt_item_current_round == 0): 
            current_rounds.append(item)
            all_items_remainder.remove(item) #remove match from list if found to be good
            #new_item = False
            
        if(diag): print('current_rounds=',current_rounds)
        if(diag): print('cnt_item_current_round=',cnt_item_current_round)
            
    #print('AFTER MAIN LOOP:')
    if(diag): print('all_items_remainder=',all_items_remainder)
    if(diag): print('current_rounds=',current_rounds)
    #print('AFTER MAIN LOOP:')
    
    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))
    return(current_rounds, all_items_remainder)#end of current_and_remainder

################################################################################

def order_of_play_one_iteration(diag, number_team_this_section):
    import itertools
    import inspect
    
    '''
    Creator: Mark Collier
    Last Modified: 16 August 2019
    '''

    all_matches_one_round = list(itertools.combinations((range(1,number_team_this_section+1)),2))

    if(diag): print('all_matches_one_round=',all_matches_one_round)

    sorted_matches = sort_matches_list_of_tuples(False, all_matches_one_round)

    if(diag): print('sorted_matches=',sorted_matches)

    list_of_matches_now = tuple_pair_to_list(diag, sorted_matches)

    if(diag): print('list_of_matches_now=',list_of_matches_now)

    all_teams_round = []
    
    for ROUND in range(number_team_this_section-1):

        if(diag): print(CGREEN+'ROUND='+str(ROUND)+CEND)

        current_round, remainder = current_and_remainder(diag, list_of_matches_now)

        list_of_matches_now = remainder

        if(diag): print('first_matches_current_round=',first_matches_current_round)

        if(diag): print(CRED+'output: current_round='+CEND,current_round)
        
        if(diag): print(CRED+'output: list_of_matches_now='+CEND,list_of_matches_now)

        #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))
        
        all_teams_round += current_round

    if(len(list_of_matches_now) != 0): raise SystemExit('len(list_of_matches_now) should == 0:'+__file__+' line number: '+str(inspect.stack()[0][2]))
        
    return(all_teams_round) #end of order_of_play_one_iteration

################################################################################

def reverse_home_team(diag, datas):
    '''
    datas: 2 dimensional list.
    reversed_datas: 2 dimension list or inner array switched.
    '''
    #print('reverse_home_team: datas=',datas)
    reversed_datas = []
    for data in datas:
        reversed_datas.append( [data[1],data[0]] )
    return(reversed_datas) #end of reverse_home_team

################################################################################

def chunk_them(diag, j, n):
    '''
    Creator: Mark Collier
    Last Modified: 16 August 2019
    
    j is a unique set of matches using all combinations, for a complete season it will need to be utilised several times - and reversed for alternating rounds.
    k will put them into the correct number of matches per round (chunks).
    '''
    k = []
    if(diag): print('j=',j)
    
    x = []
    for m in range(len(j)):
        if(diag): print('m,n,m%n=',m,n,m%n)
        if(m%n == 0):
            x = [ j[m] ]
        elif(m%n == n-1):
            x += [ j[m] ]
            k += [ x ]
            x = []
        else:
            x += [ j[m] ]
            
    if(diag): print('k=',k)

    return(k) #end of chunk_them

################################################################################

def check_match(diag, X, number_of_games_per_match, number_of_matches_per_match):
    '''
    Creator: Mark Collier
    Last Modified: 16 August 2019
    
    various checks on a single game.
    '''
    #diag=True
    import inspect

#     #think this can be done generally with int(number_of_games_per_match+1/4):
#     if(number_of_games_per_match==7):
#         minimum_values = 4
#     elif(number_of_games_per_match==3):
#         minimum_values = 2
#     else:
#         raise Exception('Exception8') 
    #minimum_values = int((number_of_games_per_match+1)/2) #works for odd number_number_of_games_per_match
    
    minimum_values = minimum_games_in_match(diag, number_of_games_per_match)
    
    if(diag): print(X)
    if(len(X) < minimum_values): raise SystemExit('check_match: len(X) < minimum_values:'+__file__+' line number: '+str(inspect.stack()[0][2]))
    if(len(X) > number_of_games_per_match): raise SystemExit('check_match: len(team X) > number_of_games_per_match:'+__file__+' line number: '+str(inspect.stack()[0][2]))
        
    for game0 in range(len(X)):
        if(X[game0] < 0): raise SystemExit('check_match: X[game0] < 0:'+__file__+' line number: '+str(inspect.stack()[0][2]))
        if(X[game0] > 99): print(CRED+'check_match: warning: X[game0] > 99:'+__file__+' line number: '+str(inspect.stack()[0][2])+CEND)

    match_X_points = sum(X)
    match_X_games = len(X)
    
    return(match_X_points, match_X_games) #end of check_match

################################################################################

def compare_single_match(diag, A, B, number_of_games_per_match, number_of_matches_per_match):
    '''
    Creator: Mark Collier
    Last Modified: 16 August 2019
    
    various checks on a single match.
    Inputs:

    A: list []
    B: list []
    Outputs:

    Ascore,Bscore: lists []

    '''
    #diag=True
    import inspect

    if(len(A) != len(B)): raise SystemExit('compare_single_match: len(A) != len(B):'+__file__+' line number: '+str(inspect.stack()[0][2]))
   
    D = []
    if(diag): print(A,B)
    
    if(diag): print('A=',A)
    if(diag): print('B=',B)
    
    for cnt, a in enumerate(A):
        if(A[cnt]!= 0 & B[cnt]!= 0 & A[cnt] == B[cnt]): \
            raise SystemExit('compare_single_match: A[cnt] == B[cnt]:'+__file__+' line number: '+str(inspect.stack()[0][2]))
   
        D.append(A[cnt]- B[cnt])
    
    #print(A-B)
    if(diag): print('D=',D)
    
    Ascore,Bscore = 0,0
    for d in D:
        if(d>0): Ascore += 1
        if(d<0): Bscore += 1
            
    Extra_points = number_of_games_per_match - (Ascore+Bscore)
    
    if(diag): print('Extra_points=',Extra_points)
    
    if(Extra_points < 0): \
        raise SystemExit('compare_single_match: #Extra_points < 0:'+__file__+' line number: '+str(inspect.stack()[0][2]))
    if(Extra_points > 4): \
        raise SystemExit('compare_single_match: #Extra_points > 4:'+__file__+' line number: '+str(inspect.stack()[0][2]))
        
    if(Extra_points > 0):
        if(Ascore > Bscore): Ascore += Extra_points
        elif(Bscore > Ascore): Bscore += Extra_points
            
    return(Ascore,Bscore) #end of compare_single_match

################################################################################

def pad_score(diag, score):
    '''
    Creator: Mark Collier
    Last Modified: 16 August 2019
    
    create 7 entries for a 7 game match.
    '''
    import inspect
    
    if(diag): print('pad_score: score=',score)
    
    if(len(score) < 1): raise SystemExit('pad_score: len(score) <1:'+__file__+' line number: '+str(inspect.stack()[0][2]))
    if(len(score) > 7): raise SystemExit('pad_score: len(score) >7:'+__file__+' line number: '+str(inspect.stack()[0][2]))

    pscore = []
    for p in score:
        if(diag): print('p=',p)
        pscore.append(str(p))
        
    for x in range(7-len(score)):
        pscore.append(' ')

    return(pscore) #end of pad_score

################################################################################

def populate_scores(diag, scores):
    '''
    Creator: Mark Collier
    Last Modified: 16 August 2019
    '''
    import inspect
    
    if(diag): print('populate_scores: scores=',scores)
    if(diag): print('populate_scores: len(scores)=',len(scores))
    if(len(scores) != 5): \
        raise SystemExit('populate_scores: len(scores) != 5:'+__file__+' line number: '+str(inspect.stack()[0][2]))

    padded_scores = [] 
    for score in scores:
        if(diag): print('score=',score)

        padded_scores.append([pad_score(diag, score[0]), pad_score(diag, score[1])])
        
    if(diag): print('padded_scores=',padded_scores)
    
    match1_AB = padded_scores[0][0]
    match1_XY = padded_scores[0][1]

    match2_AB = padded_scores[1][0]
    match2_XY = padded_scores[1][1]
    
    match3_AB = padded_scores[2][0]
    match3_XY = padded_scores[2][1]
    
    match4_AB = padded_scores[3][0]
    match4_XY = padded_scores[3][1]
    
    match5_AB = padded_scores[4][0]
    match5_XY = padded_scores[4][1]

    if(diag): print('match1_AB,match1_XY=',match1_AB,match1_XY)
    if(diag): print('match5_AB,match5_XY=',match5_AB,match5_XY)
        
    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

    return(match1_AB,match2_AB,match3_AB,match4_AB,match5_AB, \
        match1_XY,match2_XY,match3_XY,match4_XY,match5_XY) #end of populate_scores

################################################################################

def process_single_match(diag, A, B, number_of_games_per_match, number_of_matches_per_match):
    '''
    Creator: Mark Collier
    Last Modified: 16 August 2019
    
    various checks.
    '''

    if(diag): print(A,B)
    
    match_A_points,match_A_games = check_match(diag, A, number_of_games_per_match, number_of_matches_per_match)
    match_B_points,match_B_games = check_match(diag, B, number_of_games_per_match, number_of_matches_per_match)
    
    if(diag): print('match_A_points,match_A_games=',match_A_points,match_A_games)
    if(diag): print('match_B_points,match_B_games=',match_B_points,match_B_games)
    
    Ascore,Bscore = compare_single_match(diag, A, B, number_of_games_per_match, number_of_matches_per_match)
    
    if(diag): print('Ascore,Bscore=',Ascore,Bscore)
    
    return(Ascore,Bscore,match_A_points,match_B_points) #end of process_single_match

################################################################################

def match_5xN(diag, df, number_of_games_per_match, number_of_matches_per_match):
    '''
    Creator: Mark Collier
    Last Modified: 22 August 2019
    
    setup for 5 matches, N games each.
    '''
    out_list = []

    results = df.sort_values(by=['Unique Match'])['Result']

    if(diag): print('results=',results)

    for n in range(number_of_matches_per_match):
        out_list.append(results[n])

    if(diag): print('out_list=',out_list)

    return(out_list) #end of match_5xN

################################################################################

def check_for_empty(diag, scores_whole_match):
    '''
    Creator: Mark Collier
    Last Modified: 16 August 2019
    
    There are only two kinds of match scores
    1. empty set
    2. regular set with meaningful numbers.
    '''
    #diag = False
    empty = False
    length = 0
    for x in range(len(scores_whole_match)):
        if(diag): print('x',x,scores_whole_match[x])
        for y in range(len(scores_whole_match[x])):
            #print(y,scores_whole_match[x][y])
            if(diag): print('y',y,len(scores_whole_match[x][y]))
            if(len(scores_whole_match[x][y]) != 0): length += 1
    if(length == 0): empty = True
    return(empty) # end of check_for_empty

################################################################################

def match_team_summary(diag, full_table_df, section, ROUND, match, verbose, number_of_games_per_match, number_of_matches_per_match, override_result):
    '''
    Creator: Mark Collier
    Last Modified: 21 August 2019
    
    Inputs:
    
    section (1-max):
    ROUND (0-max): is capatalised as round is a system defined function.
    match (1-max): every round and section has a unique set of matches.
    override_result: this will override the match results found in full_table_df
        so that we can see them printed in susmmary form, without having to create another function.

    Outputs:
    
    1. team_sheet_df: a single team sheet match (like used/generated on match night)
    2. summary_df: summary of points (like used/generated on match night)
    '''
    import inspect
    import pandas as pd
    from IPython.display import display
    import numpy as np
    CRED = '\033[91m'
    CGREEN = '\033[32m'
    CEND = '\033[0m'
    
    if(number_of_games_per_match == 7):
        maximum_match_points = 41
    elif(number_of_games_per_match == 3):
        maximum_match_points = 21
    else:
        raise SystemExit('maximum_match_points only 41/21.'+__file__+' line number: '+str(inspect.stack()[0][2]))        
        
    #round_df = main_df.loc[main_df['Round'] == ROUND]
    
    #extract_match = full_table_df.query('Round == '+str(ROUND)).query('Section == '+str(section)).query('Match == '+str(match)).values
    
    extract_match = full_table_df.loc[(full_table_df['Round'] == ROUND) & (full_table_df['Section'] == section) & (full_table_df['Match'] == match)]
    
    if(diag): display(extract_match)

    #print('extract_match=',extract_match)
    
    team1_player1 = extract_match['Team1 Player1'].values[0]
    team1_player2 = extract_match['Team1 Player2'].values[0]
    team2_player1 = extract_match['Team2 Player1'].values[0]
    team2_player2 = extract_match['Team2 Player2'].values[0]
    
#     team1_player1 = extract_match[0][7]
#     team1_player2 = extract_match[0][8]
#     team2_player1 = extract_match[0][10]
#     team2_player2 = extract_match[0][11]

    if(diag): print('team1_player1=',team1_player1)
    if(diag): print('team1_player2=',team1_player2)

    if(diag): print('team2_player1=',team2_player1)
    if(diag): print('team2_player2=',team2_player2)

    team1 = extract_match['Team1'].values[0]
    team2 = extract_match['Team2'].values[0]
    
#     team1 = extract_match[0][6]
#     team2 = extract_match[0][9]

    if(diag): print('team1=',team1)
    if(diag): print('team2=',team2)

    scores_whole_match = extract_match['Result'].values[0]
    
    #scores_whole_match = extract_match[0][-1]

    #heiden
    
    if(diag): print('match_team_summary: scores_whole_match=',scores_whole_match)
        
    if(type(override_result) != type(None)):
        print(CRED+'match_team_summary: overriding match result with new values.'+CEND)
        #uncomment later:
        scores_whole_match = override_result
        if(diag): print('match_team_summary: scores_whole_match=',scores_whole_match)

    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

    if(check_for_empty(diag, scores_whole_match)):
        if(verbose): print(CGREEN+'match_team_summary: scores are empty.'+CEND)
        return(None, None)
        #raise SystemExit('scores are empty:'+__file__+' line number: '+str(inspect.stack()[0][2]))

    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

    if(len(scores_whole_match)!=5): \
            raise SystemExit('#matches not equal 5:'+__file__+' line number: '+str(inspect.stack()[0][2]))

    team1_rubbers,team2_rubbers = 0,0
    team1_games,team2_games = 0,0
    team1_bonus_point,team2_bonus_point = 0,0
    team1_total_points,team2_total_points = 0,0

    team1_scores,team2_scores = 0,0

    team1_rubbers_list,team2_rubbers_list = [],[]
    team1_scores_list,team2_scores_list = [],[]
    for match0 in range(len(scores_whole_match)):
        #print('match0=',match0)

        team1_current_match = scores_whole_match[match0][0]
        team2_current_match = scores_whole_match[match0][1]

        team1_score,team2_score,team1_points,team2_points =  \
            process_single_match(diag, team1_current_match, team2_current_match, number_of_games_per_match, number_of_matches_per_match)

    #     print('team1_score,team2_score=',team1_score,team2_score)
    #     print('team1_points,team2_points=',team1_points,team2_points)

        #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

        team1_scores_list.append(team1_score)
        team2_scores_list.append(team2_score)

        team1_total_points += team1_points
        team2_total_points += team2_points

        if(team1_score > team2_score):
            team1_rubbers +=1
            team1_rubbers_list.append(1)
            team2_rubbers_list.append(0)
        elif(team2_score > team1_score):
            team2_rubbers +=1
            team2_rubbers_list.append(1)
            team1_rubbers_list.append(0)

        else:
            raise SystemExit('issue1:'+__file__+' line number: '+str(inspect.stack()[0][2]))

        team1_scores += team1_score
        team2_scores += team2_score

        #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

    if(team1_rubbers > team2_rubbers):
        team1_bonus_point += 1
    elif(team2_rubbers > team1_rubbers):
        team2_bonus_point += 1
    else:
        raise SystemExit('issue2:'+__file__+' line number: '+str(inspect.stack()[0][2]))

    # print('team1_rubbers,team2_rubbers=',team1_rubbers,team2_rubbers)
    # print('team1_bonus_point,team2_bonus_point=',team1_bonus_point,team2_bonus_point)
    # print('team1_total_points,team2_total_points=',team1_total_points,team2_total_points)

    team1_total_score = sum(team1_scores_list) + team1_rubbers + team1_bonus_point
    team2_total_score = sum(team2_scores_list) + team2_rubbers + team2_bonus_point

    #print('team1_total_score,team2_total_score=',team1_total_score,team2_total_score)

    if((team1_total_score + team2_total_score) != maximum_match_points): \
        raise SystemExit('(team1_total_score + team2_total_score) != maximum_match_points:'+__file__+' line number: '+str(inspect.stack()[0][2]))
    if(team1_total_score > team2_total_score):
        print(CRED+'Team A/B wins over Team X/Y.'+CEND)
    elif(team1_total_score < team2_total_score):
        print(CRED+'Team X/Y wins over Team A/B.'+CEND)
    else:
        raise SystemExit('issue3:'+__file__+' line number: '+str(inspect.stack()[0][2]))

    # empty_match = ['11','11','11','11','11']
    # empty_match = [' ',' ',' ',' ',' ']
    # empty_match = [' ',' ',' ',' ',' ']
    # empty_summary = [' ',' ',' ',' ']
    # summary = [' ',' ',' ',' ']

    team1_summary = [sum(team1_scores_list),team1_rubbers,team1_bonus_point,team1_total_score]
    team2_summary = [sum(team2_scores_list),team2_rubbers,team2_bonus_point,team2_total_score]

    # game1_AB = game2_AB = game3_AB = game4_AB = game5_AB = game6_AB = game7_AB = empty_match
    # game1_XY = game2_XY = game3_XY = game4_XY = game5_XY = game6_XY = game7_XY = empty_match

    #print('team1_scores_list,team2_scores_list=',team1_scores_list,team2_scores_list)

    match1_AB,match2_AB,match3_AB,match4_AB,match5_AB, \
    match1_XY,match2_XY,match3_XY,match4_XY,match5_XY, \
    = populate_scores(diag, scores_whole_match)

    #print('match1_AB=',match1_AB)

    match_AB = [match1_AB,match2_AB,match3_AB,match4_AB,match5_AB]
    match_XY = [match1_XY,match2_XY,match3_XY,match4_XY,match5_XY]

    #print('match_AB=',match_AB)

    match_AB_T = np.array(match_AB).T.tolist()
    match_XY_T = np.array(match_XY).T.tolist()

    #print('match_AB_T=',match_AB_T)

    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))
    
    if(number_of_games_per_match == 7):
        team_sheet_df = pd.DataFrame({ \
                            'TeamA/B: '+team1 : ['Player1: '+team1_player1, 'Player2: '+team1_player2, 'Player2: '+team1_player2, 'Player1: '+team1_player1, 'Doubles'], \
                            'GAME 1,' : match_AB_T[0], \
                            '2,' : match_AB_T[1], \
                            '3,' : match_AB_T[2], \
                            '4,' : match_AB_T[3], \
                            '5,' : match_AB_T[4], \
                            '6,' : match_AB_T[5], \
                            '7,' : match_AB_T[6], \
                            'TeamX/Y: '+team2: ['Player1: '+team2_player1, 'Player2: '+team2_player2, 'Player1: '+team2_player2, 'Player2: '+team2_player1, 'Doubles'], \
                            'GAME 1' : match_XY_T[0], \
                            '2' : match_XY_T[1], \
                            '3' : match_XY_T[2], \
                            '4' : match_XY_T[3], \
                            '5' : match_XY_T[4], \
                            '6' : match_XY_T[5], \
                            '7' : match_XY_T[6], \
                            'G A/B' : team1_scores_list, \
                            'G X/Y' : team2_scores_list, \
                            'R A/B' : team1_rubbers_list, \
                            'R X/Y' : team2_rubbers_list, \
                          })
    elif(number_of_games_per_match == 3):
        team_sheet_df = pd.DataFrame({ \
                            'TeamA/B: '+team1 : ['Player1: '+team1_player1, 'Player2: '+team1_player2, 'Player2: '+team1_player2, 'Player1: '+team1_player1, 'Doubles'], \
                            'GAME 1,' : match_AB_T[0], \
                            '2,' : match_AB_T[1], \
                            '3,' : match_AB_T[2], \
                            'TeamX/Y: '+team2: ['Player1: '+team2_player1, 'Player2: '+team2_player2, 'Player1: '+team2_player2, 'Player2: '+team2_player1, 'Doubles'], \
                            'GAME 1' : match_XY_T[0], \
                            '2' : match_XY_T[1], \
                            '3' : match_XY_T[2], \
                            'G A/B' : team1_scores_list, \
                            'G X/Y' : team2_scores_list, \
                            'R A/B' : team1_rubbers_list, \
                            'R X/Y' : team2_rubbers_list, \
                          })
    else:
        raise SystemExit('maximum_match_points only 41/21.'+__file__+' line number: '+str(inspect.stack()[0][2]))  

    summary_df = pd.DataFrame({ \
                               'Summary': ['Games', 'Rubbers', 'Bonus Pt', 'Total Pts'], \
                               'A/B': team1_summary, \
                                'X/Y': team2_summary \
                              })

    return(team_sheet_df, summary_df) # end of match_team_summary

################################################################################

def update_team_rank(diag, team_sheet_df, summary_df, team_rank, number_of_games_per_match, number_of_matches_per_match):
    
    '''
    Creator: Mark Collier
    Last Modified: 22 August 2019
    
    update team ranking based on team_sheet_df and summary_df dataframes.
    '''
    import pandas as pd
    from IPython.display import display
    
    header = team_sheet_df.keys()

    if(diag): print('header=',header)
    
    if(diag): display(team_sheet_df)
    
    #round_df = main_df.loc[main_df['Round'] == ROUND]

    #need to improve on this, should be able to pull out info. in more general way:
    if(number_of_games_per_match==7):
        teamA =header[0].split(':')[2].strip() #replace(' ', '')
        teamB =header[8].split(':')[2].strip() #replace(' ', '')
    elif(number_of_games_per_match==3):
        teamA =header[0].split(':')[2].strip() #replace(' ', '')
        teamB =header[4].split(':')[2].strip() #replace(' ', '')
    else:
        raise SystemExit('number_of_games_per_match only 3/7 currently:'+__file__+' line number: '+str(inspect.stack()[0][2]))
    
    if(diag): print('teamA=',teamA)
    if(diag): print('teamB=',teamB)

    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))
    
    teamA_points = summary_df['A/B'].values[-1]
    teamB_points = summary_df['X/Y'].values[-1]

    if(diag): print('teamA_points=',teamA_points)
    if(diag): print('teamB_points=',teamB_points)

    for cnt,team in enumerate((teamA,teamB,)):
        entry = team_rank[team]

        #print('entry=',entry)
        entry[0] += 1

        if(cnt==0):
            entry[1] += teamA_points
            entry[2] += teamB_points
        else:
            entry[1] += teamB_points
            entry[2] += teamA_points

        #print('entry=',entry)
        team_rank[team] = entry

    return(team_rank) #end of update_team_rank

################################################################################

def update_player_rank(diag, team_sheet_df, player_rank, number_of_games_per_match, number_of_matches_per_match):
    '''
    Creator: Mark Collier
    Last Modified: 22 August 2019
    
    update player leader board based on team_sheet_df dataframe.
    '''
    import pandas as pd
    
    #need to improve on this, should be able to pull out info. in more general way:
    if(number_of_games_per_match==7):
        teamAB_players_tmp = team_sheet_df.iloc[:,0].values
        teamXY_players_tmp = team_sheet_df.iloc[:,8].values
    elif(number_of_games_per_match==3):
        teamAB_players_tmp = team_sheet_df.iloc[:,0].values
        teamXY_players_tmp = team_sheet_df.iloc[:,4].values
    else:
        raise SystemExit('number_of_games_per_match only 3/7 currently:'+__file__+' line number: '+str(inspect.stack()[0][2]))
        
    #teamAB_players_tmp = team_sheet_df.iloc[:,0].values
    #teamXY_players_tmp = team_sheet_df.iloc[:,8].values
    #teamXY_players_tmp = team_sheet_df.iloc[:,4].values
    #print('teamAB_players=',teamAB_players)

    teamAB_players = []
    for player in teamAB_players_tmp[0:-1]:
        teamAB_players.append( player.split(':')[1].strip() )

    teamXY_players = []
    for player in teamXY_players_tmp[0:-1]:
        teamXY_players.append( player.split(':')[1].strip() )

    if(diag): print('teamAB_players=',teamAB_players)
    if(diag): print('teamXY_players=',teamXY_players)

    #need to improve on this, should be able to pull out info. in more general way:
    if(number_of_games_per_match==7):
        teamAB_results = team_sheet_df.iloc[:,16][0:-1].values
        teamXY_results = team_sheet_df.iloc[:,17][0:-1].values
    elif(number_of_games_per_match==3):
        teamAB_results = team_sheet_df.iloc[:,9][0:-1].values
        teamXY_results = team_sheet_df.iloc[:,10][0:-1].values
    else:
        raise SystemExit('number_of_games_per_match only 3/7 currently:'+__file__+' line number: '+str(inspect.stack()[0][2]))
        
    if(diag): print('teamAB_results=',teamAB_results)
    if(diag): print('teamXY_results=',teamXY_results)

    if(diag): print('player_rank=',player_rank)

    for cnt,player in enumerate(teamAB_players):
        if(diag): print('player=',player)
        entry = player_rank[player]
        entry[0] = entry[0] + teamAB_results[cnt]
        entry[1] = entry[1] + teamXY_results[cnt]
        entry[2] = entry[2] + teamAB_results[cnt] + teamXY_results[cnt]
        if(diag): print('entry=',entry)
        player_rank[player] = entry

    for cnt,player in enumerate(teamXY_players):
        entry = player_rank[player]
        entry[0] = entry[0] + teamXY_results[cnt]
        entry[1] = entry[1] + teamAB_results[cnt]
        entry[2] = entry[2] + teamXY_results[cnt] + teamAB_results[cnt]
        #print('entry=',entry)
        player_rank[player] = entry

    return(player_rank) #end of update_player_rank

################################################################################

def reset_team_player_rank(diag, section_team_composition_df):
    '''
    Creator: Mark Collier
    Last Modified: 16 August 2019
    
    reset team and player leader board based on section_team_composition_df dataframe.
    '''
    import pandas as pd

    team_rank = {}
    for team in section_team_composition_df['Team Name'].values:
        team_rank[team] = [0,0,0]

    player_rank = {}
    for player in section_team_composition_df['Player 1'].values:
        #print('aaa'+player+'bbb')
        player_rank[player] = [0,0,0]
    for player in section_team_composition_df['Player 2'].values:
        #print('aaa'+player+'bbb')
        player_rank[player] = [0,0,0]
        
    return(team_rank, player_rank) #end of reset_team_player_rank

################################################################################

def print_player_table(diag, player_table, section, html_file):
    '''
    Creator: Mark Collier
    Last Modified: 23 August 2019
    
    print player leader board dataframe.
    '''
    from IPython.display import display
    import pandas as pd

    won,lost,total = [],[],[]
    for player in list(player_table.keys()):
        #print(player_table[player])
        won.append(player_table[player][0])
        lost.append(player_table[player][1])
        total.append(player_table[player][2])
    player_table_df = pd.DataFrame({ \
                                    'Player': list(player_table.keys()), \
                                    'Section': [section] * len(list(player_table.keys())), \
                                    'Won': won, \
                                    'Lost': lost, \
                                    'Total': total, \
                                   })

    display(player_table_df.sort_values(by='Won', ascending=False))

    a = append_df_to_html(diag, player_table_df, html_file)

    #player_table_df.to_html('player_table_df.html', escape=False)

    return() # end of print_player_table

################################################################################

def print_team_table(diag, team_table, section, html_file):
    '''
    Creator: Mark Collier
    Last Modified: 23 August 2019
    
    print team leader board dataframe.
    '''
    from IPython.display import display
    import pandas as pd
    
    rounds,won,lost = [],[],[]
    for team in list(team_table.keys()):
        #print(team_table[team])
        rounds.append(team_table[team][0])
        won.append(team_table[team][1])
        lost.append(team_table[team][2])
    team_table_df = pd.DataFrame({ \
                                    'Team': list(team_table.keys()), \
                                    'Section': [section] * len(list(team_table.keys())), \
                                    'Rounds': rounds, \
                                    'Won': won, \
                                    'Lost': lost, \
                                   })

    display(team_table_df.sort_values(by='Won', ascending=False))

    a = append_df_to_html(diag, team_table_df, html_file)

    #team_table_df.to_html(html_dir+'/'+'team_table_df.html', escape=False)

    return() # end of print_player_table

################################################################################

def string_list_to_integer_list(diag, list_string):
    '''
    Creator: Mark Collier
    Last Modified: 16 August 2019
    
    '''
    list_integer = []
    for cnt in range(len(list_string)):
        try:
            list_integer.append( int(list_string[cnt]))
        except:
            return()
        
    return(list_integer) #end of string_list_to_integer_list

################################################################################

def keyboard_entry(diag, entry, number_of_games_per_match, number_of_matches_per_match):
    '''
    Creator: Mark Collier
    Last Modified: 16 August 2019
    
    Take keyboard entry, will return exception if entry does not follow expected conventions.
    Inputs:
    entry:
    
    Outputs:
    list of integers padded and length 2 e.g. [[11,11,11,11,0,0,0], [9,9,9,9,9,0,0]]
    '''
    
    #think this can be done generally with int(number_of_games_per_matchmonth+1/4):
#     if(number_of_games_per_match==7):
#         minimum_values = 4
#     elif(number_of_games_per_match==3):
#         minimum_values = 2
#     else:
#         raise Exception('Exception8')

    minimum_values = minimum_games_in_match(diag, number_of_games_per_match)

    j = entry.split(':')
    k1 = string_list_to_integer_list(diag, j[0].split(','))
    k2 = string_list_to_integer_list(diag, j[1].split(','))    

    if(diag): print('k1=',k1)
    if(diag): print('k2=',k2)
        
    if(len(k1) != len(k2)):
        print('keyboard_entry: len(k1) != len(k2).')
        raise Exception('Exception1')

    for cnt in range(len(k1)):
        if(k1[cnt] < 11 and k2[cnt] < 11):
            print('k1[cnt] < 11 and k2[cnt] < 11.')
            raise Exception('Exception4')

    for cnt in range(len(k1)):
        if(k1[cnt] == k2[cnt]):
            print('k1[cnt] == k2[cnt].')
            raise Exception('Exception7')
            
    for cnt in range(len(k1)):
        if(k1[cnt] > k2[cnt]):
            if(k1[cnt] - k2[cnt] < 2):
                print('k1[cnt] > k2[cnt] & k1[cnt] - k2[cnt] < 2.')
                raise Exception('Exception5')
        if(k2[cnt] > k1[cnt]):
            if(k2[cnt] - k1[cnt] < 2):
                print('k2[cnt] > k1[cnt] & k2[cnt] - k1[cnt] < 2.')
                raise Exception('Exception6')
                
        #print(cnt, k1[cnt]-k2[cnt])
        #return(None)
        #raise SystemExit('keyboard_entry: len(k1) != len(k2):'+__file__+' line number: '+str(inspect.stack()[0][2]))
    
    if((len(k1) < minimum_values) or (len(k2) < minimum_values )):
        print('keyboard_entry: (len(k1) < minimum_values) or (len(k2) < minimum_values ).')
        raise Exception('Exception2')
        #raise SystemExit('keyboard_entry: (len(k1) < minimum_values) or (len(k2) < minimum_values ):'+__file__+' line number: '+str(inspect.stack()[0][2]))

    if((len(k1) > number_of_games_per_match) or (len(k2) > number_of_games_per_match )):
        print('keyboard_entry: (len(k1) > number_of_games_per_match) or (len(k2) > number_of_games_per_match ).')
        raise Exception('Exception3')
        #raise SystemExit('keyboard_entry: (len(k1) > number_of_games_per_match) or (len(k2) > number_of_games_per_match ):'+__file__+' line number: '+str(inspect.stack()[0][2]))
   
    if(len(k1) < number_of_games_per_match):
        k1_old = k1
        for k in range(number_of_games_per_match-len(k1_old)):
            k1 += [0]

    if(len(k2) < number_of_games_per_match):
        k2_old = k2
        for k in range(number_of_games_per_match-len(k2_old)):
            k2 += [0]
            
    if(diag): print(k1)
    if(diag): print(k2)

    return([k1] + [k2]) #end of keyboard_entry

################################################################################

def live_match(diag, main_df, number_of_games_per_match, number_of_matches_per_match, json_directory, validated_json_directory, json_orient):
    '''
    Creator: Mark Collier
    Last Modified: 22 August 2019
    
    This is run on match night to capture results into json file, it loops continuously.
    
    Will need to modify to add other features to json files, for example:
    1. date of creation
    2. user name
    3. flag whether been checked by coordinator
    
    Might need to move validated files to another area, and provide protection for the files.

    This function sets the validation components of the dataframe to defaults, e.g. 'NO'.
    
    Inputs:
    main_df: the main data frame, currently called full_table_df
    number_of_games_per_match: usually a number like 3, 5 or 7.
    number_of_matches_per_match: usually a number like 5, 7 or 11.
    json_directory:
    validated_json_directory:
    json_orient style of formatting, variable used to be consistent across all functions.
    
    Outputs:
    
    json text file of convention, e.g., cdtta_json/section_01_round_01_match_01.json
    '''
    
    import datetime
    import pandas as pd
    from IPython.display import display
    import os.path
    import string
    import inspect
    
    CRED = '\033[91m'
    CGREEN = '\033[32m'
    CEND = '\033[0m'

    pd.set_option('display.max_columns', 30)
    pd.set_option('display.max_rows', 400)
    pd.set_option('display.max_colwidth', -1)
    
    print('Entering a 0 (zero) at first character for any of the following keyboard entry will reset to beginning.')
    print('Only a file will be written if each section is answered appropriately.')
    
    rounds = main_df['Round']
    sections = main_df['Section']
    
    for n in range(99):
        try:
            PERSON_ENTERING_DATA = input(CRED+'Enter your full name (person entering match results) - alpha & spaces allowed: '+CEND)
        except:
            print(CGREEN+'Try again.'+CEND)
            continue
            
        #print('xxx'+PERSON_ENTERING_DATA+'xxx')
        #print(PERSON_ENTERING_DATA.isdigit())

        if(PERSON_ENTERING_DATA.isdigit() and int(PERSON_ENTERING_DATA) == 0):
            print(CRED+'Exiting...'+CEND)
            exit(0)
        elif(PERSON_ENTERING_DATA == ''):
            print(CGREEN+'No blanks, try again.'+CEND)
            continue
        elif(not PERSON_ENTERING_DATA.replace(' ', '').isalpha()):
            print(CGREEN+'Only alphabet letters,  try again.'+CEND)
            continue
        else:
            break
    
    TODAYS_DATE_TIME = datetime.datetime.today().strftime('YYYY-MM-DD=%Y-%m-%d HH-MM-SS=%H-%M-%S')
    
    print(CGREEN+'PERSON ENTERING DATA='+PERSON_ENTERING_DATA+' DATE/TIME (YYYY-MM-DD HH:MM:SS)='+str(TODAYS_DATE_TIME)+CEND)

    for n in range(99):
        try:
            ROUND = int(input('Round '+str(min(rounds))+'-'+str(max(rounds))+': '))
        except ValueError:
            print(CGREEN+'Incorrect type, try again.'+CEND)
            continue
        if(ROUND == 0): return(0)
        
        if(ROUND < min(rounds) or ROUND > max(rounds)):
            continue
        else:
           break

    round_df = main_df.loc[main_df['Round'] == ROUND]

    display(round_df)

    for n in range(99):
        try:
            section = int(input('Section '+str(min(sections))+'-'+str(max(sections))+': '))
        except ValueError:
            print(CGREEN+'Incorrect type, try again.'+CEND)
            continue
        if(section == 0): return(0)
        if(section < min(sections) or section > max(sections)):
            continue
        else:
           break

    section_df = round_df.loc[round_df['Section'] == section]

    display(section_df)

    matches = section_df['Match']

    for n in range(99):
        try:
            match = int(input('Match '+str(min(matches))+'-'+str(max(matches))+': '))
        except ValueError:
            print(CGREEN+'Incorrect type, try again.'+CEND)
            continue
        if(match == 0): return(0)
        if(match < min(matches) or match > max(matches)):
            continue
        else:
           break

    match_extract_df = section_df.loc[round_df['Match'] == match]

    display(match_extract_df)

    #output_directory = 'cdtta_json'
    #keep data and meta (scalar) data in separate files...
    
    output_data_file = 'section_'+'{0:02d}'.format(section)+'_round_'+'{0:02d}'.format(ROUND)+'_match_'+'{0:02d}'.format(match)+'_data.json'

    if(os.path.isfile(json_directory+'/'+output_data_file) and os.path.isfile(validated_json_directory+'/'+output_data_file)):
        print(CRED+'Warning: raw & validated output file exist... '+CEND)

    if(os.path.isfile(validated_json_directory+'/'+output_data_file)):
        print(CRED+'Warning: validated output file '+validated_json_directory+'/'+output_data_file+ ' exists.'+CEND)
    
    if(os.path.isfile(json_directory+'/'+output_data_file)):
        print(CRED+'Warning: output file '+json_directory+'/'+output_data_file+ ' exists.'+CEND)
    else:
        print(CGREEN+'Output file=',json_directory+'/'+output_data_file+CEND)

    # def padded_integer_match(diag, keyboard_entry):
    #     '''
    #     '''
    #     j = keyboard_entry.split(':')
    #     #print('j=',j)
    #     k1 = string_list_to_integer_list(diag, j[0].split(','))
    #     k2 = string_list_to_integer_list(diag, j[1].split(','))

    #     return([k1] + [k1]) #end of padded_integer_match
    # j = match1.split(':')
    # if(len(j) != 2):
    #     print('j wrong length')

    table_wooden = match_extract_df['Table'].values[0]
    unique_match = match_extract_df['Unique match'].values[0]
    ROUND = match_extract_df['Round'].values[0]
    section = match_extract_df['Section'].values[0]
    match = match_extract_df['Match'].values[0]
    match_date = match_extract_df['Match Date'].values[0]

    #print('table_wooden_table=',table_wooden)

    team1_player1 = match_extract_df['Team1 Player1'].values.tolist()[0].strip()
    team1_player2 = match_extract_df['Team1 Player2'].values.tolist()[0].strip()

    team2_player1 = match_extract_df['Team2 Player1'].values.tolist()[0].strip()
    team2_player2 = match_extract_df['Team2 Player2'].values.tolist()[0].strip()

    tmp1 = match_extract_df['Team1'].values.tolist()[0]
    tmp2 = match_extract_df['Team2'].values.tolist()[0]

###############################################################################################################

    for n in range(999):
        try:
            QUESTION = input(CRED+'Were there any fill-ins [y/n or 0=break]? '+CEND)
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
        icheck2 = 0
        print('Specify Which players were replaced with a fillin?')
        team1_player1_fillin = input('Team A/B player A [0 = no, "Surname, FirstName"]: '+team1_player1+': ')
        team1_player2_fillin = input('Team A/B player B [0 = no, "Surname, FirstName"]: '+team1_player2+': ')
        team2_player1_fillin = input('Team X/Y player A [0 = no, "Surname, FirstName"]: '+team2_player1+': ')
        team2_player2_fillin = input('Team X/Y player B [0 = no, "Surname, FirstName"]: '+team2_player2+': ')

        if(icheck2 == 0):
            print('You specified fill in but gave no one.')

        if(team1_player1_fillin.isdigit() and int(team1_player1_fillin) == 0):
            team1_player1_fillin = 'NO'

        if(team1_player2_fillin.isdigit() and int(team1_player2_fillin) == 0):
            team1_player2_fillin = 'NO'

        if(team2_player1_fillin.isdigit() and int(team2_player1_fillin) == 0):
            team2_player1_fillin = 'NO'

        if(team2_player2_fillin.isdigit() and int(team2_player2_fillin) == 0):
            team2_player2_fillin = 'NO'

        fillins = [ [[team1_player1_fillin],[team2_player1_fillin]], [[team1_player2_fillin],[team2_player2_fillin]], [[team1_player2_fillin],[team2_player1_fillin]], [[team1_player1_fillin],[team2_player2_fillin]], [['Doubles A/B'],['Doubles X/Y']], ]
    else:
        fillins = [ [['NO'],['NO']], [['NO'],['NO']], [['NO'],['NO']], [['NO'],['NO']], [['NO'],['NO']], ]

    print('fillins=',fillins)

###############################################################################################################

    if(diag): print('tmp1=',tmp1)

    if(tmp1.strip() == 'Team A Dummy' or tmp2.strip() == 'Team B Dummy'):
        print(CRED+'Team A/B Dummy, must be a finals round no entry allowed.'+CEND)
        return(0)

    team1 = match_extract_df['Team1'].values.tolist()[0].strip().split(':')[1]
    team2 = match_extract_df['Team2'].values.tolist()[0].strip().split(':')[1]

    #print(team1)
    #print(team1_player1)

    print('Note Team 1/2 are home/away teams. So order would be:')
    print('Singles: Team 1 player 1 VS. Team 2 player 1')
    print('Singles: Team 1 player 2 VS. Team 2 player 2')
    print('Singles: Team 1 player 2 VS. Team 2 player 1')
    print('Singles: Team 1 player 1 VS. Team 2 player 2')
    print('Doubles: Team 1 VS. team 2')

    print('Enter scores (comma & colon separated) in order from printed match sheet:')

    print('Example 7 game format: PlayerA VS. PlayerB = 11,3,11,13,11 : 9,11,9,11,9')
    print('Example 3 game format: PlayerA VS. PlayerB = 21,21 : 19,19')

    print('7 game format: Must have minimum of 4 integers even if they are 0, e.g. 0,0,0,0 : 11,11,11,11')
    print('3 game format: Must have minimum of 2 integers even if they are 0, e.g. 0,0 : 21,21')

    # dummy1 = '11,3,11,13,11 : 9,11,9,11,9'
    # dummy2 = '11,11,11,11 : 9,9,9,9'
    # dummy3 = '9,9,9,9 : 11,11,11,11'
    # dummy4 = '11,9,11,9,11,9,11 : 9,11,9,11,9,11,9'
    # dummy5 = '19,11,11,9,11 : 17,9,9,11,9'

    for n in range(99):
        dummy1 = input('Singles Match 1/5: ')
        if(dummy1 == '0'): return(0)
        try:
            match1_join = keyboard_entry(diag, dummy1, number_of_games_per_match, number_of_matches_per_match)
            break
        except:
            print('Try again.')
            continue

    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

    for n in range(99):
        dummy2 = input('Singles Match 2/5: ')
        if(dummy2 == '0'): return(0)

        try:
            match2_join = keyboard_entry(diag, dummy2, number_of_games_per_match, number_of_matches_per_match)
            break
        except:
            print('Try again.')
            continue

    for n in range(99):
        dummy3 = input('Singles Match 3/5: ')
        if(dummy3 == '0'): return(0)

        try:
            match3_join = keyboard_entry(diag, dummy3, number_of_games_per_match, number_of_matches_per_match)
            break
        except:
            print('Try again.')
            continue

    for n in range(99):
        dummy4 = input('Singles Match 4/5: ')
        if(dummy4 == '0'): return(0)

        try:
            match4_join = keyboard_entry(diag, dummy4, number_of_games_per_match, number_of_matches_per_match)
            break
        except:
            print('Try again.')
            continue

    for n in range(99):
        dummy5 = input('Doubles Match 5/5: ')
        if(dummy5 == '0'): return(0)
        try:
            match5_join = keyboard_entry(diag, dummy5, number_of_games_per_match, number_of_matches_per_match)
            break
        except:
            print('Try again.')
            continue

    for n in range(999):
        try:
            QUESTION = input(CRED+'Do you want to add any comments to this match [y/n or 0=break]? '+CEND)
        except:
            print('Try again.')
            continue

        if(QUESTION.isdigit() and int(QUESTION) == 0):
            raise SystemExit('function: Exiting Validation.'+__file__+' line number: '+str(inspect.stack()[0][2]))
        elif(QUESTION != 'y' and QUESTION != 'n'):
            print('Only "y" or "n", try again.')
            continue
        else:
            break

    COMMENT = None
    if(QUESTION == 'y'):
        COMMENT = input('Add your one line comment [a \'$\' will add linebreak in the output] :\n')

    #print('COMMENT=',COMMENT)

    #print('match1_join=',match1_join)
    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))
    # match1_join = keyboard_entry(diag, dummy1)
    # match2_join = keyboard_entry(diag, dummy2)
    # match3_join = keyboard_entry(diag, dummy3)
    # match4_join = keyboard_entry(diag, dummy4)
    # match5_join = keyboard_entry(diag, dummy5)

    teamA = match1_join[0] + match2_join[0] + match3_join[0] + match4_join[0] + match5_join[0]
    teamB = match1_join[1] + match2_join[1] + match3_join[1] + match4_join[1] + match5_join[1]

    results = [match1_join, match2_join, match3_join, match4_join, match5_join]

    #print('results=',results)
    #print('len(results)=',len(results))
    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))

    # print(teamA)
    # print(teamB)
    #print('k2=',k2)
    #print('xxx=',xxx)
    #print( pad_score(diag, k1) )
    # _,_ = check_match(diag, k1)
    # _,_ = check_match(diag, k2)
    # _,_ = compare_single_match(diag, k1, k2)

    # teamA = [9,11,9,11,9,11,9, 9,11,9,11,9,11,9, 9,11,9,11,9,11,9, 9,11,9,11,9,11,9, 9,11,9,11,9,11,9]
    # teamB = [11,9,11,9,11,9,11, 11,9,11,9,11,9,11, 11,9,11,9,11,9,11, 11,9,11,9,11,9,11, 11,9,11,9,11,9,11]
    
#     games = [1,2,3,4,5,6,7] * 5 # a repeating sequence.

    games = list(range(1,number_of_games_per_match+1)) * number_of_matches_per_match
    
    team1_player1 = match_extract_df['Team1 Player1'].values.tolist()[0].strip()
    team1_player2 = match_extract_df['Team1 Player2'].values.tolist()[0].strip()

    team2_player1 = match_extract_df['Team2 Player1'].values.tolist()[0].strip()
    team2_player2 = match_extract_df['Team2 Player2'].values.tolist()[0].strip()

    raw_match_df = pd.DataFrame({ \
      'Unique Match' : [unique_match] * number_of_matches_per_match, \
      'Entry Person'       : [PERSON_ENTERING_DATA] * number_of_matches_per_match, \
      'Creation Date/Time' : [TODAYS_DATE_TIME] * number_of_matches_per_match, \
      'Round Match' : [match] * number_of_matches_per_match, \
      'Match' : range(1,number_of_matches_per_match+1), \
      'Round' : [ROUND] * number_of_matches_per_match, \
      'Section' : [section] * number_of_matches_per_match, \
      'Table' : [table_wooden] * number_of_matches_per_match, \
      'Match Date' : [match_date] * number_of_matches_per_match , \
      'TeamA/B X/Y'        : [ [['TeamA/B'],['TeamX/Y']], [['TeamA/B'],['TeamX/Y']], [['TeamA/B'],['TeamX/Y']], [['TeamA/B'],['TeamX/Y']], [['TeamA/B'],['TeamX/Y']], ], \
      'Team Names'         : [ [[team1],[team2]], [[team1],[team2]], [[team1],[team2]], [[team1],[team2]], [[team1],[team2]], ], \

      'PlayerA/B X/Y'      : [ [['Team A/B Player A'],['Team X/Y Player A']], [['Team A/B Player B'],['Team X/Y Player B']], [['Team A/B Player B'],['Team X/Y Player A']], [['Team A/B Player A'],['Team X/Y Player B']], [['Doubles A/B'],['Doubles X/Y']], ], \
      'Player Names'       : [ [[team1_player1],[team2_player1]], [[team1_player2],[team2_player2]], [[team1_player2],[team2_player1]], [[team1_player1],[team2_player2]], [['Doubles A/B'],['Doubles X/Y']], ], \
      'Fillin Playes Names': fillins, \
      'Result'             : results, \
      'Validated'          : ['NO'] * number_of_matches_per_match, \
      'Validated Date/Time': ['NO'] * number_of_matches_per_match, \
      'Validation Person'  : ['NO'] * number_of_matches_per_match, \
   })

#      'Result'             : [ [[11,11,11,11,0,0,0], [3,4,5,6,0,0,0]], [[11,11,11,11,0,0,0], [8,8,8,8,0,0,0]], [[11,11,11,11,0,0,0], [9,8,7,6,0,0,0]], [[13,13,13,13,0,0,0], [11,11,11,11,0,0,0]], [[11,11,11,11,0,0,0], [1,1,1,1,0,0,0]] ], \

    pd.set_option('display.max_columns', 30)
    pd.set_option('display.max_rows', 400)
    pd.set_option('display.max_colwidth', -1)

    display(raw_match_df)
    
    print(CRED+'Writing to json file: '+json_directory+'/'+output_data_file+CEND)

    raw_match_df.to_html(json_directory+'/html/'+'raw_match.html')
    
    raw_match_df.to_json(r''+json_directory+'/'+output_data_file, orient=json_orient)

    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))
    
    tidy_json(diag, r''+json_directory+'/'+output_data_file)

    if(type(COMMENT) != type(None)):
        fhR = open(json_directory+'/'+'README', 'a')
        fhR.write('################################################################################\n')
        fhR.write(datetime.datetime.today().strftime('YYYY-MM-DD=%Y-%m-%d HH-MM-SS=%H-%M-%S\n'))

        for token in COMMENT.split('$'):
            fhR.write(token.strip()+'\n')
        fhR.write('################################################################################\n')
        fhR.close()

    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))
    
    # j_df = pd.read_json(r''+json_directory+'/'+output_file, orient=json_orient)

    # display(j_df)
    return(0) # end of live_match

################################################################################

def minimum_games_in_match(diag, number_of_games_per_match):
    '''
    Creator: Mark Collier
    Last Modified: 16 August 2019   
    
    Inputs:
    number_of_games_per match: (integer)
    Ouputs: (integer), the minimum number of games to be played to finish a match, depends on odd/even number of total games.
    number: 
    '''
    
    if((number_of_games_per_match % 2) == 0): #even
        number = int(number_of_games_per_match/2)+1
    else:
        number = int((number_of_games_per_match+1)/2)
    
    return(number) #end of minimum_games_in_match

################################################################################

def make_draw(diag, all_sections_all_rounds, YYYYMMDD):
    '''
    Creator: Mark Collier
    Last Modified: 19 August 2019
    
    Create a draw (dates, matches in order, per round)
    
    Inputs:
    all_sections_all_rounds: list [[[[ ]]]]
    YYYYMMDD: list of dates corresponding to each round

    Ouputs: list of dataframes: these can be dsiplayed
    '''
    import pandas as pd
    from IPython.display import display
    
    draw_all_df = []
    
    if(diag): print(YYYYMMDD)

    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))        

    if(diag): print('all_sections_all_rounds=',all_sections_all_rounds)

    #########################

    unique_draws = [ all_sections_all_rounds[0].copy() ]

    if(diag): print('unique_draws=',unique_draws)

    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))        

    for cnt,one_section in enumerate(all_sections_all_rounds[1:]):
        if(one_section in unique_draws):
            continue
        else:
            unique_draws += [ one_section ]

    if(diag): print('unique_draws=',unique_draws)
    if(diag): print('len(unique_draws)=',len(unique_draws))

    if(diag): print('all_sections_all_rounds=',all_sections_all_rounds)
    if(diag): print('len(all_sections_all_rounds)=',len(all_sections_all_rounds))

    #########################

    sections_common = [[]] * len(unique_draws)

    if(diag): print('sections_common=',sections_common)

    for cntA,one_draw in enumerate(unique_draws):
        for cntB,one_section in enumerate(all_sections_all_rounds):

            if(one_section == unique_draws[cntA]):
                sections_common[cntA] = sections_common[cntA] + [cntB,]

    if(diag): print('sections_common=',sections_common)

    #########################

    printTEXT = True #will print out to screen summary.
    printTEXT = False
       
    for cntA,section_common in enumerate(sections_common):
        if(printTEXT): print('Sections ', end='')
        for cntB,sss in enumerate(section_common):
            if(cntB == len(section_common)-1):
                if(printTEXT): print(sss+1, end=':\n')

            else:
                if(printTEXT): print(sss+1, end=',')
        for cntC,matches_this_round in enumerate(all_sections_all_rounds[section_common[0]]):
            if(printTEXT): print('round,date,matches=',cntC+1,YYYYMMDD[cntC],matches_this_round)

        one_df = pd.DataFrame({'Round': range(1,len(all_sections_all_rounds[section_common[0]])+1), \
                           'Date' : YYYYMMDD, \
                           'Matches': all_sections_all_rounds[section_common[0]], \
                          })
        
        draw_all_df.append(one_df)
        
        #display(one_df)
    return(draw_all_df) #end make_draw

################################################################################

def tidy_json(diag, input_output_file):
    '''
    Creator: Mark Collier
    Last Modified: 22 August 2019
    
    Minor changes to make the json file more readable.
    
    Inputs:
    input file

    Outputs:
    output_file
    '''
    import inspect

    ifh = open(input_output_file)
    for i,line in enumerate(ifh):

        line = line.replace('},{', '},\n{')
        line = line.replace('[{','[\n{')
        line = line.replace('}]','}\n]')

        if(diag): print(line)
    ifh.close()

    if(True): print('i=',i)

    if(i!=0):
        raise SystemExit('tidy_json: i.ne.0:'+__file__+' line number: '+str(inspect.stack()[0][2]))

    ofh = open(input_output_file, 'w')
    print(line,file=ofh)
    ofh.close()

    return() #end of tidy_json

################################################################################

def reduce_size_to_section_size(diag, tables, tables_per_section):
    '''
    Creator: Mark Collier
    Last Modified: 20 August 2019
    
    Inputs:
    tables
    tables_per_section

    Outputs:
    reduced: a reduced version of tables matching tables_per_section
    '''
    
    if(diag): print('tables=',tables)
    
    reduced = []
    for cnt,tables_this_section in enumerate(tables_per_section):
        if(diag): print('cnt,tables_this_section,tables[cnt]=',cnt,tables_this_section,tables[cnt][0:tables_this_section])
        reduced.append(tables[cnt][0:tables_this_section])
    
    return(reduced) #end of reduce_size_to_section_size

################################################################################

def generate_wooden_tables_per_section(diag, number_teams_per_section):
    '''
    Creator: Mark Collier
    Last Modified: 20 August 2019
    
    Inputs:
    number_teams_per_section e.g. [4, 6, 6, 6, 6, 4]
    wooden_tables_per_section

    Outputs:
    wooden_tables per section e.g. [2, 3, 3, 3, 3, 2]
    '''
    
    wooden_tables_per_section = []
    for teams in number_teams_per_section:
        wooden_tables_per_section.append(int(teams/2))
    return(wooden_tables_per_section) #end of generate_wooden_tables_per_section

################################################################################

def automatic_wooden_table_allocation(diag, number_teams_per_section, number_rounds, groups_of_n, wooden_table_max, wooden_table_init):
    '''
    Creator: Mark Collier
    Last Modified: 20 August 2019
    
    Inputs:
    number_teams_per_section e.g. [4, 6, 6, 6, 6, 4]
    number_rounds e.g. 10
    groups_of_n e.g. 3, this number is the largest section size
    wooden_table_max e.g. 22, this is the largest table number that can be used
    wooden_table_init e.g. 11, this is the first table to start to use, 11 corresponds to the first table in the new room.

    Outputs:
    list of [[[ section, round ]]]
    
    Note that at the moment this function will always give a result, however, it can become erroneous in
    situations where the number of sections and teams per section become too great, as the number of tables is
    the limiting factor.
    
    For this reason, I will add code to ensure that unique table numbers are derived, else an error will be reported.
    '''
    
    import inspect
    
    wooden_tables_per_section = generate_wooden_tables_per_section(diag, number_teams_per_section)
    
    wooden_tables_basic_round = []
    for section0 in range(len(number_teams_per_section)):

        if(diag): print('section0,wooden_table_init=',section0,wooden_table_init)

        wooden_table_section = []
        for wooden_table in range(groups_of_n):
            wooden_table_now = wooden_table_init + wooden_table

            if(wooden_table_now > wooden_table_max):
                wooden_table_now = wooden_table_now - wooden_table_max

            wooden_table_section.append(wooden_table_now)

        if(diag): print('before: wooden_table_section=',wooden_table_section)

        icheck = 0
        for n in range(groups_of_n-1):
            if(wooden_table_section[n] > wooden_table_section[n+1]):
                print('wooden_table_section[n] > wooden_table_section[n+11]')
                icheck +=1

        if(diag): print('icheck=',icheck)

        if(icheck!=0):
            imin = min(wooden_table_section)
            if(diag): print('imin=',imin)

            for n in range(gropus_of_n):
                wooden_table_section[n] = imin+n
            wooden_table_init = imin + gropus_of_n
        else:
            wooden_table_init += groups_of_n

        if(wooden_table_init > wooden_table_max):
            wooden_table_init = wooden_table_init - wooden_table_max

        if(diag): print('after: wooden_table_section=',wooden_table_section)

        wooden_tables_basic_round.append(wooden_table_section)

    if(diag): print('wooden_tables_basic_round=',wooden_tables_basic_round)

    n_rounds = wooden_tables_basic_round *12 #choose some big number probably nrounds+1 or nrounds+2

    #print('n_rounds=',n_rounds)

    all_rounds_wooden_table_allocation = []

    number_sections = len(number_teams_per_section)

    smin0 = 0
    smax0 = number_sections-1
    for round0 in range(number_rounds):

        if(round0>0):
            smin0 += number_sections-1
            smax0 += number_sections-1

        #print('round0,n_rounds[smin0:smax0+1]=',round0,n_rounds[smin0:smax0+1])

        current_round_wooden_table_allocation = reduce_size_to_section_size(diag, n_rounds[smin0:smax0+1], wooden_tables_per_section)

        xycheck = []
        for x in current_round_wooden_table_allocation:
            for y in x:
                xycheck.append(y)
            

        if(len(xycheck) != len(list(set(xycheck)))):
            print('current_round_wooden_table_allocation=',current_round_wooden_table_allocation)
            print('xycheck=',xycheck)
            raise SystemExit('automatic_wooden_wooden_table_allocation: dupliate wooden_tables, reduce sections and/or section sizes:'+__file__+' line number: '+str(inspect.stack()[0][2]))
            
        all_rounds_wooden_table_allocation.append(current_round_wooden_table_allocation)
        if(diag): print('round0,current_round_wooden_table_allocation=',CRED+str(round0)+CEND,current_round_wooden_table_allocation)

    if(diag): print('all_rounds_wooden_table_allocation=',all_rounds_wooden_table_allocation)
    
    #reorder array to be as required:
    all_sections_all_rounds_wooden_tables = []
    for section0 in range(number_sections): 
        j = []
        for round0 in range(number_rounds):
            j.append( all_rounds_wooden_table_allocation[round0][section0] )
        all_sections_all_rounds_wooden_tables.append(j)

    if(diag): print('all_sections_all_rounds_wooden_tables=',all_sections_all_rounds_wooden_tables)

    return(all_sections_all_rounds_wooden_tables) # end of automatic_wooden_table_allocation

################################################################################

def just_file_name(diag, full_name):
    '''
    Creator: Mark Collier
    Last Modified: 21 August 2019

    Extract file name from end of a directory/filename path.
    
    Inputs:

    Outputs:
    '''
    file_name = full_name.split('/')[-1]
    return(file_name) #end of just_file_name

################################################################################

def section_ROUND_match_from_json_filename(diag, file_name):
    '''
    Creator: Mark Collier
    Last Modified: 21 August 2019
    
    Extract match integers from a match json input file name.
    
    Inputs:

    Outputs:
    '''
    input_json_file = just_file_name(diag, file_name)
    if(diag): print('section_ROUND_match_from_json_file: input_json_file=', input_json_file)

    tokens = input_json_file.split('_')
    if(diag): print(tokens)

    section = int(tokens[1])
    ROUND = int(tokens[3])
    match = int(tokens[5])
    
    #raise SystemExit('STOP!:'+__file__+' line number: '+str(inspect.stack()[0][2]))
    
    return(section, ROUND, match) #end of section_ROUND_match_from_json_file

################################################################################

def pennant_names(diag, what, pennant):
    '''
    Creator: Mark Collier
    Last Modified: 21 August 2019
    
    Inputs:

    Outputs:
    '''
    import inspect

    if(what == 'Team_Names'):
       if(pennant == 'Morning_Morning'):
             return(['Bayswater1', 'Croydon1', 'Kilsyth1', 'Lilydale1', 'Ringwood1', 'ByeS1', 'Croydon2', 'Bayswater2', 'Kilsyth2', 'Ringwood2', 'Mooroolbark', 'Olinda1', 'Ringwood3', 'Bayswater3', 'Olinda2', 'Croydon3', 'Kilsyth3', 'ByeS3', 'Olinda3', 'Bayswater4', 'Ringwood4', 'Lilydale2'])
       elif(pennant == 'Thursday_Morning'):
             return(['Bayswater1', 'Croydon1', 'Kilsyth1', 'Lilydale1', 'Ringwood1', 'ByeS1', 'Croydon2', 'Bayswater2', 'Kilsyth2', 'Ringwood2', 'Mooroolbark', 'ByeS2', 'Ringwood3', 'Bayswater3', 'Olinda1', 'Croydon3', 'Kilsyth3', 'ByeS3', 'Olinda2', 'Croydon4', 'Bayswater4', 'Lilydale2', 'Ringwood4', 'ByeS4'])
       elif(pennant == 'Wednesday_Night'):
             return(['Mooroolbark Bendigo', 'Kilsyth Gin', 'Wonga Park', 'Ferntree Gully', 'The Basin', 'Knox', 'Belgrave', 'Tooronga Zoo', 'Montrose Jones', 'Kilsyth', 'Bayswater Roy', 'North Ringwood', 'Alamein', 'Mitcham', 'Kilsyth', 'Croydon', 'Bayswater', 'Wantirna', 'Donvale', 'Knoxfield', 'Vermont South', 'Studfield', 'Tooronga Zoo', 'Kilsyth', 'Scoresby', 'Boronia', 'Forest Hill', 'North Ringwood', 'Scoresby', 'Vermont', 'Yellingbo', 'Croydon Hills', 'Vermont', 'Badger Creek', 'Blackburn', 'Box Hill', 'Scoresby', 'Kilsyth', 'Coldstream', 'Wantirna', 'Heathmont', 'Forest Hill', 'Ringwood', 'Lilydale', 'Kilsyth', 'Warburton'])
       elif(pennant == 'Thursday_Night'):
             return(['Bandicoot', 'Bilby', 'Brolga', 'Cassowary', 'Cockatoo', 'Crocodile', 'Dingo', 'Dolphin', 'Dugong', 'Echidna', 'Emu', 'Fairy Penguin', 'Flying Fox', 'Fur Seal', 'Galah', 'Goanna', 'Ibis', 'Kangaroo', 'Koala', 'Kookaburra', 'Lizard', 'Lyrebird', 'Magpie', 'Numbat', 'Platypus', 'Possum', 'Quokka', 'Quoll', 'Seal', 'Sugar Glider', 'Tasmanian Devil', 'Turtle'])
       else:
            raise SystemExit('pennant_names: "pennant" can be only "Morning_Morning/Thursday_Mornin/Wednesday_Night/Thursday_Night":'+__file__+' line number: '+str(inspect.stack()[0][2]))

    elif(what == 'Player_Names'): 
        if(pennant == 'Morning_Morning'):
             return(['Lothar Pilz', 'Pam Tait', 'John Keating', 'Steve Aitken', 'Tony Brincat', 'ByeS1A', 'ByeS1B', 'John Kelly', 'Brian Zschech', 'Colin Geraghty', 'Bob Marsden', 'Rodney Matthews', 'Ray Butcher', 'Marcell Asselman', 'Paul Colcheedas', 'Neil Roberts', 'Graeme Ireland', 'Kevin Packer', 'Peter Rial', 'Barney Zwartz', 'Andrew Bialecki', 'Clive Hawes', 'Jim Goodwin', 'Richard Hince', 'Robert Varsallo', 'Graham Fly', 'Robert Priest', 'Sandra Rowe', 'Bruce Hird', 'ByeS3A', 'ByeS3B', 'Lyn Gilson', 'Jimmy McHale', 'Fumiko Suwama', 'Arthur Rich', 'Jim Barden', 'Glen Swatek', 'Bert Grotaers', 'Margaret Thomas', 'Katalin Szabo', 'Max Edwards', 'Colin Bateman', 'Helga Spitzer', 'Adele Rooke'])
        elif(pennant == 'Thursday_Morning'):
             return(['Bob Marsden', 'Fred Arthurton', 'Neil Roberts', 'Graeme Ireland', 'Barney Zwartz', 'ByeS1A', 'ByeS1B', 'Peter Rial', 'Sandra Rowe', 'Louis Markov', 'Louis Markov', 'Clive Hawes', 'Bruce Hird', 'Rob Cameron', 'Peter Roberts', 'Jimmy Mchale', 'Laurie Uglow', 'Paul Stitzel', 'ByeS2A', 'ByeS2B', 'Graham Woodfield', 'Hans Gaven', 'Dylan Thorrogood', 'Ian Stockdale', 'Jim Barden', 'Fumiko Suwama', 'Ruth Menzies', 'Margaret Thomas', 'Katalin Szabo', 'Joe Britton', 'ByeS3A', 'ByeS3A', 'Roselyn Beatty', 'Marilyn Mcfarland', 'Dorothy Markly', 'Max Edwards', 'Glen Swatek', 'Bob Byran', 'Colin Bateman', 'Rhonda Addicott', 'Pat Searle', 'Joan Schofield', 'ByeS4A', 'ByeS4B', 'Lily Stevenson', 'Sue Foster', 'Ken Merry', 'Margaret Hopstaken', 'Helga Spitzer' ])
        elif(pennant == 'Wednesday_Night'):
             return(['Taylor, Ben', 'Gin, Darian', 'Ghani, Shahid', 'Waterman, Keith', 'Smith, Jakob', 'D\’Amico, Scott', 'Menzies, Andrew', 'Datta, Raj', 'Nemenyi, Endre', 'Brindley, Aviva', 'Gardner, Mackenzie', 'Rodriguez, JC', 'Paul, Liviston', 'Majumdar, Sourav', 'Jones, Warren', 'Gormann, Ben', 'Roy, Phillip', 'Evans, Richard P', 'Evans, Bruce', 'Kwan, Justin', 'Smith, Greg', 'Cunningham, Bobby', 'Spizzica, Tony', 'Hayden, Ryan', 'Maranan, Jesse', 'Jefimenko, Walter', 'Hewitt, Gerard', 'Qin, Allen', 'Tsao, Justin', 'Hayes, Simon', 'Cauchi, Travis', 'Cheung, Adrian', 'Simons, Shane', 'Hayden, Shane', 'Cung, Robert', 'Neil, Alan', 'Khan, Inaaya', 'Brincat, Tony', 'Stewart, Craig', 'Julian, Rebecca', 'Marsden, Bob', 'Perkins, Shaun', 'Bignell, Quentin', 'Jafarzadeh, Jason', 'Perkins, David', 'Morella, Alex', 'Eddy, Chris', 'McConnell, Nick', 'Mehravar, Hassan', 'Evans, Shaun', 'Chew, Valentine', 'Woodlock, Ron', 'Menz, Garry', 'Petch, David', 'Herweynen, Ed', 'Brown, Andrew', 'Hayden, Chris', 'Jones, Cameron', 'Hassanikhoo, Hamid', 'Conroy, Mark', 'Van Koll, Marinus', 'Wachter, Matt', 'Floyd, Dannie', 'Atalla, Maged', 'Byrne, Jason', 'Evans, Steve', 'Shamakhy, Alireza', 'Cao, Tingting', 'Gray, Kaitlyn', 'Anderson, Caleb', 'Puts, Arnold', 'Balsillie, Terry', 'Thompson, Nick', 'Safir, Amir', 'McGuire, Johnathon', 'Morales, Orangel', 'Martus, Maria', 'Anderson, Daniel', 'Rowland, David', 'Chegini, Fereshteh'])
        elif(pennant == 'Thursday_Night'):
             return(['Bhiwarkar, Mangesh', 'Keating, John', 'Pilz, Lothar', 'Harris, Lachlan', 'Weighell, Michael', 'Harrison, Leigh', 'Collier, Mark', 'Bellamy, Graham', 'Signor, Dominic', 'Goodridge, Robert', 'Kung, Bernard', 'Signor, Sergio', 'Dyer, Terry', 'Goepfert, Paul', 'Holt, Ben', 'Straughair, Thomas', 'Talolin, Nick', 'Oldham, Cameron', 'Probyn-Smith, Garth', 'Jung, Tad', 'Ryan, Paul', 'Zeng, Jimmy', 'Jefimenko, Paul', 'Morgan, Shane', 'Lee, Johnson', 'Mcerlain, Peter', 'Powell, John', 'Howse, Kalan', 'Mendes, Champ', 'Mazzaferri, Michael', 'Salgueiro, Fernando', "O'Regan, Brendan", 'Zdimirovic, Zoltan', 'Goodwin, Jim', 'Smythe, David', 'Blattman, Ben', 'Byrne, Jason', 'Thompson, David', 'Shamakhy, Alireza', 'Ryan, Chris', 'Ponsonby, Mark', 'Thomson, Jamie', 'Hyde, David', 'Harrison, Schae', 'Emam, Arash', 'Mazzaferri, Henry', 'Darlow, Anthony', 'Harrison, Peter', 'Timmermans,David', 'Van Veen, Peter', 'Rewell, Luke', 'Symes, Brendon', 'Mujica, Jose', 'Short, Craig', 'Ballment, Meg', 'Salgueiro, Christian', 'Wakefield, Paul', 'Falconer, Colin', 'Powell, Robyn', 'Florey, Linda', 'Dodson, Michelle', 'Jordan, Julia', 'Winsemius, Karen', 'Nguyen, Khanh'])
        else:
            raise SystemExit('pennant_names: "pennant" can be only "Morning_Morning/Thursday_Mornin/Wednesday_Night/Thursday_Night":'+__file__+' line number: '+str(inspect.stack()[0][2]))

    else:
        raise SystemExit('pennant_names: "what" can be only "Team_Names" or "Player_Names":'+__file__+' line number: '+str(inspect.stack()[0][2]))

    return(0)

################################################################################

def concat_files(diag, files):
    '''
    Creator: Mark Collier
    Last Modified: 21 August 2019

    concat 2 or more files, last file in list is the output file.
    
    Inputs:
    a list of files

    Outputs:
    last element of files is used for output name
    '''

    with open(files[-1], 'w') as outfile:
        for fname in files[0:-1]:
            with open(fname) as infile:
                outfile.write(infile.read())

    return(0) # end of concat_files

################################################################################

def append_df_to_html(diag, df, html_file):
    '''
    Creator: Mark Collier
    Last Modified: 21 August 2019

    append html from a dataframe if html exists, otherwise make it.
    
    Inputs:
    df to print to html file (this can be opened with a browser).

    Outputs:
    output file html_file
    '''
    import os
    import datetime
    import shutil
    from datetime import timedelta

    onesecond = timedelta(seconds=1)

    if(not os.path.exists(html_file)):
        df.to_html(html_file, escape=False)
    else:
        html_tmp1 = '/tmp/html_'+(datetime.datetime.today()+timedelta(seconds=0)).strftime('%Y-%m-%d-%H-%M-%S')
        html_tmp2 = '/tmp/html_'+(datetime.datetime.today()+timedelta(seconds=-10)).strftime('%Y-%m-%d-%H-%M-%S')

        if(diag): print(html_tmp1)
        if(diag): print(html_tmp1)

        df.to_html(html_tmp1, escape=False)

        files = [html_file, html_tmp1, html_tmp2]
        concat_files(diag, files)
        shutil.move(html_tmp2, html_file)
        os.remove(html_tmp1)
       
    return(0) # end of append_df_html

################################################################################
