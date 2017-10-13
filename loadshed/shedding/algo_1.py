"""
Created on Sun Oct 1 01:16:53 2017

@author: Ola
"""

import pandas as pd
import os
from random import randint
from matplotlib import pyplot as plt
import numpy as np
from pprint import pprint

# FILE_PATH   = os.path.join(os.getcwd(),'data','lstrial_tiny.h5')
# LOAD_SEG    = 1    #### USE TO PLOT INDIVIDUAL LOAD SHEDS
FILE_PATH   = os.path.join(os.getcwd(),'data','ls_complete_2.h5')
LOAD_SEG    = 100
PAUSE_PRINT = False

def form_groups(date_hour_group,avg_h_cons,cut,shedding={}):
    groups = []
    #Iterate the rows
    houses = [[row['house_id'],row['value']] for index,row in date_hour_group.iterrows()]

    while len(houses) :
        group = []
        while sum( [h[1] for h in group]) <= cut and len(houses) :
            i = randint(0,len(houses)-1)
            group.append(houses[i]+[shedding.get(houses[i][0],0)])
            shedding[houses[i][0]] = shedding.get(houses[i][0],0)
            del houses[i]
        groups.append(group)

    if sum([ h[1] for h in groups[-1] ]) < cut :
        groups = groups[:-1]

    return groups,shedding




