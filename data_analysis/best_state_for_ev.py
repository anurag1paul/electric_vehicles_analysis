import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from data_analysis.cost_model import state_list
from data_analysis.df_gen import get_df
from data_scraping.gas_prices import get_state_dict


def get_states_ranking():
    """
    Ranks the states by the average total cost of the
    cheapest 5 electric cars in that state
    :return: dataframe of states
    """
    cheapest = None
    for state in state_list:
        df = get_df(state=state)
        df["state"] = state
        df = df[df["fuel_type"] == "e"]
        c = df.nsmallest(5, "total").groupby("state").mean()

        if cheapest is None:
            cheapest = c
        else:
            cheapest = pd.concat((cheapest, c))

    return cheapest


def plot_topk_states(k=5):
    """
    Plot the best and the worst k states for owning an electric vehicle
    :param k: number of states
    :return: None
    """
    assert isinstance(k, int) and 0 < k <= 25

    cheapest = get_states_ranking()
    res = pd.concat((cheapest.nsmallest(k, "total"),
                     cheapest.nlargest(k, "total")))
    res = res.reset_index()
    topk = res.sort_values("total")[["state", "base", "fuel", "maintenance",
                                     "insurance", "total"]]

    fig, ax = plt.subplots(figsize=(10, 7), dpi=200)

    states_dict = {val["STUSAB"]: key for key, val in get_state_dict().items()}

    # Example data
    states = [states_dict[s] for s in topk["state"]]
    n = len(states)
    x_pos = np.arange(n)

    buffer = np.zeros(n)

    for col in topk.columns[1:-1]:
        if col != "env":
            l = col.title()
        else:
            l = "Environment"

        ax.bar(x_pos, list(topk[col]), align='center', bottom = buffer, label=l)
        buffer += np.array(topk[col])

    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.set_xticks(x_pos)
    ax.set_xticklabels(states, fontsize=12)
    ax.set_yticks(np.arange(0, 140000, 20000))
    ax.set_ylabel('Total Cost ($)', fontsize=14)
    ax.legend(fontsize=14)
    plt.xticks(rotation=30)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(12)

    plt.show()
