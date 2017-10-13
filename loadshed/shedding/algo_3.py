"""
Created on Thu Sep 21 15:34:01 2017

@author: Ola
"""
from utils import db
import gb, random
from data import data_access
from collections import Counter
import operator

class Shedding:
    def __init__(self, hour_uses, n_house):
        self.hour_uses = hour_uses
        self.threshold = None
        self.n_house = n_house
        self.shedded_list = set()  # an empty set (of house ids)
        self.n_highests = []
        self.n_mediums = []
        self.n_lowests = []
        self.mosts = []
        self.leasts = []
        self.deficits = []
        self.loads_cut = []
        self.highest_houseids = []
        self.medium_houseids = []
        self.lowest_houseids = []
        self.n_highest = 0
        self.n_medium = 0
        self.n_lowest = 0
        self.shedding_range = 0
        self.n_shedding = 0
        self.daily_mean = data_access.abc()

    def calc_threshold(self, hour_uses):
        """
        calc average consumption value and put it to self.threshold
        :return: nothing
        """
        self.threshold = self.daily_mean[hour_uses.date]
        # self.threshold = hour_use.mean()

    def do_hour_shedding(self, hour_use):
        """

        :param hour_use: an HourUse object
        :return:
        """
        if hour_use.total_value <= self.threshold:
            return
        cut = hour_use.total_value - self.threshold
        if cut > 0:
            self.deficits.append(cut)
        hour_shedded_list = set()
        load_cut = 0  ##
        while cut > 0:
            i = random.randint(0, self.n_house)
            house_id = hour_use.house_id(i)
            if house_id is not None and house_id not in self.shedded_list and house_id not in hour_shedded_list:
                cut -= hour_use.value(i)
                load_cut += hour_use.value(i)  ##
                self.shedded_list.add(house_id)
                hour_shedded_list.add(house_id)
                p = hour_use.percent(i)
                if p >= gb.T_level2:
                    self.n_highest += 1
                    self.highest_houseids.append(house_id)
                elif gb.T_level1 < p < gb.T_level2:
                    self.n_medium += 1
                    self.medium_houseids.append(house_id)
                elif p <= gb.T_level1:
                    self.n_lowest += 1
                    self.lowest_houseids.append(house_id)
                db.inline_verydetail(f'{house_id:3} {cut:6.2f}')
                db.line_verydetail(f' [{self.n_highest:2} {self.n_medium:2} {self.n_lowest:2}]')
            # i += 1
            # if i == hour_use.length:
            #     i = 0
                # db.line_verydetail('     i=0')
            if len(self.shedded_list) == self.n_house:  # No more houses to shed is empty
                self.shedded_list = set()
            #     i = 0
            #     db.line_verydetail('     shedded_list=empty')
        self.loads_cut.append(load_cut)  ##
        self.n_shedding += 1
        if self.n_shedding % 100 == 0:  #### CHANGE TO 100 or n when needed
            self.n_highests.append(self.n_highest)
            self.n_mediums.append(self.n_medium)
            self.n_lowests.append(self.n_lowest)
            self.shedding_range += 1
            self.n_highest = self.n_medium = self.n_lowest = 0

            db.line_verydetail(f'{self.lowest_houseids + self.medium_houseids + self.highest_houseids}')
            dd = self.lowest_houseids + self.medium_houseids + self.highest_houseids
            cnt = Counter()
            for d in dd:
                cnt[d] += 1
            sorted_cnt = sorted(cnt.items(), key=operator.itemgetter(1))
            # print(sorted_cnt) # House IDs and frequencies of shedded houses
            self.mosts.append(sorted_cnt[0][1])  # Number of sheds of house most shedded after n_shedding sheds
            self.leasts.append(sorted_cnt[-1][1])  # Number of sheds of house least shedded after n_shedding sheds

            del self.lowest_houseids[:]
            del self.medium_houseids[:]
            del self.highest_houseids[:]

            # db.line_verydetail(f'{self.highest_houseids}')
            # db.line_verydetail(f'{self.medium_houseids}')
            # db.line_verydetail(f'{self.lowest_houseids}')
            # db.line_verydetail(f'{self.lowest_houseids + self.medium_houseids + self.highest_houseids}')
            # dd = shedding.lowest_houseids + shedding.medium_houseids + shedding.highest_houseids

    def do_shedding(self, ):
        """
        Iterate over the data (ie uses, every hour) and do the shedding
        :return:
        """
        for i, hour_use in enumerate(
                self.hour_uses):  # hour_use is a HourUse object (with house_ids, values, and total_value)
            db.line_detail('hour: {}'.format(i))
            self.calc_threshold(hour_use)
            self.do_hour_shedding(hour_use)

            # db.line_verydetail(f'{self.lowest_houseids}')
            # dd = self.lowest_houseids + self.medium_houseids + self.highest_houseids
            # db.line_verydetail(f'{dd}')
            # print (len(dd))
