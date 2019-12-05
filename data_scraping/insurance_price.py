import pandas as pd
import requests
from tqdm import tqdm

from data_analysis.cost_model import state_list


def scrape_insurance_data():
    """
    Scrapes insure.com for insurance prices and presents all
    relevant data.  Exports cleaned dataset as a csv.
    """

    for h in tqdm(range(1, 51)):
        url = (
               "https://www.insure.com/car-insurance/car-insurance-comparison" +
               "/results?make_id=all&model_name=all&car_type_id=all" +
               "&state_code_id={0}&state_code={1}&page={2}" +
               "&sortby=make&order=asc").format(h, state_list[h - 1], 1)
        html = requests.get(url).content
        df_temp = pd.read_html(html)
        df_list = df_temp[0]
        for i in range(1, 30):
            url = ("https://www.insure.com/car-insurance/" +
                   "car-insurance-comparison/results?make_id=all&" +
                   "model_name=all&car_type_id=all&state_code_id={0}" +
                   "&state_code={1}&page={2}&sortby=make&order=asc").format(
                h, state_list[h - 1], i + 1)
            html = requests.get(url).content
            try:
                df_temp = pd.read_html(html)
                frames = [df_list, df_temp[0]]
                df_list = pd.concat(frames)
            except ValueError:
                pass
        df_list = df_list.iloc[:, :6]
        df_list = df_list.drop(['Type', 'Style', 'Cylinders'], axis=1)
        df_list = df_list.reset_index(drop=True)
        for i in range(len(df_list['Premium'])):
            df_list['Premium'][i] = float(
                df_list['Premium'][i].strip('$').replace(',', ''))
        df_list['Premium'] = (pd.to_numeric(df_list['Premium']))
        df_list = df_list.groupby(['Make', 'Model']).mean()
        if h == 1:
            df_list.rename(
                columns={'Premium': 'Price:{}'.format(state_list[h - 1])},
                inplace=True)
            df_main = df_list
        else:
            df_main['Price:{}'.format(state_list[h - 1])] = df_list['Premium']
    df_main.to_csv('data/Insurance.csv')
