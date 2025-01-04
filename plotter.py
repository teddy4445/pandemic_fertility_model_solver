# library imports
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

colors = ["#006400", "#00008b", "#b03060", "#ff0000", "#ffff00", "#deb887", "#00ff00", "#00ffff", "#ff00ff", "#6495ed"]

class Plotter:
    
    def __init__(self):
        pass
        
    @staticmethod
    def fig2(histories, save_paths):
        h_index = 0
        for history in histories:
            index = 0
            for city_name, b_vals in history.items():
                days = range(len(b_vals[0]))

                signals_array = np.array(b_vals)
                average_signal = -1*np.mean(signals_array, axis=0)
                std_signal = np.std(signals_array, axis=0)/10

                plt.plot(days, average_signal, color=colors[index], label=f"{city_name}")
                plt.fill_between(days, average_signal - std_signal, average_signal + std_signal, color=colors[index], alpha=0.25)
                index += 1

            plt.xlabel('Time in days [t]', fontsize=16)
            plt.ylabel('Average fertility decline (B) [1]', fontsize=16)
            plt.xticks([365 * i for i in range(11)])
            plt.legend()
            plt.gca().spines[['right', 'top']].set_visible(False)
            plt.grid(alpha=0.25, color="black")
            plt.tight_layout()
            plt.savefig(save_paths[h_index], dpi=400)
            plt.close()
            h_index += 1

    @staticmethod
    def fig3(means, stds, x_label, y_label, save_path):

        plt.plot(range(len(means)), means, "-", color="black")
        plt.fill_between(range(len(means)), np.array(means) - np.array(stds)/10, np.array(means) + np.array(stds)/10, color="black",
                         alpha=0.5)

        plt.xlabel(x_label, fontsize=16)
        plt.ylabel(y_label, fontsize=16)
        plt.legend()
        plt.gca().spines[['right', 'top']].set_visible(False)
        plt.grid(alpha=0.25, color="black")
        plt.tight_layout()
        plt.savefig(save_path, dpi=400)
        plt.close()

    @staticmethod
    def fig4(values, x_ticks, y_ticks, x_label, y_label, save_path):
        plt.figure(figsize=(10, 8))
        sns.heatmap(values, xticklabels=x_ticks, yticklabels=y_ticks, cmap="YlGnBu")
        plt.xlabel(x_label, fontsize=16)
        plt.ylabel(y_label, fontsize=16)
        plt.tight_layout()
        plt.savefig(save_path, dpi=400)
        plt.close()

    @staticmethod
    def fig5(x_vals, y_vals, z_vals, save_path):
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x_vals, y_vals, z_vals, color='black', alpha=0.5)
        ax.set_xlabel(x_label, fontsize=16)
        ax.set_ylabel(y_label, fontsize=16)
        ax.set_zlabel(z_label, fontsize=16)
        plt.tight_layout()
        plt.savefig(save_path, dpi=400)
        plt.close()
