import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import numpy as np

state_list = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI",
              "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI",
              "MN", "MO", "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV",
              "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT",
              "VA", "VT", "WA", "WI", "WV", "WY"]

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Washington DC': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}


# MPGe to Kwh/1mile :
#     kwh/100km = 3370.5 / 1.609344 / MPGe
#     kwh/1km = kwh/100km /100
#     kwh/1mile = kwh/1km / 0.621371
#   ->kwh/1mile = 33.7 / MPGe
# This function is created by Yuepeng, Jiang
def ele_Cost(miles, elePrice, MPGe):
    '''
    @miles : total miles for a certain type of user
    @elePrice : electricity price in each state
    @MPGe : EV car's MPGe
    @return : total cost in dollars for charging EV
    '''
    totalEle = miles * 33.7 / MPGe
    return totalEle * elePrice  # eleprice should be in dollars/kwh


# This function is created by Yuepeng, Jiang
def fuel_Cost(miles, fuelPrice, mpg):
    """
    @milse: total miles
    @fuelPrice : gas price in specific state
    @mpg: fuel car's mpg
    @return : total fuel cost in dollars
    """
    totalGallon = miles / mpg
    return fuelPrice * totalGallon  # fuelPrice should be in dollars/gallon


# Environment Cost:
#     the average price to reduce 1 ton of CO2 is 50$
#     Accoring to mpg we know miles/gallon; 8.89kg CO2 is generated per gallon; So we know that how much is it to reduce CO2.
#     For EV cars, we get data of how much CO2 is generated per mwh(Electricity unit) in each states. So we can know how much is it to reduce co2 for ev
# This function is created by Yuepeng, Jiang
def env_fuel_car(miles, mpg, mPerGallon=8.89, priceToReduce=50):
    '''
    @miles : total miles for a certain type of user
    @mpg : fuel car's mpg
    @return : environment cost for fuel car
    '''
    # a typical cost is around 3000 dollars for medium user

    totalGallon = miles / mpg
    totalCO2 = totalGallon * 8.89 / 1000  # in tons
    totalCost = totalCO2 * priceToReduce
    return totalCost


# This function is created by Yuepeng, Jiang
def env_ev_car(miles, mpge, co2_per_mwh, priceToReduce=50):
    """
    @miles : total miles for a certain type of user
    @mpge: ev car's mpge
    @co2_per_mwh : how much CO2 is generated per mwh
    """
    totalEle = miles * 33.7 / mpge / 1000  # in mwh
    totalCO2 = totalEle * co2_per_mwh
    totalCost = totalCO2 * priceToReduce
    return totalCost


def import_all_data():
    """
    import all data files
    :param: none
    :type: none

    :return: DataFrame, DataFrame, DataFrame, DataFrame, DataFrame, DataFrame
    """
    insurance_msrp = pd.read_csv('data/insurance_msrp_data.csv')

    electricity_data = pd.read_excel('data/eia_gov.xlsx')
    electricity_data = electricity_data.set_index('state')

    gas_price = pd.read_csv('data/gas-prices_2019-11-08.csv')
    state_abbr = list()
    for row in gas_price.iterrows():
        state_abbr.append(us_state_abbrev[row[1]['states']])
    gas_price.insert(loc=0, column='state_abbr', value=state_abbr)
    gas_price = gas_price.set_index('state_abbr')
    # gas_price['state_abbr']

    co2_mwh = pd.read_csv('data/co2_mwh.csv')
    co2_mwh = co2_mwh.set_index('states')
    # co2_mwh

    maintenance_data = pd.read_csv('data/maintenance_cost_brands.csv')
    maintenance_data = maintenance_data.set_index('Car Brand')
    # maintenance_data

    fuel_economy_data = pd.read_csv('data/fueleconomy_vehicles.csv', header=0)
    fuel_economy_data = fuel_economy_data[
        ['make', 'model', 'city08', 'highway08', 'fuelType1', 'mpgData',
         'year']]
    fuel_economy_data = fuel_economy_data[fuel_economy_data["year"] > 2018]

    return insurance_msrp, electricity_data, gas_price, co2_mwh, maintenance_data, fuel_economy_data


