"""
Created on Mon Jul 24 11:56:54 2017

@author: Ola
"""
import numpy as np


class HourUse:
    def __init__(self, date_index):
        self.house_ids = []
        self.date = date_index  # 0-based date index
        self.values = []
        self.percents = None  # np.array(), [0, 100]
        self.hour_highest = 0
        self.total_value = 0
        self.length = 0
        self.n_hrs = 24
        self.threshold = None

    def add(self, house_id, value, date_index):
        self.house_ids.append(house_id)
        self.values.append(value)
        self.total_value += value
        self.length += 1

    def value(self, index):
        if index < 0 or index >= self.length:
            return None
        return self.values[index]

    def house_id(self, index):
        if index < 0 or index >= self.length:
            return None
        return self.house_ids[index]

    def mean(self):
        return self.total_value / self.length

    def percent(self, index):
        if index < 0 or index >= self.length:
            return None
        return self.percents[index]

    def sort(self):
        """
        Sort the two arrays (house_ids and values) in descending order based on values.
        :return: nothing, just update the two arrays self.house_ids and self.values
        """
        n = len(self.house_ids)
        for i in range(n - 1):
            for j in range(i + 1, n):
                if self.values[i] < self.values[j]:
                    self.values[i], self.values[j] = self.values[j], self.values[i]
                    self.house_ids[i], self.house_ids[j] = self.house_ids[j], self.house_ids[i]

        # update self.percents for the houses
        a = np.array(self.values)
        min_value = a.min()
        max_value = a.max()
        self.percents = ((a - min_value) / (max_value - min_value) * 100).round().astype(int)
