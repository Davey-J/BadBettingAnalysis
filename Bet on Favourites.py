import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

data = []
bet_on_fav = []

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

for game in data[1:]:
    odds = game[26:29]
    favourite = ' '
    fav_odds = 0
    profit = 0
    winner = game[6]

    if min(odds) == odds[0]:
        fav_odds = float(odds[0])
        favourite = 'H'
    elif min(odds) == odds[1]:
        fav_odds = float(odds[1])
        favourite = 'D'
    elif min(odds) == odds[2]:
        fav_odds = float(odds[2])
        favourite = 'A'

    if favourite == winner:
        profit = 10*fav_odds
    else:
        profit = -10

    bet_on_fav.append([favourite, winner, fav_odds, profit])

total_wins = 0
running_tally = []
success = 0
total = 0

for x in bet_on_fav:
    if x[2]:
        print(x)
        total += 1
        if x[3] < 0:
            total_wins += x[3]
            success += 1
        else:
            total_wins += x[3]-10
    running_tally.append(total_wins)

print(total_wins)
print(success/total)
print(total)

fig, ax = plt.subplots()  # Create a figure containing a single axes.
plt.title('Total P/L Over the 2019-2023 Seasons Betting on the Favourite')
plt.xlabel('Game Number')
plt.ylabel('Total P/L in GBP')
ax.plot(range(0,len(running_tally)), running_tally)
plt.savefig("Favourite Plot")# Plot some data on the axes.
plt.show()