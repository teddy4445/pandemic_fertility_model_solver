# library imports


# project imports
from agent import Agent
from population import Population


class Simulation:

    def __init__(self, population, days, alpha_ca, alpha_ae, alpha_ed, beta_s, beta_a, phi, gamma_a, gamma_s, lambda_prob, fertility_drop_prob, omega, xi):
        # simulation info
        self.population = population
        self.days = days

        # model params
        self.alpha_ca = alpha_ca
        self.alpha_ae = alpha_ae
        self.alpha_ed = alpha_ed
        self.beta_s = beta_s
        self.beta_a = beta_a
        self.phi = phi
        self.gamma_a = gamma_a
        self.gamma_s = gamma_s
        self.omega = omega
        self.xi = xi
        self.lambda_prob = lambda_prob
        self.fertility_drop_prob = fertility_drop_prob
        
        # technical vars
        self.history = []
        
    def run():
        for i in range(self.days):
            self.run_step()

    def run_step(self):
        for _ in range(self.days):
            infections = self.population.calculate_infections() # for each epidemiolgical group (i.e., age and gender and state=="S") how many should be infected 
            # TODO: go over these groups and update random subset of the right size such that their state is E 
            self.population.update(self.alpha_ca, self.alpha_ae, self.alpha_ed, self.phi, self.gamma_a, self.gamma_s, self.lambda_prob, self.fertility_drop_prob, self.fertility_drop_rate)
            self.population.add_births(self.omega, self.xi)
            self.history.append(self.population.get_epi_dist())
