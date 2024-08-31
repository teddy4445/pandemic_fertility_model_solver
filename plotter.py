# library imports
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class Plotter:
    
    def __init__(self):
        pass
        
    @staticmethod
    def plot_results(history, save_path):
        days = range(len(history))

        states = ['S', 'E', 'I^a', 'I^s', 'R']
        for state_index in range(len(states)):
            plt.plot(days, history[:, state_index], label=f"${states[state_index]}$")

        plt.xlabel('Days', fontsize=16)
        plt.ylabel('Portion of the population', fontsize=16)
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path, dpi=400)
        plt.close()

    @staticmethod
    def plot_multi_result(average_history, std_dev_history, save_path):
        days = range(len(average_history))
        states = ['S', 'E', 'I^a', 'I^s', 'R']
        for state_index in range(len(states)):
            plt.plot(days, average_history[:, state_index], label=f"${states[state_index]}$")
            plt.fill_between(days, 
                             np.array(average_history[:, state_index]) - np.array(std_dev_history[:, state_index]),
                             np.array(average_history[:, state_index]) + np.array(std_dev_history[:, state_index]),
                             alpha=0.2)

        plt.xlabel('Days', fontsize=16)
        plt.ylabel('Portion of the population', fontsize=16)
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path, dpi=400)
        plt.close()

    @staticmethod
    def plot_fertility_rate_dynamics(time_data, tfr_data, cities, scenarios, save_path):
        fig, axs = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
        scenario_titles = ['No Pandemic', 'With Pandemic', 'Pandemic Without Immunity Decay']

        for i, scenario in enumerate(scenarios):
            for city in cities:
                axs[i].plot(time_data, tfr_data[scenario][city], label=city)
            axs[i].set_title(scenario_titles[i])
            axs[i].set_xlabel('Time (days)', fontsize=16)

        axs[0].set_ylabel('Total Fertility Rate (TFR)', fontsize=16)
        axs[0].legend()
        plt.tight_layout()
        plt.savefig(save_path, dpi=400)
        plt.close()

    @staticmethod
    def plot_infection_vs_fertility_heatmap(infection_rates, fertility_reduction, average_tfr_reduction, save_path):
        plt.figure(figsize=(10, 8))
        sns.heatmap(average_tfr_reduction, xticklabels=infection_rates, yticklabels=fertility_reduction, cmap="YlGnBu")
        plt.xlabel('Infection Rate ($\\beta$)', fontsize=16)
        plt.ylabel('Fertility Reduction ($\\xi$)', fontsize=16)
        plt.tight_layout()
        plt.savefig(save_path, dpi=400)
        plt.close()

    @staticmethod
    def create_sensitivity_analysis_table(sensitivity_data, save_path):
        df = pd.DataFrame(sensitivity_data, columns=['Parameter Name', 'Value Range', 'Impact on TFR', 'Impact on Population Size'])
        df.to_csv(save_path, index=False)
        print(df.to_markdown(index=False))

    @staticmethod
    def plot_3d_scatter(kinds_want_rate, fertility_reduce_ability, tfr, save_path):
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(kinds_want_rate, fertility_reduce_ability, tfr, c='blue', marker='o', alpha=0.25)
        ax.set_xlabel('Kinds Want Rate ($\\omega$)', fontsize=16)
        ax.set_ylabel('Fertility Reduce Ability ($\\xi$)', fontsize=16)
        ax.set_zlabel('Total Fertility Rate (TFR)', fontsize=16)

        plt.tight_layout()
        plt.savefig(save_path, dpi=400)
        plt.close()
