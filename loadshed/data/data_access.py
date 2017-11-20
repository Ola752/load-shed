"""
Created on Mon Jul 24 11:56:55 2017

@author: Ola
"""

import pandas as pd
import os
from utils import db
from shedding.hour_use import HourUse
from utils import timing


def find_houseid_max(uses):
    hmax = 0
    for i, use in uses.iterrows():
        if use.house_id > hmax:
            hmax = use.house_id
    return hmax


def read_hdf5():
    timing.start()
    filename = 'ls_comp.h5'
    # filename = 'lstrial_tiny.h5'
    uses = pd.read_hdf(filename, 'data', mode='r', columns=['date', 'hour', 'house_id', 'value'])
    pd.to_datetime(uses['date'])
    uses.value = uses.value.astype(float)
    m = find_houseid_max(uses)
    print(f'hmax: {m}')
    timing.stop()


def read_consumptions():
    """
    use pd to read_csv into a uses frame, called 'uses'.
    Then, sort the uses based on 'use', every hour.
    :return: hour_uses, an array of HourUse objects
    """
    # current_dir = os.path.dirname(__file__)
    # file_path = os.path.join(current_dir, 'ls.csv')
    # uses = pd.read_csv(file_path, names=['date', 'hour', 'house_id', 'value'])  # dataframe (in pandas)
    # filename = 'ls.h5'
    # uses = pd.read_hdf(filename, 'data', mode='r', columns=['date', 'hour', 'house_id', 'value'])
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'ls_comp.h5')
    # file_path = os.path.join(current_dir, 'lstrial_tiny.h5')
    uses = pd.read_hdf(file_path, names=['date', 'hour', 'house_id', 'value'])  # dataframe (in pandas)



    pd.to_datetime(uses['date'])
    uses.value = uses.value.astype(float)
    hour_uses = []
    house_ids = set()
    current_date = current_hour = None
    date_index = -1

    # db.line_brief(f'{uses.shape}')
    for i, use in uses.iterrows():
        # if i % 10000 == 0:
        #     db.inline(f'{i/10000:.0f} ')
        if use.house_id not in house_ids:
            house_ids.add(use.house_id)
        if use.date != current_date or use.hour != current_hour:
            if use.date != current_date:
                date_index += 1
            current_date, current_hour = use.date, use.hour
            hour_use = HourUse(date_index)
            hour_uses.append(hour_use)
            # print(hour_use)
        hour_use.add(use.house_id, use.value, date_index)

    for hour_use in hour_uses:
        hour_use.sort()


    return hour_uses, len(house_ids)

def abc():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'ls_comp.h5')
    # file_path = os.path.join(current_dir, 'lstrial_tiny.h5')
    uses = pd.read_hdf(file_path, names=['date', 'hour', 'house_id', 'value'])

    def get_sum_consumption(group):
        return group.value.sum()

    def get_daily_mean_consumption(group):
        return group.value.sum() / len(uses.hour.unique())

    daily_mean = uses.groupby('date').apply(get_daily_mean_consumption)

    return daily_mean


if __name__ == '__main__':
    read_consumptions()

