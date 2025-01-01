# library imports
import random
import numpy as np
import concurrent.futures
from collections import Counter

# project imports
from agent import Agent


class Population:
    def __init__(self):
        self.agents = []

    def __repr__(self):
        return "<Population: {}>".format(len(self.agents))

    def __str__(self):
        return "<Population: {} | {}>".format(len(self.agents), self.get_epi_dist())
            
    def add(self, agent):
        if isinstance(agent, Agent):
            self.agents.append(agent)

    def update(self, params):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Map the update function to each agent
            futures = [executor.submit(agent.update, params) for agent in self.agents]
            # Wait for all futures to complete
            concurrent.futures.wait(futures)
        self.agents = [agent for agent in self.agents if agent.state != 'D']

    def get_epi_dist(self):
        states = [agent.state for agent in self.agents]
        counts = Counter(states)
        return [counts.get('S', 0), counts.get('E', 0), counts.get('Ia', 0), counts.get('Is', 0), counts.get('R', 0)]

    def _get_agent_dist(self):
        states = [agent.get_desp() for agent in self.agents]
        counts = Counter(states)
        answer = {}
        for gender in ["m", "f"]:
            for age in ["c", "a", "e"]:
                for fortility in ["n", "f"]:
                    for epi in ["S", "E", "Is", "Ia", "R"]:
                        key = f"{gender}-{age}-{epi}-{fortility}"
                        answer[key] = counts.get(key, 0)
        return answer

    def add_births(self,
                   params: dict):
        count = self._calculate_births(params=params)
        for _ in range(count):
            self.agents.append(Agent(age_group='c', gender=random.choice(['m', 'f']), epi_state="S")) # TODO: male and female 50-50 percent, is it right?

    def _calculate_births(self,
                          params: dict):
        f = []
        m = []
        for agent in self.agents:
            if agent.age_group != "a":
                continue
            if agent.gender == "f":
                f.append(agent)
            else:
                m.append(agent)

        total_rate = 0

        min_count = min([len(f), len(m)])
        for i in range(min_count):
            random_index = random.randint(0, len(m) - 1)
            m_fertility = m.pop(random_index).fertility
            random_index = random.randint(0, len(f) - 1)
            f_fertility = f.pop(random_index).fertility
            if m_fertility == "n":
                if f_fertility == "f":
                    total_rate += params["xi"]
                else:
                    total_rate += 1
            else:
                if f_fertility == "f":
                    total_rate += params["xi"]*params["xi"]
                else:
                    total_rate += params["xi"]

        births = params["omega"] * total_rate
        return int(np.floor(births))

    def infect(self, params: dict):
        agents_dist = self._get_agent_dist()

        infected_group = {}

        # for each epi_state=S group, find out how many infected
        for gender in ["m", "f"]:
            for age in ["c", "a", "e"]:
                for fortility in ["n", "f"]:
                    key = f"{gender}-{age}-S-{fortility}"
                    s_count = agents_dist[key]

                    if s_count == 0:
                        continue

                    infected_val = 0

                    for gender_i in ["m", "f"]:
                        for age_i in ["c", "a", "e"]:
                            for fortility_i in ["n", "f"]:
                                for epi_i in ["Is", "Ia"]:
                                    key_i = f"{gender_i}-{age_i}-{epi_i}-{fortility_i}"
                                    infected_val += agents_dist[key_i] * params[f"beta_{key_i}"]

                    infected_group[key] = round(s_count * infected_val)

        # update the wanted numbers
        for agent in self.agents:
            key = agent.get_desp()
            if key in infected_group:
                agent.infect()
                infected_group[key] -= 1
                if infected_group[key] == 0:
                    del infected_group[key]
                    if len(infected_group) == 0:
                        break
