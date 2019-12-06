import pandas as pd
import requests


def fuse_rows(df, n):
    """
    Concatenates the first n rows into a single row
    for a given dataframe df.

    """
    for row in range(1,n):
        for col in range(len(df.values[0])):
            if isinstance(df.values[row][col],str):
                if isinstance(df.values[0][col], str):
                    df.values[0][col] = df.values[0][col] + ' ' + df.values[row][col]
                else:
                    df.values[0][col] = df.values[row][col]


def scrape_sales_data():
    """
    Function used to scrape and clean data

    List of Plots:
    Plot1: 2017 State Motor Vehicle Registration
    Plot2a: Production of Automobiles
    Plot2b: Market Share
    Plot2c: Fuel Economy
    Plot3a: Hybrid and Electric Vehicle Sales
    Plot3b: Total Vehicle Sales
    Plot4a: US Vehicle Model Sales of the Last Month
    Plot4b: US Vehicle Model Sales by Month

    Currently exports Plot3a and Plot4b as csv files
    """
    url = 'https://www.fhwa.dot.gov/policyinformation/statistics/2017/xls/mv1.xlsx'
    df = pd.read_excel(url, header=[6])
    fuse_rows(df,4)
    df = df.drop([1,2,3,56])
    x = df.columns
    df.columns = ['State', x[1], x[1], x[1], x[4], x[4], x[4], x[7], x[7], x[7], x[10], x[10], x[10], x[13], x[13], x[13]]
    Plot1 = df

    url = 'https://www.bts.gov/sites/bts.dot.gov/files/table_01_20_052019.xlsx'
    df = pd.read_excel(url,header=1)
    df1 = df.iloc[:6,:]
    df2 = df.iloc[6:12,:]
    df3 = df.iloc[12:18,:]
    Plot2a = df1
    Plot2b = df2
    Plot2c = df3

    url = 'https://cms.bts.gov/sites/bts.dot.gov/files/table_01_19q418.xlsx'
    df = pd.read_excel(url,header=1,index_col=0)
    Plot3a = df.iloc[:3,:]

    url = 'https://www.bts.gov/sites/bts.dot.gov/files/table_01_16_062019.xlsx'
    df = pd.read_excel(url,header=1)
    Plot3b = df.iloc[:1,:]

    url = 'https://www.goodcarbadcar.net/2019-us-vehicle-sales-figures-by-model/#vwspc-section-5'
    html = requests.get(url).content
    df_list = pd.read_html(html)
    Plot4a = df_list[0].iloc[:193,:7]
    Plot4b = df_list[1].iloc[:297,:13]
    Make = []
    Model = []
    for i in Plot4b["Model"]:
        words = i.split(' ')
        if words[0] == 'Alfa' or words[0] == 'Land':
            print('In')
            Make.append(' '.join(words[:2]))
            Model.append(' '.join(words[2:]))
        else:
            Make.append(words[0])
            Model.append(' '.join(words[1:]))
    Plot4b['Make'] = Make
    Plot4b['Model'] = Model
    Plot4b = Plot4b[['Make', 'Model', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]

    GraphA = Plot3a.iloc[:,12:].T
    GraphA.to_csv('data/ElectricSales.csv')
    Plot4b.to_csv('data/CarSales.csv')
