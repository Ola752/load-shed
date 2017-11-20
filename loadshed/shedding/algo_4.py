"""
Created on Sat Oct 14 09:33:14 2017

@author: Ola
"""

"""
This algorithm is an original that considers standard deviation in selecting
households. The SD of weekly consumption is calculated, and households who
consume above a threshold (mean + 2*SD) during a hour of shedding are omitted
from the shedding! Thus, the difference between the number of times households
are selected is a bit higher, even though two lists try to make it equal.
"""

import pandas as pd
import os
from random import randint
from matplotlib import pyplot as plt
from pprint import pprint
import numpy as np
from datetime import datetime
import operator

# FILE_PATH   = os.path.join(os.getcwd(),'data','lstrial_tiny.h5')
# FILE_PATH   = os.path.join(os.getcwd(),'data','testdata_algo4.h5')
FILE_PATH    = os.path.join(os.getcwd(),'data','ls_comp.h5')

DATE_FORMAT     = '%Y-%m-%d-%H'
#DATE_FORMAT     = '%d/%m/%Y-%H'

LOAD_SEG    = 1
PAUSE_PRINT = False

exclude_a = []
exclude_b = []
take_always = None

NRML = {}

NO_LISTS = False


def create_df(path = FILE_PATH):
    df          = pd.read_hdf(path)
    df["date"]  = df["date"].map(str) + '-' +df["hour"].map(str)
    df['date']  = pd.to_datetime(df['date'],format=DATE_FORMAT)
    df          = df.set_index('date')

    return df

def group_A(df):
    global NRML
    result = {}
    for g1,n1 in df.groupby([df.index.month]) :
        result[g1] = {}
        mxs = {}
        for g2,n2 in n1.groupby([n1.index.weekday]) :
            result[g1][g2] = {}
            for g3,n3 in n2.groupby([n2.index.hour]) :
                result[g1][g2][g3]  = {}
                for g4,n4 in n3.groupby([n3['house_id']]):
                    mean = n4['value'].mean()
                    result[g1][g2][g3][g4] = n4['value'].mean()
                    mxs[g4] = mean if mean > mxs.get(g4,0) else  mxs.get(g4,0)

        for wd in result[g1] :
            for hr in result[g1][wd]:
                for hs in mxs :
                    result[g1][wd][hr][hs] = result[g1][wd][hr][hs]/mxs[hs]*1.0

    NRML = result
    return result


def calc_normalized():
    df = create_df()
    print ('Creating Normalized list')
    group_A(df)
    print (group_A(df))
    print ('Done')

def form_groups(date_hour_group,avg_h_cons,cut,shedding):
    global take_always
    take_always = None

    if NO_LISTS:
        houses = [[row['house_id'],row['value'],datetime.strptime(row['date']+'-'+str(row['hour']),DATE_FORMAT)] for index,row in date_hour_group.iterrows()]

    else :
        #Iterate the rows
        if len(exclude_a) == len(date_hour_group.index) :
            exclude_a.clear()
        houses = [[row['house_id'],row['value'],datetime.strptime(row['date']+'-'+str(row['hour']),DATE_FORMAT)] for index,row in date_hour_group.iterrows() if row['house_id'] not in exclude_a and  row['house_id'] not in exclude_b]

        if sum( [h[1] for h in houses]) < cut :
             exclude_a.clear()
             take_always = houses

             houses = [[row['house_id'],row['value'],datetime.strptime(row['date']+'-'+str(row['hour']),DATE_FORMAT)] for index,row in date_hour_group.iterrows() if \
                row['house_id'] not in exclude_a and  \
                row['house_id'] not in exclude_b and  \
                row['house_id'] not in [x[0] for x in take_always]
                ]


    groups = []

    #Get the right normalized group
    nrml = NRML[houses[0][2].month][houses[0][2].weekday()][houses[0][2].hour]
    nrml = {x:nrml[x] for x in nrml if x in [y[0] for y in houses]}
    nrml = list([list(x) for x in sorted(nrml.items(), key=operator.itemgetter(1))])
    for x in nrml :
        value = [y[1] for y in houses if y[0]==x[0]][0]
        x.insert(1,value)

    houses = nrml
    # print (houses)

    if take_always and len(take_always):
        #Do same for take_always
        nrml = NRML[take_always[0][2].month][take_always[0][2].weekday()][take_always[0][2].hour]
        nrml = {x:nrml[x] for x in nrml if x in [y[0] for y in take_always]}
        nrml = list([list(x) for x in sorted(nrml.items(), key=operator.itemgetter(1))])
        for x in nrml :
            value = [y[1] for y in take_always if y[0]==x[0]][0]
            x.insert(1,value)
        take_always = nrml

    while len(houses) :
        group = []
        if take_always:
            for al_tk in take_always :
                shedding[al_tk[0]] = shedding.get(al_tk[0],0)
                group.append(al_tk+[shedding.get(al_tk[0],0)])

        while sum( [h[1] for h in group]) <= cut and len(houses) :
            i = 0
            shedding[houses[i][0]] = shedding.get(houses[i][0],0)
            group.append(houses[i]+[shedding.get(houses[i][0],0)])
            del houses[i]

        groups.append(group)

    if sum([ h[1] for h in groups[-1] ]) < cut :
        groups = groups[:-1]

    return groups[:1],shedding

