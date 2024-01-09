import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import math

data = []

with open("Premiership 2021-22.csv", 'r') as csv_data:
    open_data = []
    data_reader = csv.reader(csv_data)
    for row in data_reader:
        data.append(row)

correct = 0
incorrect = 0
draws = 0
funds = 500
profit = 0
total_profit = 0
retroactive_look_range = 5
running_total = []

for game_no in range(1,len(data)):
    game = data[game_no]
    odds = game[26:29]
    home_team = game[2]
    away_team = game[3]
    past_home_games = []
    past_away_games = []

    for past_game in data[game_no-1:0:-1]:
        if len(past_home_games) < retroactive_look_range and past_game[2] == home_team:
            past_home_games.append(int(past_game[4]) - int(past_game[5]))
        elif len(past_home_games) < retroactive_look_range and past_game[3] == home_team:
            past_home_games.append(int(past_game[4]) - int(past_game[5]))

    for past_game in data[game_no - 1:0:-1]:
        if len(past_away_games) < retroactive_look_range and past_game[2] == away_team:
            past_away_games.append(int(past_game[4]) - int(past_game[5]))
        elif len(past_away_games) < retroactive_look_range and past_game[3] == away_team:
            past_away_games.append(int(past_game[4]) - int(past_game[5]))

    if len(past_home_games) > 0:
        home_past_gd = sum(past_home_games)/len(past_home_games)
    else:
        home_past_gd = 0
    if len(past_away_games) > 0:
        away_past_gd = sum(past_away_games)/len(past_away_games)
    else:
        away_past_gd = 0

    predicted = ''

    if home_past_gd > away_past_gd:
        predicted = 'H'
    elif home_past_gd < away_past_gd:
        predicted = 'A'
    else:
        predicted = 'D'

    stake = 10

    if game[6] == predicted:
        correct += 1
        if game[6] == 'H':
            profit = stake*(float(odds[0])) - stake
        elif game[6] == 'A':
            profit = stake*(float(odds[2])) - stake
        elif game[6] == 'D':
            profit = stake*(float(odds[1])) - stake
    else:
        profit = -stake
        incorrect += 1
    total_profit += profit
    running_total.append(total_profit)

print()
print(correct)
print(draws)
print(incorrect)
print()
print(total_profit)

fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot(range(0,len(running_total)), running_total)  # Plot some data on the axes.
plt.show()