import os

from data_scraping import *

data_folder = "data/"
nrel_api_key = ""
eia_api_key = ""

if __name__ == "__main__":
    # scrape car_sales data
    scrape_sales_data()
    print("Sales data Scraped!")

    # car prices
    prices_folder = "data/cars_dot_com"
    if not os.path.exists(prices_folder):
        os.makedirs(prices_folder)

    parse_cars_dot_com(50, prices_folder)
    car_prices = read_clean_cars_data(prices_folder, 50)
    car_prices.to_csv("data/cars_cleaned_grouped.csv")
    print("Car Prices Data Scraped!")

    # insurance
    scrape_insurance_data()
    print("Insurance Data Scraped!")

    # maintenance
    scrape_maintenance_costs_brand(data_folder)
    print("Maintenance Costs Data Scraped!")

    # gas prices
    gas_prices_states(data_folder)
    print("Gas Prices Scraped!")

    # electricity prices and ev charging stations data
    if nrel_api_key and eia_api_key:
        scrape_ev_data(nrel_api_key, eia_api_key)
        print("Electricity Data Scraped!")
    else:
        print("ERROR: Please provide api keys to download electricity prices")

    # generate manual checklist
    create_manual_checklist()
    print("Manual Checklist Created")
