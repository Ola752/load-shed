"""
Created on Mon Jul 24 11:56:55 2017

@author: Ola
"""
import matplotlib.pyplot as plt
import numpy as np
from data.data_access import read_consumptions
# from shedding.algo_2 import Shedding  # Use this when running algo1 or shedding
from shedding.algo_3 import Shedding     # Use this when running algo2 or shedding1
import gb
from shedding import algo_1
from shedding import algo_1_1
from shedding import algo_2_2
from shedding import algo_3_2
from shedding import algo_4
from shedding import algo_X
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


    # For printing first x individual loadsheds
    w1 = 0.5
    plt.xlabel('Number of shedding events')
    plt.ylabel('Number of households disconnected')
    label_x = range(1, 51)
    # label_x = range(1, 8)
    p1 = plt.bar(label_x, shedding.n_highests[:50], width = w1, color='g')
    p2 = plt.bar(label_x, shedding.n_mediums[:50], width = w1, color='b', bottom = shedding.n_highests[:50])
    p3 = plt.bar(label_x, shedding.n_lowests[:50], width = w1, color='r', bottom = [sum(x) for x in zip(shedding.n_highests[:50],shedding.n_mediums[:50])])
    plt.legend((p1[0], p2[0], p3[0]), ('High electricity consumers', 'Medium electricity consumers', 'Low electricity consumers'),
               fontsize=10, ncol=1, framealpha=0, fancybox=True)
    plt.ylim([0, max([sum(x) for x in zip(shedding.n_lowests[:50], shedding.n_mediums[:50], shedding.n_highests[:50])]) * 1.5])
    plt.xticks([x - 1 for x in label_x][0::5], rotation='horizontal')
    plt.xlim([(min(label_x) - w1/2), (max(label_x) + w1/2)])
    plt.show()

    # # For printing aggregated x loadsheds in n groups A
    # plt.xlabel('Every 100 shedding events')
    # plt.ylabel('Number of times selected')
    # label_x = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    # # label_x = [100, 200, 300]
    # p1 = plt.bar(label_x, shedding.n_highests, width=50, color='g')
    # p2 = plt.bar(label_x, shedding.n_mediums, width=50, color='b', bottom = shedding.n_highests)
    # p3 = plt.bar(label_x, shedding.n_lowests, width=50, color='r', bottom = [sum(x) for x in zip(shedding.n_highests,shedding.n_mediums)])
    # plt.legend((p1[0], p2[0], p3[0]), ('High-level consumers', 'Med-level consumers', 'Low-level consumers'),
    #            fontsize=10, ncol=1, framealpha=0, fancybox=True)
    # plt.ylim([0, max([sum(x) for x in zip(shedding.n_lowests, shedding.n_mediums, shedding.n_highests)]) * 1.5])
    # plt.xticks(label_x, rotation = 'horizontal')
    # plt.show()
    #
    #
    # # For printing aggregated number of houses shed every 100 load sheds
    # plt.xlabel('Every 100 shedding events')
    # plt.ylabel('Number of times selected')
    # label_x = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    # plt.bar(label_x, [sum(x) for x in zip(shedding.n_highests, shedding.n_mediums, shedding.n_lowests)], width=50, color='g')
    # plt.ylim([0, max([sum(x) for x in zip(shedding.n_lowests, shedding.n_mediums, shedding.n_highests)]) * 1.3])
    # plt.xticks(label_x, rotation = 'horizontal')
    # plt.show()
    #
    #
    # # For printing aggregated x loadsheds in n groups B
    # plt.xlabel('Every 100 shedding events')
    # plt.ylabel('Number of times selected')
    # label_x = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    # # label_x = [100, 200, 300]
    # p1 = plt.bar(label_x, shedding.mosts, width=50, color='b')
    # p2 = plt.bar(label_x, shedding.leasts, width=50, color='r', bottom = shedding.mosts)
    # plt.legend((p1[0], p2[0]),('Number of sheds of household most shed','Number of sheds of household least shed'),
    #            fontsize=10, ncol = 1, framealpha = 0, fancybox = True)
    # plt.ylim([0, max([sum(x) for x in zip(shedding.mosts,shedding.leasts)])*1.3])
    # plt.xticks(label_x, rotation = 'horizontal')
    # plt.show()


    # # For plotting deficits AND values of loads shed during first x individual loadsheds (DEBUG DATA SET)
    # ax = plt.subplot(111)
    # w = 0.25
    # plt.xlabel('Individual shedding events')
    # plt.ylabel('Loads in kWh')
    # label_x = range(1, 8)
    # ax.bar(np.asarray(label_x) - w/2, shedding.deficits, width=w, color='b', align='center', label='Deficits')
    # ax.bar(np.asarray(label_x) + w/2, shedding.loads_cut, width=w, color='r', align='center', label='Loads cut')
    # plt.xticks(label_x, rotation='vertical')
    # plt.legend = plt.legend(loc='upper right', shadow=True)
    # plt.ylim([0, (max(max(shedding.deficits), max(shedding.loads_cut)) * 1.3)])
    # plt.xlim([(min(label_x) - 0.25), (max(label_x) + 0.25)])
    # # ax.autoscale(tight=True)
    # plt.show()


    # For plotting deficits AND values of loads shed during first 50 individual loadsheds
    ax = plt.subplot(111)
    w = 0.4
    plt.xlabel('Number of shedding events')
    plt.ylabel('Consumption (kWh)')
    label_x = range(1, 51)
    ax.bar(np.asarray(label_x) - w/2, shedding.deficits[:50], width=w, color='b', align='center', label='Deficits')
    ax.bar(np.asarray(label_x) + w/2, shedding.loads_cut[:50], width=w, color='r', align='center', label='Loads cut')
    plt.xticks([x - 1 for x in label_x][0::5], rotation='horizontal')
    plt.legend = plt.legend(loc='upper right', shadow=True)
    plt.ylim([0, (max(max(shedding.deficits[:50]), max(shedding.loads_cut[:50])) * 1.3)])
    plt.xlim([(min(label_x) - w), (max(label_x) + w)])
    # ax.autoscale(tight=True)
    plt.show()


    # For plotting number of households shed per unit load cut
    w2 = 0.5
    plt.xlabel('Number of shedding events')
    plt.ylabel('Households disconnected per kW shed')
    label_x = range(1, 51)
    # label_x = range(1, 8)
    plt.bar(label_x, [x/y for x, y in zip([sum(k) for k in zip(shedding.n_lowests[:50], shedding.n_mediums[:50], shedding.n_highests[:50])], shedding.loads_cut[:50])], width = w2, color='b')
    plt.xlim([(min(label_x) - w2), (max(label_x) + w2)])
    plt.ylim([0,1])
    plt.show()


    print ([sum(x) for x in zip(shedding.n_lowests[:50], shedding.n_mediums[:50], shedding.n_highests[:50])])
    print ()


if __name__ == '__main__':
    # go() # this can be used when running algo2 or algo3. Just change at the top!
    # algo_1.load_set()
    algo_1_1.load_set()
    # algo_2_2.load_set()
    # algo_3_2.load_set()
    # algo_4.load_set()
    # algo3()
    # algo4()
    # test()