def load_set():
    '''
    Load the data
    '''
    df                  = pd.read_hdf(FILE_PATH)

    '''
    Calculate the hourely average
    '''
    date_hour_groups    = df.groupby(['date','hour'])
    total_cons          = [date_hour_groups.get_group((a,b))['value'].sum() for a,b in date_hour_groups.groups ]
    avg_h_cons          = sum(total_cons)/len(total_cons) *1.0
    house_count         = len(df['house_id'].unique())
    '''
    Create the groups
    '''
    shedding = {}
    #For each hour
    loads = 1
    last_df = None
    full_df = None
    number_shed = 0
    x = []
    y = []
    ym = []
    yx = []
    deficits = [] ##
    loads_cut = []  ##
    numbers_shed = []  ##

    for a,b in date_hour_groups.groups :
        print ('*'*60)
        print ('{} - {} - {}'.format(loads,a,b))
        try :
            avg_h_cons = df.loc[df['date'] == a]['value'].mean()*house_count

            date_hour_group  = date_hour_groups.get_group((a,b))
            h_cons = date_hour_group['value'].sum()

            cut = h_cons - avg_h_cons
            load_cut = 0 ##


            if h_cons >= avg_h_cons :
                deficits.append(cut) ##
                #Form groups
                groups,shedding = form_groups(date_hour_group,avg_h_cons,cut,shedding)

                #Shed, by the cumulative number of sheds in the group
                shed_sums = [[sum([h[2] for h in groups[i]]),i] for i in range(0,len(groups))]
                min_shed  = min([g[0] for g in shed_sums])
                g_index = [g[1] for g in shed_sums if g[0] == min_shed][0]

                #shed

                for h in groups[g_index] :
                    h[2] += 1
                    shedding[h[0]] = h[2]

                for hs in groups[g_index] :
                    print('ID : {:>10.0f}, CONS : {:>10.2f}, SHED : {:>10.2f}'.format(hs[0],hs[1],hs[2]))
                    load_cut += hs[1] ##
                    # print (load_cut) ##
                number_shed +=len(groups[g_index])
                num_shed = len(groups[g_index])  ##

                print ('CUT : {:>10.2f}, CONSUMPTION {:>10.2f}'.format(cut,h_cons))
                loads +=1

                loads_cut.append(load_cut)  ##
                numbers_shed.append(num_shed) ##


            if loads %LOAD_SEG == 0 :
                full_df = pd.DataFrame(list(shedding.items()),columns = ['house','shedding']).set_index('house')
                if last_df is None :
                    last_df = full_df.copy(True)
                    last_df['shedding'] = 0

                now_df = full_df.subtract(last_df,axis=1)
                now_df['total'] = full_df['shedding']
                last_df = full_df.copy(True)



                # print(groups)  ##
                # print (groups[g_index])  ##
                # print (len(groups[g_index]))  ##

                # print (deficits)
                # print (loads_cut)
                # print(numbers_shed)
                print ('*'*60)
                print ('LAST {}/{} LOADS '.format(LOAD_SEG,loads))

                print ('MAX : HOUSE {}, SHEDS {}'.format(now_df['shedding'].argmax(),now_df['shedding'].max()))
                print ('MIN : HOUSE {}, SHEDS {}'.format(now_df['shedding'].argmin(),now_df['shedding'].min()))
                print ('NUMBER OF HOUSES SHED : {}'.format(number_shed))
                x.append(loads)
                y.append(number_shed)
                yx.append(now_df['shedding'].max())
                ym.append(now_df['shedding'].min())
                number_shed = 0

            if PAUSE_PRINT :
                input()
        except :
            pass

    print ('*'*60)
    print ('TOTAL LOADS')
    print ('MAX : HOUSE {}, SHEDS {}'.format(full_df['shedding'].argmax(),full_df['shedding'].max()))
    print ('MIN : HOUSE {}, SHEDS {}'.format(full_df['shedding'].argmin(),full_df['shedding'].min()))
    total_shed = len(full_df.loc[full_df['shedding'] != 0])
    print ('TOTAL HOUSES SHED : {}'.format(total_shed))
    fig, ax = plt.subplots()
    x = [int(_x) for _x in x]
    # x = [i-LOAD_SEG for i in x]
    print (yx)
    print (ym)
    print (y)


    ticks = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

    plt.bar(x,y,width=LOAD_SEG/2.0,color='g',align='center',label = 'Sheds')
    plt.xlabel('Every 100 shedding events')
    plt.ylabel('Number of households shed')
    plt.xticks(ticks, rotation='horizontal')
    plt.ylim([0, max(y)* 1.3])
    plt.show()

    p1 = plt.bar(x, yx, LOAD_SEG/2.0, color='b',label = 'Max')
    p2 = plt.bar(x, ym, LOAD_SEG/2.0, color='r',bottom=yx)
    plt.xlabel('Every 100 shedding events')
    plt.ylabel('Number of households shed')
    plt.xticks(ticks, rotation='horizontal')
    plt.legend((p1[0], p2[0]),('Number of sheds of household most shed','Number of sheds of household least shed'),
               fontsize=10, ncol = 1, framealpha = 0, fancybox = True)
    plt.ylim([0, max([sum(x) for x in zip(yx,ym)])*1.3])
    plt.show()



    # plt.bar(x,y,width=LOAD_SEG/2.0,color='g',align='center',label = 'Sheds')
    # plt.xlabel('Every 100 shedding events')
    # plt.ylabel('Number of households shed')
    # plt.xticks(x, rotation='horizontal')
    # plt.ylim([0, max(y)* 1.3])
    # plt.show()
    #
    # p1 = plt.bar(x, yx, LOAD_SEG/2.0, color='b',label = 'Max')
    # p2 = plt.bar(x, ym, LOAD_SEG/2.0, color='r',bottom=yx)
    # plt.xlabel('Every 100 shedding events')
    # plt.ylabel('Number of households shed')
    # plt.xticks(x, rotation='horizontal')
    # plt.legend((p1[0], p2[0]),('Number of sheds of household most shed','Number of sheds of household least shed'),
    #            fontsize=10, ncol = 1, framealpha = 0, fancybox = True)
    # plt.ylim([0, max([sum(x) for x in zip(yx,ym)])*1.3])
    # plt.show()




    # # For plotting deficits AND values of loads shed during first x individual loadsheds (Test DATA)
    # label_x = range(1,8)
    # ax = plt.subplot(111)
    # w = 0.4
    # plt.xlabel('Individual shedding events')
    # plt.ylabel('Loads in kW')
    # ax.bar(np.asarray(label_x) - w/2, deficits, width=w, color='g', align='center', label='Deficits')
    # ax.bar(np.asarray(label_x) + w/2, loads_cut, width=w, color='r', align='center', label='Loads cut')
    # plt.xticks(label_x, rotation='horizontal')
    # plt.legend = plt.legend(loc='upper right', shadow=True)
    # plt.ylim([0, (max(max(deficits), max(loads_cut)) * 1.3)])
    # plt.xlim([(min(label_x) - w), (max(label_x) + w)])
    # # ax.autoscale(tight=True)
    # plt.show()


    # # For plotting deficits AND values of loads shed during first 50 individual loadsheds
    # ax = plt.subplot(111)
    # w = 0.4
    # plt.xlabel('Individual shedding events')
    # plt.ylabel('Loads in kW')
    # label_x = range(1, 51)
    # ax.bar(np.asarray(label_x) - w/2, deficits[:50], width=w, color='g', align='center', label='Deficits')
    # ax.bar(np.asarray(label_x) + w/2, loads_cut[:50], width=w, color='r', align='center', label='Loads cut')
    # plt.xticks([x - 1 for x in label_x][0::5], rotation='horizontal')
    # plt.legend = plt.legend(loc='upper right', shadow=True)
    # plt.ylim([0, (max(max(deficits[:50]), max(loads_cut[:50])) * 1.3)])
    # plt.xlim([(min(label_x) - w), (max(label_x) + w)])
    # # ax.autoscale(tight=True)
    # plt.show()



    # # For plotting number of households shed per unit load cut (TEST DATA)
    # w2 = 0.5
    # plt.xlabel('Individual shedding events')
    # plt.ylabel('Households shed per unit kW load cut')
    # label_x = range(1, 8)
    # plt.bar(label_x, [x/y for x, y in zip(numbers_shed, deficits)], width = w2, color='b')
    # plt.xlim([(min(label_x) - w2), (max(label_x) + w2)])
    # plt.ylim([0,1])
    # plt.show()


    #
    # # For plotting number of households shed per unit load cut (first 50 sheds)
    # w2 = 0.5
    # plt.xlabel('Individual shedding events')
    # plt.ylabel('Households shed per unit kW load cut')
    # label_x = range(1, 51)
    # plt.bar(label_x, [x/y for x, y in zip(numbers_shed[:50], deficits[:50])], width = w2, color='b')
    # plt.xlim([(min(label_x) - w2), (max(label_x) + w2)])
    # plt.ylim([0,1])
    # plt.show()