import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import random

data = []

leagues = ["Premiership","Championship","League 1","League 2"]
names = []
year_range = range(19,23)

for league in leagues:
    names.append([league + " 20" + str(x) + "-" + str(x+1) + ".csv" for x in year_range])

print(names)

for league in names:
    for file in league:
        name_data = []
        with open(file, 'r') as csv_data:
            open_data = []
            data_reader = csv.reader(csv_data)
            for data_row in data_reader:
                name_data.append(data_row)
        data += name_data[1:]

profit = 0
running_profit = []
stake = 10

for game in data:
    odds = [float(x) for x in game[26:29]]
    home_team = game[2]
    away_team = game[3]
    winner = game[6]

    selection = random.randint(0,3)

    if selection == 0 and winner == 'H':
        print("Home Win")
        profit += (odds[0] * stake) - stake
    elif selection == 1 and winner == 'D':
        profit += (odds[1] * stake) - stake
        print("Draw Win")
    elif selection == 2 and winner == 'A':
        profit += (odds[2] * stake) - stake
        print("Away Win")
    else:
        profit += -stake
        print("Loss")
    running_profit.append(profit)

print(profit)

plt.plot(running_profit)
plt.show()