def build_model_data_dict(insurance_msrp, electricity_data, gas_price, co2_mwh,
                          maintenance_data, fuel_economy_data,
                          mpg_threshold=70):
    """
    aggregate all dataframe into one master dictionary
    :param: insurance_msrp, electricity_data, gas_price, co2_mwh, maintenance_data, fuel_economy_data, mpg_threshold
    :type: DataFrame, DataFrame, DataFrame, DataFrame, DataFrame, DataFrame, int

    :return: dict
    """

    master_dict = dict()

    for car_info in insurance_msrp.iterrows():

        mpg = 0.55 * car_info[1]['city_mpg'] + 0.45 * car_info[1]['highway_mpg']
        if mpg == 0:
            brand_data = fuel_economy_data[
                fuel_economy_data['make'] == car_info[1]['Make']]
            best_score = -1
            best_match = ''
            for candidate in brand_data.iterrows():
                score = fuzz.ratio(candidate[1]['model'], car_info[1]['Model'])
                if score > best_score:
                    best_score = score
                    best_match = candidate[1]
            mpg = 0.55 * candidate[1]['city08'] + 0.45 * candidate[1][
                'highway08']

        car_name = ' '.join([car_info[1]['Make'], car_info[1]['Model']])

        master_dict[car_name] = dict()
        master_dict[car_name]['base'] = car_info[1]['price']
        master_dict[car_name]['maintenance'] = int(
            maintenance_data.at[car_info[1]['Make'], 'Cost'].replace("$",
                                                                     "").replace(
                ",", ""))
        master_dict[car_name]['fuel_type'] = 'e' if mpg > mpg_threshold else 'g'
        master_dict[car_name]['insurance'] = dict()  # by state

        master_dict[car_name]['user_type'] = dict()
        for mileage in [60000, 120000, 180000]:
            master_dict[car_name]['user_type'][mileage] = dict()
            master_dict[car_name]['user_type'][mileage][
                'fuel_cost'] = dict()  # by state
            master_dict[car_name]['user_type'][mileage][
                'env_cost'] = dict()  # by state
            master_dict[car_name]['user_type'][mileage]['total_cost'] = dict()
            master_dict[car_name]['user_type'][mileage]['total_cost'][
                'with_env'] = dict()  # by state
            master_dict[car_name]['user_type'][mileage]['total_cost'][
                'no_env'] = dict()  # by state

        for state in state_list:
            for mileage in [60000, 120000, 180000]:

                if mpg >= mpg_threshold:
                    # for EV
                    electricity = electricity_data.at[state, '201908'] / 100
                    fuel_cost = ele_Cost(mileage, electricity, mpg)
                    env_cost = env_ev_car(mileage, mpg,
                                          co2_mwh.at[state, 'co2/mwh'])
                else:
                    # for fuel car
                    gas = gas_price.at[state, 'prices']
                    fuel_cost = fuel_Cost(mileage, gas, mpg)
                    env_cost = env_fuel_car(mileage, mpg)

                maintenance_cost = int(
                    maintenance_data.at[car_info[1]['Make'], 'Cost'].replace(
                        "$", "").replace(",", ""))

                msrp = car_info[1]['price']
                insurance_cost = car_info[1]['Price:' + state] * 10

                total_cost_env = fuel_cost + env_cost + maintenance_cost + insurance_cost + msrp
                total_cost = fuel_cost + maintenance_cost + insurance_cost + msrp

                master_dict[car_name]['insurance'][state] = insurance_cost
                master_dict[car_name]['user_type'][mileage]['fuel_cost'][
                    state] = fuel_cost
                master_dict[car_name]['user_type'][mileage]['env_cost'][
                    state] = env_cost
                master_dict[car_name]['user_type'][mileage]['total_cost'][
                    'with_env'][state] = total_cost_env
                master_dict[car_name]['user_type'][mileage]['total_cost'][
                    'no_env'][state] = total_cost

    return master_dict


def get_best_vehicle(df, price_range, fuel_type):
    """
    recommend best vehicles base on price range and fuel type
    :param: df, price_range,fuel_type
    :type: DataFrame, list, str

    :return: DataFrame
    """
    temp_df = df[df['base'] <= price_range[1]][df['base'] >= price_range[0]][
        df['fuel_type'] == fuel_type]
    op_cost = list()
    for row in temp_df.iterrows():
        op_cost.append(row[1]['total'] - row[1]['base'])
    temp_df.insert(value=op_cost, column='op_cost', loc=0)
    return temp_df.sort_values(by='op_cost').nsmallest(10, columns='op_cost')
