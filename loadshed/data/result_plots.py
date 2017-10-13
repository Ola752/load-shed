"""
Created on Mon Oct  9 17:03:32 2017

@author: Ola
"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import random
from random import randint
import pandas as pd

fname = "ls_complete2.txt"
fh = open(fname)

R1 = []
R2 = []
R3 = []
R4 = []

CONS = pd.DataFrame()
# cons = pd.read_csv('lstrial_tiny.csv', sep=',', parse_dates=True, names=['date', 'hour', 'house_id', 'value'])
cons = pd.read_csv('ls_complete.csv', sep=',', parse_dates=True, names=['date', 'hour', 'house_id', 'value'])
CONS = CONS.append(cons, ignore_index=False, verify_integrity=False)

dates = CONS.date.unique()
house_IDs = CONS.house_id.unique()
hours = CONS.hour.unique()

chosen_date = dates[randint(0, len(dates))]
chosen_date = str(chosen_date)


for lines in fh:
    lines = lines.rstrip()
    # datess = dates[randint(0, len(dates))]
    if lines.startswith(chosen_date):
        lines = lines.split(',')
        a = str(random.choice(house_IDs))
        if lines[1].startswith(a):
            c1 = lines[3]
            R1.append(c1)
            R1 = [float(i) for i in R1]
        b = str(random.choice(house_IDs))
        if lines[1].startswith(b):
            c1 = lines[3]
            R2.append(c1)
            R2 = [float(i) for i in R2]
        c = str(random.choice(house_IDs))
        if lines[1].startswith(c):
            c1 = lines[3]
            R3.append(c1)
            R3 = [float(i) for i in R3]
        d = str(random.choice(house_IDs))
        if lines[1].startswith(d):
            c1 = lines[3]
            R4.append(c1)
            R4 = [float(i) for i in R4]

# Time_Slots = []
# for i in range (0, 24):
#    Time_Slots.append(i)


# width = 0.3
# ax = pl.subplot(111)
# w = 0.25
# pl.xlabel('Households')
# pl.ylabel('Hourly Consumption')
# ax.bar(np.asarray(Time_Slots) - 0.3, R1, width=w ,color='b',align='center')
# ax.bar(np.asarray(Time_Slots) - 0.1, R2, width=w,color='g',align='center')
# ax.bar(np.asarray(Time_Slots) + 0.1, R3, width=w,color='r',align='center')
# ax.bar(np.asarray(Time_Slots) + 0.3, R4, width=w,color='y',align='center')
# pl.xticks(Time_Slots, rotation='vertical')
# legend = pl.legend(loc='upper right', shadow=True)
##pl.ylim(0,0.9)
# pl.xlim([(min(Time_Slots) - 0.35),(max(Time_Slots) + 0.35)])
##ax.autoscale(tight=True)
#
# pl.show()




row_names = ['H1', '', 'H2', '', 'H3', '', 'H4']
column_names = [0, 5, 10, 15, 20]

fig = plt.figure()
ax = Axes3D(fig)

lx = 24  # Work out matrix dimensions
ly = 4
xpos = np.arange(0, lx, 1)  # Set up a mesh of positions
ypos = np.arange(0, ly, 1)
xpos, ypos = np.meshgrid(xpos + 0.2, ypos + 0.2)
xpos = [item for sublist in xpos for item in sublist]
ypos = [item for sublist in ypos for item in sublist]

zpos = np.zeros(lx * ly)

dx = 0.15 * np.ones_like(zpos)
dy = dx.copy()
dz = R1 + R2 + R3 + R4

cs = ['c'] * 24 + ['b'] * 24 + ['g'] * 24 + ['r'] * 24

ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=cs)

# sh()
ax.w_xaxis.set_ticklabels(column_names)
ax.w_yaxis.set_ticklabels(row_names)
ax.set_xlabel('Hours')
ax.set_ylabel('Households')
ax.set_zlabel('Consumption')

plt.show()

# For total consumption
Time_Slots = []
for i in range(0, 24):
    Time_Slots.append(i)


def get_sum_consumption(group):
    return group.value.sum()


# Total hourly sum of all consumption, to get plots
hourly_sum = CONS.groupby(['hour']).apply(get_sum_consumption)
# print (hourly_sum)

width = 0.5
plt.xlabel('Hours')
plt.ylabel('Total hourly consumption')
plt.bar(Time_Slots, hourly_sum, width, color='b', align='center')
plt.xticks(Time_Slots, rotation='vertical')
plt.legend = plt.legend(loc='upper right', shadow=True)
plt.xlim([(min(Time_Slots) - 0.25), (max(Time_Slots) + 0.25)])
# pl.ylim(0.7, 1.0)
plt.show()
