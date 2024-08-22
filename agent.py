# library imports
import random


class Agent:

    def __init__(self, age_group, gender, epi_state):
        self.age_group = age_group
        self.gender = gender
        self.state = epi_state
        self.age_clock = 0
        self.epi_clock = 0
        self.fertility = "n"

    def __repr__(self):
        return "<Agent>"

    def __str__(self):
        return "<Agent: age={}, gender={}, state={}, fertility={}, age_clock={}, epi_clock={}>".format(self.age_group,
                                                                                                       self.gender,
                                                                                                       self.state,
                                                                                                       self.fertility,
                                                                                                       self.age_clock,
                                                                                                       self.epi_clock)

    def get_desp(self):
        return f"{self.gender}-{self.age_group}-{self.state}-{self.fertility}"

    def update(self,
               params):
        self.age(params=params)
        self.progress_disease(params=params)

    def infect(self):
        self.state = "E"
        self.epi_clock = 0

    def age(self,
            params: dict):
        self.age_clock += 1
        # Age transition logic
        if self.age_group == 'c' and self.age_clock >= params["alpha_ca"]:
            self.age_group = 'a'
            self.age_clock = 0
        elif self.age_group == 'a' and self.age_clock >= params["alpha_ae"]:
            self.age_group = 'e'
            self.age_clock = 0
        elif self.age_group == 'a' and self.age_clock >= params["alpha_ed"]:
            self.state = 'D'
            self.age_clock = 0

    def progress_disease(self,
                         params: dict):
        self.epi_clock += 1
        if self.state == 'E' and self.epi_clock >= params["phi_{},{}".format(self.gender, self.age_group)]:
            if random.random() < params["rho_{}".format(self.gender)]:
                self.state = 'Ia'
            else:
                self.state = 'Is'
            self.epi_clock = 0
        elif self.state == 'Ia' and self.epi_clock >= params["gamma_a_{}".format(self.gender)]:
            self.state = 'R'
            self.epi_clock = 0
        elif self.state == 'Is' and self.epi_clock >= params["gamma_s_{}".format(self.gender)]:
            if random.random() < params["lambda_{}".format(self.gender)]:
                self.state = 'R'
                if self.age_group == 'a' and random.random() < params["fertility_drop_prob"]:
                    self.fertility = "f"
            else:
                self.state = 'D'  # Dead - not part of the model, remove these at the end of each simulation step from the model
            self.epi_clock = 0
        elif self.state == 'R' and self.epi_clock >= params["delta_{}".format(self.gender)]:
            self.state = 'S'
            self.epi_clock = 0
