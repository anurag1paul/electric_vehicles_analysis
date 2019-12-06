import numpy as np

from data_analysis.cost_model import import_all_data, build_model_data_dict
from data_scraping import insurance_matching

if __name__ == "__main__":

    name_map = insurance_matching.create_manual_checklist()
    insurance_msrp_data = insurance_matching.read_manual_checklist(
        'data/processed_manual_checklist.csv', name_map)
    insurance_msrp_data.to_csv('data/insurance_msrp_data.csv')

    # Model Elements
    # - Assuming a lifespan of 10 years: Insurance cost, Maintenance Cost
    # - Light user (6k miles/year), Medium user (12k miles/year),
    #   heavy user (18k miles/year): Gasoline cost, Electricty Cost
    # - Market Price
    # - Environmental Cost
    # - Overall cost calculation will be based on each car,
    #   each state, w/(o) env, user type (insurance_msrp,
    #   electricity_data, gas_price, co2_mwh,

    (insurance_msrp, electricity_data, gas_price, co2_mwh,
            maintenance_data, fuel_economy_data) = import_all_data()
    master_dict = build_model_data_dict(insurance_msrp, electricity_data, gas_price,
                                  co2_mwh, maintenance_data, fuel_economy_data)

    np.save('data/master_dict.npy', master_dict)
