import pandas as pd
import numpy as np


## data source : https://www.eia.gov/tools/faqs/faq.php?id=74&t=11
dataElectric = pd.read_excel('data/annual_generation_state.xls')
dataCarbon = pd.read_excel('data/emission_annual.xls')

### preprocessing data:
dataCarbon= dataCarbon[dataCarbon['Year']==2018]
dataCarbon = dataCarbon[dataCarbon['State']!='DC']
dataCarbon = dataCarbon[dataCarbon['State']!= 'US-TOTAL']
dataCarbon = dataCarbon[dataCarbon['Energy Source'] == 'All Sources']
dataCarbon = np.asarray(dataCarbon)

## for electricity data :
dataElectric.reindex(['a','b','c','d','e','f'])
b=dataElectric.columns
columns = ['year','state','type','resource','generation']
dic,i = {},0
for j in range(len(columns)):
    dic[b[j]] = columns[j]
E = dataElectric.rename(columns=dic)
E = E[E['year']==2018]
E
E = E[E['resource'] == 'Total']
E = E[E['state'] != 'DC']
E = E[E['state'] != 'US-Total']
E = E[E['type'] == 'Total Electric Power Industry']
E = np.asarray(E)
dataElectric = E
#################


def emissionDict(dataCarbon) :
    """
    @dataCarbon : Carbon emission data
    @return : a dictionary with key = state name, value = CO2 emission
    """
    assert isinstance(dataCarbon, pd.DataFrame)
    prev = 'AK'
    index,sumOfEmissions = 0,0
    emissionDict = {}
    for i in range(len(C)) :
        item = C[i]
        if item[1]!=prev :
            emissionDict[prev] = sumOfEmissions
            sumOfEmissions = item[4]
            prev = item[1]
        else :
            sumOfEmissions += item[4]
    emissionDict['Wyoming'] = sumOfEmissions
    return emissionDict


def ele_generation(dataElectric) :
    """
    @dataElectric : electricity generation in each state
    @return : a dictionary with key = state name, value = electricity generation
    """
    assert isinstance(dataElectric,pd.DataFrame)
    generationDict = {}
    for i in range(len(dataElectric)) :
        item = dataElectric[i]
        generationDict[item[1]] = item[4]
    return generationDict


def co2_per_mwh(generationDict,emissionDict) :
    """
    @dataElectric : annual electricity generation in each state
    @dataCarbon : annual CO2 emission generation in each state
    @return : a dictionary with key = states name, value : CO2 emission per mwh electricity
    """
    assert isinstance(generationDict,dict)
    assert isinstance(emissionDict,dict)
    perMPH = {}
    for name in generationDict :
        perMPH[name] = emissionDict[name]*1.0 / generationDict[name]
    return perMPH


def generate_csv(perMPH) :
    """
    This function writes a csv file with state name as index and
    the value of CO2 generation per mwh electricity as column
    @perMPH : a dictionary
    """
    my_dict = perMPH
    with open('co2_mwh.csv', 'w') as f:
        f.write('states,co2/mwh\n')
        for key in my_dict.keys():
            f.write("%s,%s\n"%(key,my_dict[key]))
