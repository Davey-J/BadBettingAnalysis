import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import math

match_data = []
elo_params = [1500,64,400,1]

start_elos = {"E0": 4000, "E1": 3000, "E2": 2000, "E3": 1000}
leagues = ["Premiership","Championship","League 1","League 2"]
names = []

year_range = range(19,23)
year_num = len(year_range)
league_num = len(leagues)

for league in leagues:
    names.append([league + " 20" + str(x) + "-" + str(x+1) + ".csv" for x in year_range])

print(names)

for x in range(0,year_num):
    for y in range(0,league_num):
        name_data = []
        with open(names[y][x], 'r') as csv_data:
            open_data = []
            data_reader = csv.reader(csv_data)
            for data_row in data_reader:
                name_data.append(data_row)
        match_data += name_data[1:]


def elo_sigma(r,k,s):
    return (10 ** (r / s)) / ((10 ** ((-r) / s)) + k + (10 ** (r / s)))


def calc_elos(data,params):
    teams = {}

    start_elo = params[0]
    k_factor = params[1]
    scale_factor = params[2]
    k_draw = params[3]

    for row in data:
        h_team = row[2]
        a_team = row[3]
        winner = row[6]

        elo_probs = [0, 0, 0]

        if h_team not in teams:
            teams[h_team] = start_elos[row[0]]
        if a_team not in teams:
            teams[a_team] = start_elos[row[0]]

        h_init_elo = teams[h_team]
        a_init_elo = teams[a_team]

        expected_score = 1 / (1 + (10 ** ((a_init_elo - h_init_elo) / scale_factor)))

        r = h_init_elo - a_init_elo

        elo_probs[0] = elo_sigma(r, k_draw, scale_factor)
        elo_probs[2] = elo_sigma(-r, k_draw, scale_factor)
        elo_probs[1] = k_draw * math.sqrt(elo_sigma(r, k_draw, scale_factor)*elo_sigma(-r, k_draw, scale_factor))

        actual_score = 0.5

        if winner == 'H':
            actual_score = 1
        elif winner == 'A':
            actual_score = 0
        else:
            actual_score = 0.5

        h_adjusted_elo = max(100, h_init_elo + (k_factor * (actual_score - expected_score)))
        a_adjusted_elo = max(100, a_init_elo + (k_factor * -(actual_score - expected_score)))

        teams[h_team] = h_adjusted_elo
        teams[a_team] = a_adjusted_elo

    return teams


def print_rankings(elo_dict):
    sorted_rankings = sorted(elo_dict.items(), key=lambda x:x[1])
    for x in sorted_rankings:
        print(x)


def get_bet(h,a,elo_data,book_odds,params):
    print(h + " v " + a)
    elo_probs = [0,0,0]
    odds_probs = [1/book_odds[0],1/book_odds[1],1/book_odds[2]]

    start_elo = params[0]
    k_factor = params[1]
    scale_factor = params[2]
    k_draw = params[3]

    h_elo = elo_data[h]
    a_elo = elo_data[a]

    expected_score = 1 / (1 + (10 ** ((a_elo - h_elo) / scale_factor)))

    r = h_elo - a_elo

    elo_probs[0] = elo_sigma(r, k_draw, scale_factor)
    elo_probs[2] = elo_sigma(-r, k_draw, scale_factor)
    elo_probs[1] = k_draw * math.sqrt(elo_sigma(r, k_draw, scale_factor) * elo_sigma(-r, k_draw, scale_factor))

    if max(elo_probs) == elo_probs[0]:
        print("Home Win Expected")
        print(elo_probs[0])
        print(odds_probs[0])
        print("Stake Mult :", elo_probs[0]/odds_probs[0])
    elif max(elo_probs) == elo_probs[1]:
        print("Draw Expected")
        print(elo_probs[1])
        print(odds_probs[1])
        print("Stake Mult :", elo_probs[1] / odds_probs[1])
    elif max(elo_probs) == elo_probs[2]:
        print("Away Win Expected")
        print(elo_probs[2])
        print(odds_probs[2])
        print("Stake Mult :", elo_probs[2] / odds_probs[2])


calc_data = calc_elos(match_data,elo_params)
print_rankings(calc_data)
print()

get_bet( "Forest Green", "Sheffield Weds", calc_data, [9, 4.8, 1.47], elo_params)
