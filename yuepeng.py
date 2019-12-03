import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

##needed files : 'summary_2017.xlsx' 'transportation_CO2_by_state_2017.xlsx'
                # 'Insurance.csv'  'maintenance_cost_brands.csv'

##### picture in environment factor
def plotEn_pic():
    '''
    Plot the picture of the ratio of co2 emissions in transportation over total emissions
    '''

    ##emission in total across USA
    dataS = pd.read_excel('summary_2017.xlsx')
    dataS = dataS[1:]
    data1 = np.asarray(dataS[54:55])
    data2 = np.asarray(data1[0][1:29])

    ## in transportation
    data = pd.read_excel('transportation_CO2_by_state_2017.xlsx')
    dataU = data.copy()
    numpyArray = np.asarray(dataU)
    y = numpyArray[53]
    x = numpyArray[1]
    x2 = x[1:39].astype(int)
    y2 = y[1:39].astype(float)
    x2 = x2[10:]
    y2 = y2[10:]
    y = y2 / data2

    ##plot

    #plt.figure(dpi=600)
    ax = plt.subplot(111)
    ax.plot(x2, y)
    plt.ylabel('Ratio')
    plt.xlabel('Year')
    plt.title(r'Ratio of CO$_2$ Emissions in Transportation over Total Emissions',
              fontdict={'fontsize': 10, 'fontweight': 'bold'})
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    from matplotlib import rcParams
    rcParams['axes.titlepad'] = 30
    # plt.savefig('image')
    plt.show()


def plot_insurance():
    '''
    Plot the picture of 3 highest and 3 lowest car brands with respect to the
    average yearly insurance
    '''
    insurance = pd.read_csv('Insurance.csv')
    copy1 = insurance.copy()
    # compute average cost of each car model
    copy1['Model'] = 0
    copy1['Make'] = 0
    copy2 = insurance.copy()
    copy2['average'] = copy1.sum(axis=1) / 52
    copy3 = copy2.groupby('Make')
    names = list(set(insurance['Make']))

    res = {}
    for name in names:
        c = copy3.get_group(name)
        res[name] = c.sum()['average'] / c.shape[0]
    names.sort(key=lambda x: res[x])
    x1, x2 = names[0:3], names[-3:]
    x = x1 + x2  ## brand names

    y = []  ##insurance cost
    for i in x:
        y.append(res[i])

    ##plot:

    #plt.figure(dpi=200, figsize=(8, 6))
    ax = plt.subplot(111)
    ax.bar(x, y, width=0.8)
    plt.ylabel('Average Insurance Per Year($)', fontdict={'fontsize': 12})
    plt.title('3 Highest Brand and 3 Lowest Brand')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xticks(x, x, rotation='45')
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    plt.show()


def plot_maintenance():
    '''
    Plot the picture of 3 highest and 3 lowest car brands with respect to the
    average yearly maintenance cost
    '''
    maintenance = pd.read_csv('maintenance_cost_brands.csv')
    maintenance = maintenance.sort_values('Cost')
    brands = list(maintenance['Car Brand'])
    costs = list(maintenance['Cost'])
    top3, top3Cost = brands[10:13], costs[10:13]
    low3, low3Cost = brands[13:16], costs[13:16]
    x, y = low3 + top3, low3Cost + top3Cost
    for i in range(len(y)):  ## yearly
        cost = re.sub(r'[$,]', '', y[i])
        y[i] = int(cost) / 10
    ###plot:

    #     plt.figure(dpi=200, figsize=(8, 6))
    ax = plt.subplot(111)
    ax.bar(x, y, width=0.8)
    plt.ylabel('Maintenance Cost Per Year($)', fontdict={'fontsize': 12})
    plt.title('3 Highest Brand and 3 Lowest Brand')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xticks(x, x, rotation='45')
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    plt.show()


# environment functions are contained in Yuxuan's code
# call plotEn_pic() plot_insurance() plot_maintenance() to plot

