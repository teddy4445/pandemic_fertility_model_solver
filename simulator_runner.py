# library imports
import time
import random

import numpy as np

# project imports
from agent import Agent
from plotter import Plotter
from simulator import Simulation
from population import Population
from loading_bar import LoadingBar


class SimulatorRunner:
    
    def __init__(self, population_size, initial_infected, days, params):
        self.population_size = population_size
        self.initial_infected = initial_infected
        self.days = days
        self.params = params

    def __repr__(self):
        return "<SimulatorRunner>"

    def __str__(self):
        return "<SimulatorRunner>"

    def paper_run(self,
                  verbose: LoadingBar):
        """
        A single function to run all the logic needed to produce all the results for the paper
        :return:
        """
        self._generate_fertility_rate_dynamics_data(verbose=verbose,
                                                    save_path="fertility_rate_dynamics.pdf")
        self._generate_infection_vs_fertility_data(verbose=verbose,
                                                   save_path="infection_vs_fertility.pdf")
        self._generate_sensitivity_analysis_data(verbose=verbose,
                                                 save_path="sensitivity_analysis.pdf")
        self._generate_3d_scatter_data(verbose=verbose,
                                       save_path="3d_scatter.pdf")

    def _generate_fertility_rate_dynamics_data(self, verbose, save_path):
        # TODO: Ariel, make sure the values make sense and run the relevent simulaiton
        # Example code to generate or retrieve data
        time_data = range(0, 365)  # Simulate 365 days
        cities = ['CityA', 'CityB', 'CityC']
        scenarios = ['no_pandemic', 'with_pandemic', 'pandemic_no_immunity_decay']

        # Simulated TFR data for each scenario and city
        tfr_data = {
            'no_pandemic': {
                'CityA': [2.5 + i * 0.01 for i in time_data],
                'CityB': [2.4 + i * 0.01 for i in time_data],
                'CityC': [2.6 + i * 0.01 for i in time_data],
            },
            'with_pandemic': {
                'CityA': [2.5 - i * 0.02 for i in time_data],
                'CityB': [2.4 - i * 0.02 for i in time_data],
                'CityC': [2.6 - i * 0.02 for i in time_data],
            },
            'pandemic_no_immunity_decay': {
                'CityA': [2.5 - i * 0.015 for i in time_data],
                'CityB': [2.4 - i * 0.015 for i in time_data],
                'CityC': [2.6 - i * 0.015 for i in time_data],
            },
        }

        # Plot the fertility rate dynamics
        Plotter.plot_fertility_rate_dynamics(time_data, tfr_data, cities, scenarios, save_path)


    def _generate_infection_vs_fertility_data(self, verbose, save_path):
        # TODO: Ariel, make sure the values make sense and run the relevent simulaiton
        # Example code to generate or retrieve data
        infection_rates = [0.1 * i for i in range(1, 11)]  # Infection rate from 0.1 to 1.0
        fertility_reduction = [0.1 * i for i in range(1, 11)]  # Fertility reduction from 0.1 to 1.0
        average_tfr_reduction = np.random.rand(10, 10)  # Randomly generated for illustration

        # Plot the heatmap
        Plotter.plot_infection_vs_fertility_heatmap(infection_rates, fertility_reduction, average_tfr_reduction, save_path)

    def _generate_sensitivity_analysis_data(self, verbose, save_path):
        # TODO: Ariel, make sure the values make sense and run the relevent simulaiton
        # Example code to generate or retrieve data
        sensitivity_data = [
            {'Parameter Name': '\\beta', 'Value Range': '0.5 - 1.5', 'Impact on TFR': 'High',
             'Impact on Population Size': 'Moderate'},
            {'Parameter Name': '\\xi', 'Value Range': '0.5 - 1.5', 'Impact on TFR': 'Moderate',
             'Impact on Population Size': 'Low'},
            # More rows...
        ]

        # Create the sensitivity analysis table
        Plotter.create_sensitivity_analysis_table(sensitivity_data, save_path)

    def _generate_3d_scatter_data(self, verbose, save_path):
        # TODO: Ariel, make sure the values make sense and run the relevent simulaiton
        # Example code to generate or retrieve data
        kinds_want_rate = [0.1 * i for i in range(1, 21)]  # Simulated range for ω
        fertility_reduce_ability = [0.1 * i for i in range(1, 21)]  # Simulated range for ξ
        tfr = [1.5 + 0.1 * i for i in range(1, 21)]  # Simulated TFR values

        # Plot the 3D scatter plot
        Plotter.plot_3d_scatter(kinds_want_rate, fertility_reduce_ability, tfr, save_path)

    def run_simulation(self,
                       verbose: LoadingBar,
                       save_path: str = ""):
        population = Population()
        agents = [Agent(age_group='c', gender=random.choice(['m', 'f']), epi_state='S') for _ in
                  range(self.population_size)]
        for agent in random.sample(agents, int(self.population_size * self.initial_infected)):
            agent.state = 'Ia'
        population.agents = agents
        simulation = Simulation(population,
                                self.days,
                                self.params)
        simulation.run(verbose=verbose)
        if save_path != "":
            Plotter.plot_results(simulation.history, save_path)

        return simulation

    def run_multiple_simulations(self,
                                 n: int,
                                 save_path: str,
                                 verbose: LoadingBar):
        all_histories = []
        verbose.register(name="Global", total=n)
        for sim_index in range(n):
            if verbose:
                verbose.update(name="Global", iteration=sim_index)
                verbose.refresh()
            all_histories.append(self.run_simulation(verbose=verbose).history)
        verbose.update(name="Global", iteration=n)

        # Convert all_histories to numpy array for easier manipulation
        all_histories = np.array(all_histories)

        # Calculate average and std deviation across simulations
        average_history = np.mean(all_histories, axis=0)
        std_dev_history = np.std(all_histories, axis=0)

        # save results in plot
        if save_path != "":
            Plotter.plot_multi_result(average_history, std_dev_history, save_path)

        return all_histories
