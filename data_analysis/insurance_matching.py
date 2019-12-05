import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import heapq
import math


def create_manual_checklist():
    """
    for fuzzy matching, create a manual checklist for human
    to each make matching decisions
    :param: none
    :type: none

    :return: none
    """
    car_data = pd.read_csv('data/car_data_kaggle.csv')
    insurance_data = pd.read_csv('data/insurance.csv')

    make_model_str_set = set()

    for row in insurance_data[['Make', 'Model']].iterrows():
        make_model_str_set.add(" ".join([row[1]['Make'], row[1]['Model']]))
    print(make_model_str_set)

    cars_cleaned_df = pd.read_csv('data/cars_cleaned_grouped.csv')

    name_map = dict()
    manual_df = pd.DataFrame(columns = ['First', "Second", "Third"])
    good_match_count = 0
    for name in cars_cleaned_df['name']:
        make_model_name = name[5:len(name)]
        h = []
        for known_name in make_model_str_set:
            score = fuzz.ratio(make_model_name, known_name)
            if score == 100:
                h = [(score, (name, known_name))]
                name_map[name] = known_name
                good_match_count += 1
                break
            else:
                heapq.heappush(h, (score, (name, known_name)))
        while (len(h)) > 3:
            heapq.heappop(h)

        if (len(h)) > 1:
            manual_df = manual_df.append({'First': heapq.heappop(h),
                                          'Second': heapq.heappop(h),
                                          'Third': heapq.heappop(h)},
                                         ignore_index=True)
    manual_df.to_csv("data/manual_checklist.csv")
    return name_map


def read_manual_checklist(manual_checklist, name_map):
    """
    read back decision checklist after manual decisions
    :param: manual_checklist, name_map
    :type: str, map

    :return: DataFrame
    """
    manual_decision = pd.read_csv(manual_checklist)
    insurance_data = pd.read_csv('data/insurance.csv')
    for row in manual_decision.iterrows():
        if (not math.isnan(row[1]['Choice']) and
                row[1]['Choice'] != 0 and row[1]['Choice'] in [0,1,2,3]):
            decision_str = list(row[1][['First', 'Second',
                                        'Third']])[int(row[1]['Choice']) - 1]
            decision = decision_str.split(',')
            decision[1] = (decision[1]
                           .replace('(','')
                           .replace(')','')
                           .replace("""'""",'')
                           .strip(' '))
            decision[2] = (decision[2]
                           .replace('(','')
                           .replace(')','')
                           .replace("""'""",'')
                           .strip(' '))
            assert decision[1] not in name_map.keys(), decision[1]
            name_map[decision[1]] = decision[2]
    make_model_str_set = set()
    for row in insurance_data[['Make', 'Model']].iterrows():
        make_model_str_set.add(" ".join([row[1]['Make'], row[1]['Model']]))

    insurance_data = pd.read_csv('data/insurance.csv')
    assembled_name = list()
    for row in insurance_data.iterrows():
        assembled_name.append(" ".join([row[1]['Make'], row[1]['Model']]))
    insurance_data.insert(loc=len(insurance_data.columns),
                          column='assembled_name', value=assembled_name)

    cars_cleaned_df = pd.read_csv('data/cars_cleaned_grouped.csv')

    insurance_data['price'] = np.nan
    insurance_data['city_mpg'] = np.nan
    insurance_data['highway_mpg'] = np.nan
    for car in cars_cleaned_df.iterrows():
        if car[1]['name'] in name_map:
            i = (insurance_data[insurance_data['assembled_name'] ==
                                name_map[car[1]['name']]]['assembled_name'].index)
            insurance_data.loc[i,'price'] = car[1]['price']
            insurance_data.loc[i,'city_mpg'] = car[1]['city_mpg']
            insurance_data.loc[i,'highway_mpg'] = car[1]['highway_mpg']

    insurance_msrp_data = insurance_data[insurance_data['price'] > 0]
    return insurance_msrp_data
