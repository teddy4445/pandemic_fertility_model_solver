# library imports
import matplotlib.pyplot as plt

class Plotter:
    
    def __init__(self):
        pass
        
    @staticmethod
    def plot_results(simulation, save_path):
        days = range(simulation.days)
        history = self.simulation.history

        states = ['S', 'E', 'I^a', 'I^s', 'R', 'D']
        for state in states:
            counts = [day_counts[state] for day_counts in history]
            plt.plot(days, counts, label=f"${state}$")

        plt.xlabel('Days', fontsize=16)
        plt.ylabel('Portion of the population', fontsize=16)
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path, dpi=400)
        plt.close()

    @staticmethod
    def plot_multi_result(average_history, std_dev_history, save_path):
        days = range(simulation.days)
        history = self.simulation.history

        # Plot average results
        days = range(self.days)
        states = ['S', 'E', 'I^a', 'I^s', 'R']
        for state in states:
            avg_counts = [day_counts[state] for day_counts in average_history]
            plt.plot(days, avg_counts, label=f"Average {state}")
            
            std_dev_counts = [day_counts[state] for day_counts in std_dev_history]
            plt.fill_between(days, 
                             np.array(avg_counts) - np.array(std_dev_counts), 
                             np.array(avg_counts) + np.array(std_dev_counts), 
                             alpha=0.2)

        plt.xlabel('Days', fontsize=16)
        plt.ylabel('Portion of the population', fontsize=16)
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path, dpi=400)
        plt.close()