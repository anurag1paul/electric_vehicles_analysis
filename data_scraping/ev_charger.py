import requests
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import math

from data_analysis.cost_model import state_list


def import_data(nrel_data, eia_data):
    """
    import nrel and eia data from file
    :param: nrel_data, eia_data
    :type: str, str

    :return: DataFrame, DataFrame
    """
    # EV Charging Station Data
    df_nrel = pd.read_excel(nrel_data)
    # Electricity Cost Data
    df_eia = pd.read_excel(eia_data)

    return df_nrel, df_eia


def scraping_data(nrel_api_key, eia_api_key):
    """
    scrap data from nrel and eia website using given api keys
    :param: nrel_api_key, eia_api_key
    :type: str, str

    :return: none
    """
    URL = ("https://developer.nrel.gov/api/alt-fuel-stations/v1.json?" +
           "api_key={}").format(nrel_api_key)
    response = requests.get(url=URL)
    data_dict = response.json()
    df = pd.DataFrame(data_dict["fuel_stations"])
    df.to_excel("data/nrel_gov_data.xlsx")

    data_dict = dict()
    for state in state_list:
        URL = ("http://api.eia.gov/series/?" +
               "api_key={}&series_id=ELEC.PRICE.{}-ALL.M").format(
            eia_api_key, state)
        response = requests.get(url=URL)
        # print((state, response))
        data = response.json()['series'][0]['data']
        for entry in data:
            if entry[0] not in data_dict:
                data_dict[entry[0]] = dict()
            data_dict[entry[0]][state] = entry[1]
    df_eia = pd.DataFrame(data_dict)
    df_eia.to_excel("data/eia_gov.xlsx")


def prepare_data(df_nrel):
    """
    clean up ev charging station data
    :param: df_nrel
    :type: DataFrame

    :return: DataFrame
    """
    field_of_interest = ['fuel_type_code', 'city', 'state', 'zip', 'country',
                         'status_code', 'access_code', 'owner_type_code',
                         'ev_level1_evse_num', 'ev_level2_evse_num',
                         'ev_dc_fast_num', 'ev_connector_types', 'ev_network',
                         'ev_pricing', 'ev_renewable_source', 'geocode_status',
                         'latitude', 'longitude', 'open_date', 'facility_type']

    EV_stations = df_nrel[df_nrel['fuel_type_code'] == 'ELEC']
    EV_stations = EV_stations[field_of_interest]
    return EV_stations


def show_us_charging_facility(ev_stations):
    """
    show charging facility distribution on a US map
    :param: ev_stations
    :type: DataFrame

    :return: none
    """
    facility_dist_dict = dict()
    for facility in ev_stations['state']:
        if facility not in facility_dist_dict:
            facility_dist_dict[facility] = 1
        facility_dist_dict[facility] += 1
    df_dict = dict()
    df_dict['state'] = list(facility_dist_dict.keys())
    df_dict['count'] = list(facility_dist_dict.values())
    facility_dist_df = pd.DataFrame(df_dict)

    fig = go.Figure(data=go.Choropleth(
        locations=facility_dist_df['state'],  # Spatial coordinates
        z=facility_dist_df['count'].astype(float),  # Data to be color-coded
        locationmode='USA-states',
        # set of locations match entries in `locations`
        colorscale='Reds',
        colorbar_title="",
    ))

    fig.update_layout(
        title_text='EV Charging Facility',
        geo_scope='usa',  # limite map scope to USA
    )

    fig.show()


def show_us_charging_station(ev_stations):
    """
    show charging station distribution on a US map
    :param: ev_stations
    :type: DataFrame

    :return: none
    """
    facility_dist_dict = dict()
    for facility in ev_stations['state']:
        if facility not in facility_dist_dict:
            facility_dist_dict[facility] = 1
        facility_dist_dict[facility] += 1
    df_dict = dict()
    df_dict['state'] = list(facility_dist_dict.keys())
    df_dict['count'] = list(facility_dist_dict.values())
    facility_dist_df = pd.DataFrame(df_dict)

    station_dist_dict = dict()
    for station in ev_stations[
        ['state', 'ev_level1_evse_num', 'ev_level2_evse_num',
         'ev_dc_fast_num']].iterrows():
        if station[1]['state'] not in station_dist_dict:
            station_dist_dict[station[1]['state']] = 0
        if not math.isnan(station[1]['ev_level1_evse_num']):
            station_dist_dict[station[1]['state']] += station[1][
                'ev_level1_evse_num']
        if not math.isnan(station[1]['ev_level2_evse_num']):
            station_dist_dict[station[1]['state']] += station[1][
                'ev_level2_evse_num']
        if not math.isnan(station[1]['ev_dc_fast_num']):
            facility_dist_dict[station[1]['state']] += station[1][
                'ev_dc_fast_num']
    # print(station_dist_dict)
    df_dict = dict()
    df_dict['state'] = list(station_dist_dict.keys())
    df_dict['count'] = list(station_dist_dict.values())
    station_dist_df = pd.DataFrame(df_dict)

    fig = go.Figure(data=go.Choropleth(
        locations=station_dist_df['state'],  # Spatial coordinates
        z=station_dist_df['count'].astype(float),  # Data to be color-coded
        locationmode='USA-states',
        # set of locations match entries in `locations`
        colorscale='Reds',
        colorbar_title="Number of Charging Stations",
    ))

    fig.update_layout(
        title_text='EV Charging Stations',
        geo_scope='usa',  # limite map scope to USA
    )

    fig.show()


