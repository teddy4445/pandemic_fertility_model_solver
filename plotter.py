# library imports
import numpy as np
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
