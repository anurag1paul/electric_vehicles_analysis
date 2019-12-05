import numpy as np
import pandas as pd

from data_analysis.cost_model import state_list


def get_df(user_id=12000, state="all"):
    """
    Generates a dataframe using the processed cost model pickle
    :param user_id: miles driver per year
    :param state: all or a specific US state abbreviation
    :return: dataframe
    """
    assert isinstance(user_id, int) and user_id in {6000, 12000, 18000}
    assert isinstance(state, str) and (state == "all" or state in state_list)

    user_id *= 10

    data = np.load("data/master_dict.npy", allow_pickle=True).item()

    car_name = []
    base = []
    maintenance = []
    fuel_type = []
    fuel_cost = []
    env = []
    insurance = []

    for key in data:
        car_name.append(key)
        c_dict = data[key]
        base.append(c_dict["base"])
        maintenance.append(c_dict["maintenance"])
        fuel_type.append(c_dict["fuel_type"])
        user = c_dict["user_type"][user_id]
        if state == "all":
            if c_dict["fuel_type"] == "e":
                env_cost = 0
            else:
                env_cost = np.mean(list(user["env_cost"].values()))
            env.append(env_cost)
            insurance.append(np.mean(list(c_dict['insurance'].values())))
            fuel_cost.append(np.mean(list(user["fuel_cost"].values())))
        else:
            if c_dict["fuel_type"] == "e":
                env_cost = 0
            else:
                env_cost = np.mean(list(user["env_cost"].values()))
            env.append(env_cost)
            insurance.append(c_dict['insurance'][state])
            fuel_cost.append(user["fuel_cost"][state])

    df = pd.DataFrame({"name": car_name,
                       "fuel_type": fuel_type,
                       "base": base,
                       "fuel": fuel_cost,
                       "maintenance": maintenance,
                       "insurance": insurance,
                       "env": env})

    df["total"] = (df["base"] + df["fuel"] + df["maintenance"] +
                   df["insurance"] + df["env"])
    return df