def show_us_station_per_site(ev_stations):
    """
    show charging station per facility distribution on a US map
    :param: EV_stations
    :type: DataFrame

    :return: none
    """
    facility_dist_dict = dict()
    for facility in ev_stations['state']:
        if facility not in facility_dist_dict:
            facility_dist_dict[facility] = 1
        facility_dist_dict[facility] += 1
    df_dict = dict()
    df_dict['state'] = list(facility_dist_dict.keys())
    df_dict['count'] = list(facility_dist_dict.values())
    facility_dist_df = pd.DataFrame(df_dict)

    station_dist_dict = dict()
    for station in ev_stations[
        ['state', 'ev_level1_evse_num', 'ev_level2_evse_num',
         'ev_dc_fast_num']].iterrows():
        if station[1]['state'] not in station_dist_dict:
            station_dist_dict[station[1]['state']] = 0
        if not math.isnan(station[1]['ev_level1_evse_num']):
            station_dist_dict[station[1]['state']] += station[1][
                'ev_level1_evse_num']
        if not math.isnan(station[1]['ev_level2_evse_num']):
            station_dist_dict[station[1]['state']] += station[1][
                'ev_level2_evse_num']
        if not math.isnan(station[1]['ev_dc_fast_num']):
            facility_dist_dict[station[1]['state']] += station[1][
                'ev_dc_fast_num']
    # print(station_dist_dict)
    df_dict = dict()
    df_dict['state'] = list(station_dist_dict.keys())
    df_dict['count'] = list(station_dist_dict.values())
    station_dist_df = pd.DataFrame(df_dict)

    avg_size_dist_dict = dict()
    for item in station_dist_dict.items():
        avg_size_dist_dict[item[0]] = item[1] / facility_dist_dict[item[0]]

    df_dict['state'] = list(avg_size_dist_dict.keys())
    df_dict['count'] = list(avg_size_dist_dict.values())
    avg_size_dist_df = pd.DataFrame(df_dict)

    fig = go.Figure(data=go.Choropleth(
        locations=avg_size_dist_df['state'],  # Spatial coordinates
        z=avg_size_dist_df['count'].astype(float),  # Data to be color-coded
        locationmode='USA-states',
        # set of locations match entries in `locations`
        colorscale='Reds',
        colorbar_title="Stations per Site",
    ))

    fig.update_layout(
        title_text='Average Charging Facility Size',
        geo_scope='usa',  # limite map scope to USA
    )

    fig.show()


def show_us_elec_cost(df_eia):
    """
    show electricity cost distribution on a US map
    :param: df_eia
    :type: DataFrame

    :return: none
    """
    fig = go.Figure(data=go.Choropleth(
        locations=df_eia['state'],  # Spatial coordinates
        z=df_eia['201908'].astype(float),  # Data to be color-coded
        locationmode='USA-states',
        # set of locations match entries in `locations`
        colorscale='Reds',
        colorbar_title="USD per kWh",
    ))

    fig.update_layout(
        title_text='Latest US Electricity Cost',
        geo_scope='usa',  # limit map scope to USA
    )

    fig.show()


def show_us_gas_cost(gas_data):
    """
    show gas cost distribution on a US map
    :param: gas_data
    :type: str

    :return: none
    """
    gas_price = pd.read_csv(gas_data)
    gas_price = gas_price.set_index('state_abbr')
    fig = go.Figure(data=go.Choropleth(
        locations=gas_price.index,  # Spatial coordinates
        z=gas_price['prices'].astype(float),  # Data to be color-coded
        locationmode='USA-states',
        # set of locations match entries in `locations`
        colorscale='Reds',
        colorbar_title="USD per gallon",
    ))

    fig.update_layout(
        title_text='Latest US Gasoline Prices',
        geo_scope='usa',  # limit map scope to USA
    )

    fig.show()


def show_us_elec_cost_all(df_eia):
    """
    show all year electricity cost distribution on a US map with slider
    :param df_eia: EV_stations
    :type df_eia: DataFrame

    :return: none
    """
    # Create figure
    fig = go.Figure()

    # Add traces, one for each slider step
    for step in list(df_eia.columns):
        fig.add_trace(
            go.Choropleth(
                locations=df_eia.index,  # Spatial coordinates
                z=df_eia[step].astype(float),  # Data to be color-coded
                locationmode='USA-states',
                # set of locations match entries in `locations`
                colorscale='Reds',
                colorbar_title="USD/kWh",
                name=step))

    # Make 10th trace visible
    fig.data[0].visible = True

    # Create and add slider
    steps = []
    for i in range(len(fig.data)):
        step = dict(
            method="restyle",
            args=["visible", [False] * len(fig.data)],
        )
        step["args"][1][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active=0,
        #     currentvalue={"201908"},
        pad={"t": 50},
        steps=steps
    )]

    fig.update_layout(
        sliders=sliders,
        title_text='2011-2019 Monthly Electricity Cost in the US',
        geo_scope='usa'  # limit map scope to USA
    )

    fig.show()
