import os
import re

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from data_analysis.df_gen import get_df


def get_sales_df(data_file="data/ElectricSales.csv"):
    """
    Reads the sales file and return the dataframe
    :param data_file: name of the file
    :return: dataframe
    """
    assert os.path.exists(data_file)

    df = pd.read_csv(data_file, index_col=0)
    df['Electric'] = df['Electric'] / 1000
    df['Plug-in hybrid-electric'] = df['Plug-in hybrid-electric'] / 1000
    return df


def plot_sales_trend(sales_df):
    df = sales_df
    fig, ax = plt.subplots(dpi=200)
    ax.set_xlabel('Year', fontsize='14')
    ax.set_ylabel('Sales in Thousands', fontsize='14')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.plot(df.index, df.Electric, label='Electric', color='limegreen')
    ax.plot(df.index, df.Electric, '.', color='limegreen')
    ax.plot(df.index, df['Plug-in hybrid-electric'],
            label='Hybrid-Electric(Plug-In)', color='blue')
    ax.plot(df.index, df['Plug-in hybrid-electric'], '.', color='blue')
    ax.legend(loc='upper left')
    plt.title('Electric Vehicle Sales')
    plt.tight_layout()
    plt.show()
    fig.savefig('ElectricSales.png')


def get_sales_projection(df):
    z1 = np.polyfit(df.index, df.Electric, 2)
    z2 = np.polyfit(df.index, df['Plug-in hybrid-electric'], 2)
    p1 = np.poly1d(z1)
    p2 = np.poly1d(z2)

    return p1, p2


def plot_sales_projection(sales_df):
    df = sales_df

    p1, p2 = get_sales_projection(df)

    fig, ax = plt.subplots(dpi=200)
    ax.set_xlabel('Year', fontsize='14')
    ax.set_ylabel('Sales in Thousands', fontsize='14')
    ax.yaxis.set_ticks(np.arange(0, 170, 40))
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    xp = np.linspace(2011, 2022, 100)
    ax.plot(df.index, df.Electric, label='Electric', color='limegreen')
    ax.plot(df.index, df.Electric, '.', color='limegreen')
    ax.plot(df.index, df['Plug-in hybrid-electric'],
            label='Hybrid-Electric(Plug-In)', color='blue')
    ax.plot(df.index, df['Plug-in hybrid-electric'], '.', color='blue')
    ax.plot(xp, p1(xp), '--', label='Electric Projection', color='limegreen')
    ax.plot(xp, p2(xp), '--', label='Hybrid Projection', color='blue')
    ax.legend(loc='upper left')
    plt.tight_layout()
    plt.show()
    fig.savefig('ElectricSalesProjection.png')


def plot_total_sales():
    data1 = 'data/TotalSales.csv'
    df = pd.read_csv(data1, index_col=0)

    fig, ax = plt.subplots(dpi=200)
    ax.set_xlabel('Year', fontsize='14')
    ax.set_ylabel('Sales in Thousands', fontsize='14')
    ax.set_ylim([0, 12000])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.plot(df.index, df['Total new passenger car sales'], color='dimgrey')
    ax.plot(df.index, df['Total new passenger car sales'], '.',
            color='dimgrey')
    plt.title('Total Car Sales')
    plt.tight_layout()
    plt.show()
    fig.savefig('TotalSales.png')


def get_total_sales_prediction():
    data = 'data/TotalSalesFullExtra.csv'
    df = pd.read_csv(data, index_col=0)
    z = np.polyfit(df.index, df['Total new passenger car sales'], 2)
    p3 = np.poly1d(z)

    return p3, df


def plot_sales_prediction():
    p3, df = get_total_sales_prediction()
    fig, ax = plt.subplots()
    ax.set_xlabel('Year')
    ax.set_ylabel('Sales in Thousands')
    ax.set_ylim([0, 12000])

    xp = np.linspace(1970, 2022, 100)
    ax.plot(df.index, df['Total new passenger car sales'],
            label='Total New Passenger Car Sales', color='blue')
    ax.plot(xp, p3(xp), '--', label='Total Sales Projection')
    ax.legend(loc='lower left')
    plt.show()
    fig.savefig('TotalSalesPrediction.png')


def plot_market_analysis(electric_sales_df, total_sales_df):
    GraphC = pd.concat([electric_sales_df.T, total_sales_df.T]).T
    GraphC['Electric'] = GraphC['Plug-in hybrid-electric'] + GraphC['Electric']
    GraphC['Electric'] = GraphC['Electric'] / 1000
    GraphC = GraphC.iloc[:, 2:]
    titles = ['Total new passenger car sales', 'Electric']
    GraphC = GraphC.reindex(columns=titles)
    GraphC['Percentage'] = GraphC['Electric'] / GraphC[
        'Total new passenger car sales']

    labels = ['Electric', 'Gas']
    p1, p2 = get_sales_projection(electric_sales_df)
    p3, _ = get_total_sales_prediction()

    sizes = [p1(2021) + p2(2021), (p3(2021)) - (p1(2021) + p2(2021))]
    explode = (0.3, 0)
    colors = ['limegreen', 'silver']
    fig1, ax1 = plt.subplots(dpi=200)
    ax1.pie(sizes, labels=labels, colors=colors, explode=explode,
            autopct='%1.1f%%', shadow=False, startangle=160,
            textprops={'fontsize': 14})
    ax1.axis('equal')
    plt.title('2021 (Projected)')
    plt.tight_layout()
    plt.show()
    fig1.savefig('Market2021.png')

    labels = ['Electric', 'Gas']
    sizes = [p1(2011) + p2(2011), (p3(2011)) - (p1(2011) + p2(2011))]
    explode = (0.3, 0)
    colors = ['limegreen', 'silver']
    fig1, ax1 = plt.subplots(dpi=200)
    ax1.pie(sizes, labels=labels, colors=colors, explode=explode,
            autopct='%1.1f%%', shadow=False, startangle=160,
            textprops={'fontsize': 14})
    ax1.axis('equal')
    plt.title('2011')
    plt.tight_layout()
    plt.show()
    fig1.savefig('Market2011.png')


