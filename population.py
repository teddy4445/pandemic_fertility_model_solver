# library imports
import numpy as np
import concurrent.futures
from collections import Counter

# project imports
from agent import Agent


class Population:
    def __init__(self):
        self.agents = []
            
    def add(self, agent):
        if isinstance(agent, Agent):
            self.agents.append(agent)

    def update(self, alpha_ca, alpha_ae, alpha_ed, phi, gamma_a, gamma_s, lambda_prob, fertility_drop_prob, fertility_drop_rate):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Map the update function to each agent
            futures = [executor.submit(agent.update, alpha_ca, alpha_ae, alpha_ed, phi, gamma_a, gamma_s, lambda_prob, fertility_drop_prob, fertility_drop_rate) for agent in self.agents]
            # Wait for all futures to complete
            concurrent.futures.wait(futures)
        self.agents = [agent for agent in self.agents who agent.state != 'D']

    def get_epi_dist(self):
        states = [agent.state for agent in self.agents]
        counts = Counter(states)
        return {'S': counts.get('S', 0), 'E': counts.get('E', 0), 'Ia': counts.get('Ia', 0), 'Is': counts.get('Is', 0), 'R': counts.get('R', 0)}


    def add_births(self, omega, xi):
        count = self._calculate_births(omega, xi)
        for _ in range(count):
            self.population.agents.append(Agent(age_group='c', gender=random.choice(['m', 'f']))) # TODO: male and female 50-50 percent, is it right?
        

    def _calculate_births(self, omega, xi):
        Sa_female = sum(1 for agent in self.agents if agent.state == 'S' and agent.age_group == 'a' and agent.gender == 'f')
        Sa_male = sum(1 for agent in self.agents if agent.state == 'S' and agent.age_group == 'a' and agent.gender == 'm')
        Ra_female = sum(1 for agent in self.agents if agent.state == 'R' and agent.age_group == 'a' and agent.gender == 'f')
        Ra_male = sum(1 for agent in self.agents if agent.state == 'R' and agent.age_group == 'a' and agent.gender == 'm')
        
        births = omega * (min(Sa_female, Sa_male) + xi * min(Ra_female, Ra_male))
        return int(np.floor(births))
        
    def _calculate_infections(self):
        pass # TODO: ARIEL - this is for you 
