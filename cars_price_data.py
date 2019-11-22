import os

from lxml import html
import requests
import pandas as pd
from tqdm import tqdm


def parse_cars_dot_com(n_pages, folder):
    """
    Function to parse cars.com and extract price,
    fuel type, city and highway MPG for all cars
    :param n_pages:number of pages
    :type n_pages: int
    :param folder: folder in which to save all pages
    :return: None
    """
    assert isinstance(n_pages, int) and n_pages > 0
    assert isinstance(folder, str) and os.path.exists(folder)

    base_link = """https://www.cars.com/for-sale/searchresults.action/?
                page={}&perPage=100&rd=99999&searchSource=GN_REFINEMENT&
                sort=relevance&stkTypId=28880"""

    for i in tqdm(range(1, n_pages)):
        link = base_link.format(i)
        page = requests.get(link)
        tree = html.fromstring(page.content)

        payment = tree.xpath('//div[@class="payment-section"]')
        prices = [each.getchildren()[0].text.strip() for each in payment]
        car_names = [s.strip() for s in
                     tree.xpath('//h2[@class="listing-row__title"]/text()')]
        links = tree.xpath('//a[@class="shop-srp-listings__listing"]/@href')

        city_mpg = []
        highway_mpg = []
        fuels = []

        # use the embedded link in search page to extract mpg
        # and fuel type values

        for sub_link in links:
            c_mpg, h_mpg, fuel = parse_car_details(sub_link)
            city_mpg.append(c_mpg)
            highway_mpg.append(h_mpg)
            fuels.append(fuel)

        df = pd.DataFrame({"name": car_names,
                           "price": prices,
                           "city_mpg": city_mpg,
                           "highway_mpg": highway_mpg,
                           "fuel_type": fuels})

        df.to_csv("{}/page{}.csv".format(folder, i), index=False)


def parse_car_details(link):
    """
    Extract car specific details from the cars.com page
    :param link: partial value contained in search page
    :return: city mpg, highway mpg and fuel type
    """
    assert link and isinstance(link, str)

    full_link = "http://cars.com{}".format(link)
    sub_page = requests.get(full_link)
    subtree = html.fromstring(sub_page.content)
    text_vals = [s.strip() for s in subtree.xpath(
                     """//li[@class="vdp-details-basics__item"]
                     /strong/text()""")]
    values = [s.strip()
              for s in subtree.xpath("""//li[@class=
              "vdp-details-basics__item"]/span/text()""")]
    c_mpg = h_mpg = 0
    fuel = ""

    for t, v in zip(text_vals, values):
        if t == "City MPG:":
            c_mpg = int(v)
        if t == "Highway MPG:":
            h_mpg = int(v)
        if t == "Fuel Type:":
            fuel = v

    return c_mpg, h_mpg, fuel


def read_clean_cars_data(folder, num_pages):
    """
    Read the directory containing cars.com dump and clean and format
    to create a pandas data frame
    :param folder: which contains all the pages scraped
    :param num_pages: number of pages to be loaded
    :return: data frame
    """
    assert isinstance(folder, str) and os.path.exists(folder)
    assert isinstance(num_pages, int) and num_pages > 0

    tdf = pd.read_csv("{}/page1.csv".format(folder))
    for i in range(2, num_pages):
        tdf = pd.concat((tdf, pd.read_csv("{}/page{}.csv".format(folder, i))))

    tdf2 = tdf.dropna()
    tdf2 = tdf2[tdf2["price"] != "Not Priced"]
    tdf2["price"] = tdf2["price"].apply(lambda x : int(x[1:].replace(",", "")))

    tdf3 = tdf2.groupby(["name", "fuel_type"]).mean()
    tdf3 = tdf3.reset_index()

    return tdf3

