"""
Created on Mon Jul 24 11:56:55 2017

@author: Ola
"""
import matplotlib.pyplot as plt

from data.data_access import read_consumptions
from shedding.shedding import Shedding  # Use this when running algo1 or shedding
# from shedding.shedding1 import Shedding     # Use this when running algo2 or shedding1
import gb
from shedding import algo_3
from shedding import algo_4
from utils import db
from utils.db import DebugMode
from utils.utils import *
# from statistics import mode
# from scipy.stats import mode
import operator


def go():
    # gb.debug_mode = DebugMode.Brief
    # gb.debug_mode = DebugMode.Detail
    gb.debug_mode = DebugMode.VeryDetail

    hour_uses, n_house = read_consumptions()
    shedding = Shedding(hour_uses, n_house)
    shedding.do_shedding()
    # db.line_verydetail(f'{shedding.n_highests}')
    # db.line_verydetail(f'{shedding.n_mediums}')
    # db.line_verydetail(f'{shedding.n_lowests}')

    # calc_cumulative_values(shedding.n_highests)
    # db.line_verydetail(f'{shedding.n_highests}')
    # calc_cumulative_values(shedding.n_mediums)
    # db.line_verydetail(f'{shedding.n_mediums}')
    # calc_cumulative_values(shedding.n_lowests)
    # db.line_verydetail(f'{shedding.n_lowests}')

    plt.xlabel('Every shedding event')
    plt.ylabel('Number of households shed')
    # label_x = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    # label_x = [100, 200, 300]
    label_x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    # label_x = [1, 2, 3, 4, 5, 6]
    p1 = plt.bar(label_x, shedding.n_highests[:30], width=0.4, color='g')
    p2 = plt.bar(label_x, shedding.n_mediums[:30], width=0.4, color='b', bottom = shedding.n_highests[:30])
    p3 = plt.bar(label_x, shedding.n_lowests[:30], width=0.4, color='r', bottom = [sum(x) for x in zip(shedding.n_highests[:30],shedding.n_mediums[:30])])
    plt.legend((p1[0], p2[0], p3[0]), ('High-level consumers', 'Med-level consumers', 'Low-level consumers'),
               fontsize=10, ncol=1, framealpha=0, fancybox=True)
    plt.ylim([0, max([sum(x) for x in zip(shedding.n_lowests[:30], shedding.n_mediums[:30], shedding.n_highests[:30])]) * 1.5])
    plt.xticks(label_x, rotation = 'vertical')
    plt.show()

    # plt.xlabel('Every 100 shedding events')
    # plt.ylabel('Number of households shed')
    # # label_x = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    # # label_x = [100, 200, 300]
    # p1 = plt.bar(label_x, shedding.n_highests, width=50, color='g')
    # p2 = plt.bar(label_x, shedding.n_mediums, width=50, color='b', bottom = shedding.n_highests)
    # p3 = plt.bar(label_x, shedding.n_lowests, width=50, color='r', bottom = [sum(x) for x in zip(shedding.n_highests,shedding.n_mediums)])
    # plt.legend((p1[0], p2[0], p3[0]), ('High-level consumers', 'Med-level consumers', 'Low-level consumers'),
    #            fontsize=10, ncol=1, framealpha=0, fancybox=True)
    # plt.ylim([0, max([sum(x) for x in zip(shedding.n_lowests, shedding.n_mediums, shedding.n_highests)]) * 1.5])
    # plt.xticks(label_x, rotation = 'horizontal')
    # plt.show()

    # plt.xlabel('Every 100 shedding events')
    # plt.ylabel('Number of households shed')
    # label_x = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    # # label_x = [100, 200, 300]
    # p1 = plt.bar(label_x, shedding.mosts, width=50, color='b')
    # p2 = plt.bar(label_x, shedding.leasts, width=50, color='r', bottom = shedding.mosts)
    # plt.legend((p1[0], p2[0]),('Number of sheds of household most shed','Number of sheds of household least shed'),
    #            fontsize=10, ncol = 1, framealpha = 0, fancybox = True)
    # plt.ylim([0, max([sum(x) for x in zip(shedding.mosts,shedding.leasts)])*1.3])
    # plt.xticks(label_x, rotation = 'horizontal')
    # plt.show()


def test():
    hour_uses, n_house = read_consumptions()
    print(n_house)



def algo2():
    gb.debug_mode = DebugMode.VeryDetail

    hour_uses, n_house = read_consumptions()
    shedding1 = Shedding(hour_uses, n_house)
    shedding1.do_shedding()


def algo3():
    print ('I am working on algorithm 3')


# def algo4():
#     print('I am working on algorithm 4')



if __name__ == '__main__':
    # go() # this can be used when running algo1 or algo2. Just change at the top!
    # algo2()
    # algo_3.load_set()
    algo_4.load_set()
    # algo3()
    # algo4()
    # test()


