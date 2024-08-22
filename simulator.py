# library imports

# project imports
from agent import Agent
from population import Population
from loading_bar import LoadingBar


class Simulation:

    def __init__(self, population, days, params):
        self.population = population
        self.days = days
        self.params = params
        
        # technical vars
        self.history = []

    def __repr__(self):
        return "<Simulator {}/{} ({:.2f}%}>".format(len(self.history),
                                                    self.days,
                                                    100*len(self.history)/self.days)

    def __str__(self):
        return "<Simulator {}/{} ({:.2f}%}>".format(len(self.history),
                                                    self.days,
                                                    100*len(self.history)/self.days)
        
    def run(self,
            verbose):
        if verbose:
            verbose.register(name="Sim", total=self.days)
        for day in range(self.days):
            self.run_step()
            if verbose:
                verbose.update("Sim", day)
                verbose.refresh()

    def run_step(self):
        self.population.update(params=self.params)
        self.population.infect(params=self.params)
        self.population.add_births(params=self.params)
        self.history.append(self.population.get_epi_dist())
