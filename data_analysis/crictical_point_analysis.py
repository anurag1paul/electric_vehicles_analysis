import numpy as np
from matplotlib import pyplot as plt

from data_analysis.cost_model import state_list
from data_analysis.df_gen import get_df
from data_scraping.gas_prices import get_state_dict

data = np.load("master_dict.npy", allow_pickle=True).item()


def find_critical_points():
    """
    Finds critical point for each state.
    Critical Point is the point at which the average cost of gas
    vehicles equals the average cost of electric vehicles at a specific number
    of miles driver per year.
    :return: mileage, total_cost and states
    """
    mileage = []
    total_cost = []
    states = []

    for state in state_list:
        avg_6 = get_df(user_id=60000, state=state).set_index(["name", "fuel_type"])
        avg_6["yearly"] = avg_6["total"] - avg_6["base"]

        avg_18 = get_df(user_id=180000, state=state).set_index(["name", "fuel_type"])
        avg_18["yearly"] = avg_18["total"] - avg_18["base"]

        delta = (avg_18 - avg_6) / 12000

        avg_1 = avg_6 - (5000 * delta)

        avg_1 = avg_1.reset_index()
        avg1_gas = avg_1[avg_1["fuel_type"]=="g"].nsmallest(45, "yearly")
        avg1_electric = avg_1[avg_1["fuel_type"]=="e"].nsmallest(7, "yearly")

        delta = delta.reset_index()

        delta_gas = delta[delta["name"].isin(avg1_gas["name"])]
        delta_electric = delta[delta["name"].isin(avg1_electric["name"])]

        avg1_g_mean = float(avg1_gas.groupby("fuel_type").mean()["total"])
        avg1_e_mean = float(avg1_electric.groupby("fuel_type").mean()["total"])
        delta_g_mean = float(delta_gas.groupby("fuel_type").mean()["total"])
        delta_e_mean = float(delta_electric.groupby("fuel_type").mean()["total"])

        x = (avg1_g_mean - avg1_e_mean) / (delta_e_mean - delta_g_mean)
        cost = avg1_g_mean + x * delta_g_mean
        mileage.append(x)
        total_cost.append(cost)
        states.append(state)

    return mileage, total_cost, states


def plot_critical_points():
    """
    Plots a scatter plot of critical point (miles per yr, total cost) for each
    state of USA. Critical Point is the point at which the average cost of gas
    vehicles equals the average cost of electric vehicles at a specific number
    of miles driver per year.
    :return: None
    """

    states_dict = {val["STUSAB"]: key for key, val in get_state_dict().items()}
    mileage, total_cost, states = find_critical_points()

    fig, ax = plt.subplots(figsize=(10,8), dpi=200)
    ax.scatter(mileage, total_cost)
    st = {txt : (mileage[i]+200, total_cost[i]+200)
          for i, txt in enumerate(states)}
    sel = ["HI", "ME", "MD", "MN", "CA", "GA", "KS", "WY", "WV", "ND"]
    for key in sel:
        ax.annotate(states_dict[key], st[key], fontsize=11)
        # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlim(8000, 45000)
    ax.set_xlabel("Miles/Year", fontsize=14)
    ax.set_ylabel("Total Cost($)", fontsize=14)

    plt.show()

