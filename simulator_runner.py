# library imports
import random
import time

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

    def run_simulation(self,
                       verbose: LoadingBar,
                       save_path: str = ""):
        population = Population()
        agents = [Agent(age_group='c', gender=random.choice(['m', 'f']), epi_state='S') for _ in range(self.population_size)]
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
        
        return average_history, std_dev_history