def plot_yearly_cost_comaprison():
    """

    :return:
    """
    df1 = get_df(user_id=60000)
    df2 = get_df(user_id=120000)
    df3 = get_df(user_id=180000)

    df1['Yearly'] = (df1['total'] - df1['base']) / 10
    df1 = df1.sort_values('Yearly')
    df2['Yearly'] = (df2['total'] - df2['base']) / 10
    df2 = df2.sort_values('Yearly')
    df3['Yearly'] = (df3['total'] - df3['base']) / 10
    df3 = df3.sort_values('Yearly')

    de1 = df1[df1['fuel_type'] == 'e'][:7]['Yearly'].mean()
    dg1 = df1[df1['fuel_type'] == 'g'][:45]['Yearly'].mean()
    de2 = df2[df2['fuel_type'] == 'e'][:7]['Yearly'].mean()
    dg2 = df2[df2['fuel_type'] == 'g'][:45]['Yearly'].mean()
    de3 = df3[df3['fuel_type'] == 'e'][:7]['Yearly'].mean()
    dg3 = df3[df3['fuel_type'] == 'g'][:45]['Yearly'].mean()

    e = (de1, de2, de3)
    g = (dg1, dg2, dg3)
    ind = np.arange(3)
    width = 0.45
    fig, ax = plt.subplots(dpi=200)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    rects1 = ax.bar(ind + width, e, width, color='limegreen')
    rects2 = ax.bar(ind, g, width, color='dimgrey')
    ax.set_ylabel('Yearly Cost')
    ax.set_ylim([2000, 3750])
    ax.yaxis.set_ticks(np.arange(2000, 3750, 400))
    ax.set_xlabel('Miles Per Year')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(('6000', '12000', '18000'))
    ax.legend((rects2[0], rects1[0]), ('Gas', 'Electric'), loc='upper left')
    plt.tight_layout()
    plt.show()
    fig.savefig('YearlyEvG.png')


# needed files : 'summary_2017.xlsx' 'transportation_CO2_by_state_2017.xlsx'
# 'Insurance.csv'  'maintenance_cost_brands.csv'

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


def plot_costs_pie(costs_dict, title):
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200, subplot_kw=dict(aspect="equal"))

    costs = list(costs_dict.keys())
    data = [costs_dict[key] for key in costs]

    t = []
    for c in costs:
        if c != "env":
            t.append(c.title())
        else:
            t.append("Environment")

    def func(pct):
        return "{:.1f}%".format(pct)

    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct), pctdistance=0.75,
                            textprops=dict(color="w"), wedgeprops=dict(width=0.5), startangle=-40)

    plt.setp(autotexts, size=16, weight="bold")

    bbox_props = dict(boxstyle="square,pad=0.4", fc="w", ec="k", lw=0)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(t[i], xy=(x, y), xytext=(1.25*np.sign(x), 1.2*y),
                    horizontalalignment=horizontalalignment, fontsize=18, **kw)

    ax.set_title(title, fontsize=20)

    plt.show()


def plot_all_cars_costs_pie(df):
    national = df[["base", "fuel", "maintenance", "insurance", "env"]]
    avg = dict(national.mean())
    plot_costs_pie(avg, "Average Cost Breakdown")


def plot_electric_cars_costs_pie(df):
    electric = df[df["fuel_type"] == "e"]
    avg_e = dict(electric[["base", "fuel", "maintenance", "insurance"]].mean())
    plot_costs_pie(avg_e, "Electric Vehicle Cost Breakdown")


def plot_gasoline_cars_costs_pie(df):
    gas = df[df["fuel_type"] == "g"]
    avg_g = dict(gas[["base", "fuel", "maintenance", "insurance", "env"]].mean())
    plot_costs_pie(avg_g, "Gasoline Vehicle Cost Breakdown")


def plot_cheapest_cars(df, k=5, name=""):
    topk = df.nsmallest(k, "total")

    fig, ax = plt.subplots(figsize=(10, 7), dpi=200)

    # Example data
    cars = [s.replace("Chevrolet", "Chevy") for s in list(topk["name"])]

    x_pos = np.arange(k)

    buffer = np.zeros(k)
    names = []

    for col in topk.columns[2:-1]:
        if col != "env":
            l = col.title()
        else:
            l = "Environment"

        ax.bar(x_pos, list(topk[col]), align='center', bottom = buffer, label=l)
        buffer += np.array(topk[col])

    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.set_xticks(x_pos)
    ax.set_xticklabels(cars, fontsize=12)
    ax.set_yticks(np.arange(0, 140000, 20000))
    ax.set_ylabel('Total Cost ($)', fontsize=14)
    ax.legend(fontsize=14)
    ax.set_title('Top 5 Cheapest {} Cars'.format(name), fontsize=18)
    plt.xticks(rotation=30)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(12)

    plt.show()