def calc_stds(group,hour):
    # exclude_b.clear()
    for g in group.groupby(['house_id']).groups :
        std  = np.std(group.loc[group['house_id'] == g]['value'])
        mean =  group.loc[group['house_id'] == g]['value'].mean()
        h    =  [x['value'] for i,x in group.loc[(group['house_id'] == g) & (group['hour'] == hour)].iterrows()] [0]

        # if h > (mean+2*std) :
        #     exclude_b.append(g)

def load_set():

    '''
    Load the data
    '''
    df                  = pd.read_hdf(FILE_PATH)
    calc_normalized()

    '''
    Calculate the hourly average
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
    discoms_i = []  ##
    discomforts2 = []  ## To calculate discomforts for every x load sheds!
    DISCOMS = []  ## To calculate discomforts for every x load sheds!
    discomforts = {}  ##

    for a,b in date_hour_groups.groups :
        print ('*'*60)
        print ('{} - {} - {}'.format(loads,a,b))
        try :
            avg_h_cons = df.loc[df['date'] == a]['value'].mean()*house_count

            # if not NO_LISTS:
            #     #stds = [np.std(df.loc[df['date'] == a]['value'])]
            #     calc_stds(df.loc[df['date'] == a],b)

            date_hour_group  = date_hour_groups.get_group((a,b))
            h_cons = date_hour_group['value'].sum()

            cut = h_cons - avg_h_cons
            load_cut = 0  ##
            discomfort = 0  ##

            if h_cons >= avg_h_cons :
                deficits.append(cut)  ##
                #Form groups
                groups,shedding = form_groups(date_hour_group,avg_h_cons,cut,shedding)

                #Shed, by the cumulative number of sheds in the group
                shed_sums = [[sum([h[3] for h in groups[i]]),i] for i in range(0,len(groups))]
                min_shed  = min([g[0] for g in shed_sums])
                g_index = [g[1] for g in shed_sums if g[0] == min_shed][0]
                #shed

                for h in groups[g_index] :
                    h[3] += 1
                    if np.isinf(h[2]) or np.isnan(h[2]) or h[2] < 0:  ##
                        h[2] = 0
                    discomforts[h[0]] = discomforts.get(h[0],0)+h[2] # Just changed
                    shedding[h[0]] = h[3]
                    if not NO_LISTS :

                        if not take_always or  h[0] not in [x[0] for x in take_always]:
                            exclude_a.append(h[0])

                for hs in groups[g_index] :
                    load_cut += hs[1]  ##

                    if np.isinf(hs[2]) or np.isnan(hs[2]):  ##
                        hs[2] = 0  ##
                    discomfort += hs[2]  ##

                    print('ID : {:>10.0f}, CONS : {:>10.2f}, NRMLZD AVERAGE : {:>10.2f}, SHED : {:>10.2f}, DISC : {:>10.2f}'.format(hs[0],hs[1],hs[2],hs[3],discomforts.get(hs[0],0)))
                number_shed +=len(groups[g_index])
                num_shed = len(groups[g_index])  ##

                print ('CUT : {:>10.2f}, CONSUMPTION {:>10.2f}'.format(cut,h_cons))
                print ('Excluded SHED')
                print (exclude_a)
                print ('Excluded STD')
                print (exclude_b)
                loads +=1

                loads_cut.append(load_cut)  ##
                numbers_shed.append(num_shed)  ##
                discoms_i.append(discomfort)  ##
                discomforts2.append(discomfort)  ## To calculate discomforts for every x load sheds!


            if loads % LOAD_SEG == 0 and loads not in x :
                full_df = pd.DataFrame(list(shedding.items()),columns = ['house','shedding']).set_index('house')

                if last_df is None :
                    last_df = full_df.copy(True)
                    last_df['shedding'] = 0

                now_df = full_df.subtract(last_df,axis=1)
                now_df['total'] = full_df['shedding']
                last_df = full_df.copy(True)



                print ('*'*60)
                print ('LAST {}/{} LOADS '.format(LOAD_SEG,loads))

                print ('MAX : HOUSE {}, SHEDS {}'.format(now_df['shedding'].argmax(),now_df['shedding'].max()))
                print ('MIN : HOUSE {}, SHEDS {}'.format(now_df['shedding'].argmin(),now_df['shedding'].min()))
                print ('NUMBER OF HOUSES SHED : {}'.format(number_shed))

                x.append(loads)
                y.append(number_shed)
                DISCOMS.append(sum(discomforts2))
                yx.append(now_df['shedding'].max())
                ym.append(now_df['shedding'].min())
                number_shed = 0
                discomforts2 = []  ## To calculate discomforts for every x load sheds!

            if PAUSE_PRINT :
                input()
        except Exception as e :
            print (e)
            pass

    print ('*'*60)
    print ('TOTAL LOADS')
    print ('MAX : HOUSE {}, SHEDS {}'.format(full_df['shedding'].argmax(),full_df['shedding'].max()))
    print ('MIN : HOUSE {}, SHEDS {}'.format(full_df['shedding'].argmin(),full_df['shedding'].min()))
    total_shed = len(full_df.loc[full_df['shedding'] != 0])
    print ('TOTAL HOUSES SHED : {}'.format(total_shed))

    print (x)
    print (yx)
    print (ym)
    print (y)

    print(discomforts)  ### This is a dictionary with ID as key and aggregated discomfort as value over the entire shedding period
    print (sorted(discomforts.items(), key=operator.itemgetter(1)))

    max_value = max(discomforts.values()) # Getting the maximum discomfort value from dictionary
    max_keys = [k for k, v in discomforts.items() if v == max_value]  # getting all keys containing the maximum
    # print(max_value, max_keys)

    min_value = min(discomforts.values()) # Getting the minimum discomfort value from dictionary
    min_keys = [k for k, v in discomforts.items() if v == min_value]  # getting all keys containing the minimum
    # print(min_value, min_keys)


    overall_discomfort = sum(discomforts.values()) # Summing up all discomfort values in dictionary
    # print(overall_discomfort)

    utilitarian = overall_discomfort
    egalitarian = max_value
    envy_freeness = max_value - min_value

    # print (utilitarian, egalitarian, envyness)
    print('Utilitarian : {:>10.2f}, Egalitarian : {:>10.2f}, Envy-freeness : {:>10.2f}'.format(utilitarian, egalitarian, envy_freeness))
    print ('Number of houses shed : {:>10.0f}'.format(sum(y)))
    print('Discomfort caused per house shed : {:>10.2f}'.format(utilitarian/sum(y)))

    # print(discoms_i)
    # overall_discom = sum(discoms_i)
    # print(overall_discom)

    # print(DISCOMS)   ### DISCOMS IS PER X NUMBER OF SHEDS!!!
    # overall_DISCOMS = sum(DISCOMS)
    # print(overall_DISCOMS)


    # plt.bar(x,y,width=LOAD_SEG/2.0,color='r',align='center')
    # plt.title('Sheds')
    # plt.show()
    #
    # p1 = plt.bar(x, yx, LOAD_SEG/2.0, color='g' )
    # plt.title('Max')
    # plt.show()
    #
    # p2 = plt.bar(x, ym, LOAD_SEG/2.0, color='b')
    # plt.title('min')
    # plt.show()


    # ticks = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    #
    # plt.bar(x,y,width=LOAD_SEG/2.0,color='b',align='center',label = 'Sheds')
    # plt.xlabel('Every 100 shedding events')
    # plt.ylabel('Number of households shed')
    # plt.xticks(ticks, rotation='horizontal')
    # plt.ylim([0, max(y)* 1.3])
    # plt.show()
    #
    # p1 = plt.bar(x, yx, LOAD_SEG/2.0, color='b',label = 'Max')
    # p2 = plt.bar(x, ym, LOAD_SEG/2.0, color='r',bottom=yx)
    # plt.xlabel('Every 100 shedding events')
    # plt.ylabel('Number of households shed')
    # plt.xticks(ticks, rotation='horizontal')
    # plt.legend((p1[0], p2[0]),('Number of sheds of household most shed','Number of sheds of household least shed'),
    #            fontsize=10, ncol = 1, framealpha = 0, fancybox = True)
    # plt.ylim([0, max([sum(x) for x in zip(yx,ym)])*1.3])
    # plt.show()
    #
    #
    #
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






    # plt.bar(x, DISCOMS, LOAD_SEG/2.0, color='b',label = 'Max')
    # plt.xlabel('Every x shedding events')
    # plt.ylabel('Discomfort caused')
    # plt.xticks(x, rotation='horizontal')
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



    # # For plotting number of households shed per unit load cut (first 50 sheds)
    # w2 = 0.5
    # plt.xlabel('Number of shedding events')
    # plt.ylabel('Households disconnected per kW shed')
    # label_x = range(1, 51)
    # plt.bar(label_x, [x/y for x, y in zip(numbers_shed[:50], deficits[:50])], width = w2, color='b')
    # plt.xlim([(min(label_x) - w2), (max(label_x) + w2)])
    # plt.ylim([0,max([x/y for x, y in zip(numbers_shed[:50], deficits[:50])])*1.1])
    # plt.show()

    # dplc_4 = [x/y for x, y in zip(numbers_shed[:50], deficits[:50])]
    # print (dplc_4)
