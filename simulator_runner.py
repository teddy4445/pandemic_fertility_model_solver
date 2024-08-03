# library imports


# project imports
from agent import Agent
from population import Population
from simulator import Simulator


class SimulatorRunner:
    
    def __init__(self, population_size, initial_infected, days, alpha_ca, alpha_ae, alpha_ed, beta_s, beta_a, phi, gamma_a, gamma_s, lambda_prob, fertility_drop_prob, omega, xi):
        self.population_size = population_size
        self.initial_infected = initial_infected
        self.days = days
        self.alpha_ca = alpha_ca
        self.alpha_ae = alpha_ae
        self.alpha_ed = alpha_ed
        self.beta_s = beta_s
        self.beta_a = beta_a
        self.phi = phi
        self.gamma_a = gamma_a
        self.gamma_s = gamma_s
        self.lambda_prob = lambda_prob
        self.fertility_drop_prob = fertility_drop_prob

    def run_simulation(self, save_path = ""):
        population = Population()
        agents = [Agent(age_group='c', gender=random.choice(['m', 'f'])) for _ in range(size)]
        for agent in random.sample(self.agents, int(size * initial_infected)):
            agent.state = 'Ia'
        population.agents = agents
        simulation = Simulation(population, self.days, alpha_ca, alpha_ae, alpha_ed, self.beta_s, self.beta_a, self.phi, self.gamma_a, self.gamma_s, self.lambda_prob, self.fertility_drop_prob)
        simulation.run()
        if save_path != "":
            Plotter.plot_results(simulation, save_path)
            
        return simulation
    
    def run_multiple_simulations(self, n, save_path):
        all_histories = [self.run_simulation().history for i in range(n)]

        # Convert all_histories to numpy array for easier manipulation
        all_histories = np.array(all_histories)

        # Calculate average and std deviation across simulations
        average_history = np.mean(all_histories, axis=0)
        std_dev_history = np.std(all_histories, axis=0)
        if save_path != "":
            Plotter.plot_results(simulation, save_path)
        
        return average_history, std_dev_history