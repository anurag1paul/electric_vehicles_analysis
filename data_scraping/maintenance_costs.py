import os

import pandas as pd


def scrape_maintenance_costs_brand(folder=None):
    """
    Scrape yourmechanic.com to get maintenance_cost
    for 10 years for different brands
    Dumps to folder if specified
    :param folder: optional
    :type folder: string
    :return: pandas data-frame
    """
    your_mechanic = """https://www.yourmechanic.com/article/
    the-most-and-least-expensive-cars-to-maintain-by-maddy-martin"""

    cost = pd.read_html(your_mechanic)

    brands = cost[0].drop(0)
    brands.columns = brands.iloc[0]
    brands = brands.drop(1)

    if folder is not None:
        assert isinstance(folder, str) and os.path.exists(folder)
        brands.to_csv(os.path.join(folder, "brands_maintenance.csv"))

    return brands
