import os
from datetime import date

import pandas as pd
import requests
from lxml import html


def get_state_dict():
    """
    Generate mapping of state name to state abbreviations
    :return: dictionary
    """
    state_dict = pd.read_csv(
                       "https://www2.census.gov/geo/docs/reference/state.txt",
                       sep='|',
                       dtype='S')
    state_dict = state_dict.set_index('STATE_NAME').to_dict('index')
    state_dict['Washington DC'] = state_dict['District of Columbia']
    return state_dict


def gas_prices_states(folder=None):
    """
    Scrapes gasbuddy.com to get gas prices for every state in USA
    :param folder: optional, dump in the folder if specified
    :type folder: string
    :return: data frame
    """
    gas_buddy = "https://www.gasbuddy.com/USA"
    page = requests.get(gas_buddy)
    tree = html.fromstring(page.content)
    states = [s.strip()
              for s in
              tree.xpath('//div[@class="col-sm-6 col-xs-6 siteName"]/text()')]
    prices = [s.strip()
              for s in
              tree.xpath('//div[@class="col-sm-2 col-xs-3 text-right"]/text()')]
    gas = pd.DataFrame({"states": states, "prices": prices})
    state_dict = get_state_dict()
    gas["state_abbr"] = [state_dict[x]["STUSAB"] for x in gas["states"]]

    if folder is not None:
        assert isinstance(folder, str) and os.path.exists(folder)
        gas.to_csv(os.path.join(folder,
                                "gas_states_{}.csv".format(date.today())))

    return gas


def gas_prices_cities(folder=None):
    """
    Scrapes gasbuddy.com to get gas prices for few cities of every state in USA
    :param folder: optional, dump in the folder if specified
    :type folder: string
    :return: data frame
    """
    state_abbr = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL',
                  'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA',
                  'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE',
                  'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
                  'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT',
                  'VA', 'WA', 'WV', 'WI', 'WY']

    gas_url = "https://www.gasbuddy.com/USA/{}"
    states = []
    cities = []
    prices = []
    for short_name in state_abbr:

        page = requests.get(gas_url.format(short_name))
        tree = html.fromstring(page.content)

        temp = [s.strip()
                for s in
                tree.xpath('//div[@class="col-sm-6 col-xs-6 siteName"]/text()')]
        cities.extend(temp)

        prices.extend([s.strip()
                       for s in
                       tree.xpath("""//div
                       [@class="col-sm-2 col-xs-3 text-right"]/text()""")])

        states.extend([short_name for i in temp])

    gas_cities = pd.DataFrame({"City": cities,
                               "State": states,
                               "Price": prices})

    if folder is not None:
        assert isinstance(folder, str) and os.path.exists(folder)
        gas_cities.to_csv(
            os.path.join(folder, "gas_cities_{}.csv".format(date.today())))

    return gas_cities

