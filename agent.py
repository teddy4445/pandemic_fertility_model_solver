# library imports
import random
import matplotlib.pyplot as plt
import numpy as np

class Agent:

    def __init__(self, age_group, gender, epi_state):
        self.age_group = age_group
        self.gender = gender
        self.state = epi_state 
        self.age_clock = 0
        self.epi_clock = 0
        self.fertility = 1.0  

    def update(self, alpha_ca, alpha_ae, alpha_ed, phi, gamma_a, gamma_s, lambda_prob, fertility_drop_prob, fertility_drop_rate):
        self.age(alpha_ca, alpha_ae, alpha_ed)
        self.progress_disease(phi, gamma_a, gamma_s, lambda_prob, fertility_drop_prob)

    def age(self, alpha_ca, alpha_ae, alpha_ed):
        self.age_clock += 1
        # Age transition logic
        if self.age_group == 'c' and self.age_clock >= alpha_ca:
            self.age_group = 'a'
            self.age_clock = 0
        elif self.age_group == 'a' and self.age_clock >= alpha_ae:
            self.age_group = 'e'
            self.age_clock = 0
        elif self.age_group == 'a' and self.age_clock >= alpha_ed:
            self.state = 'D'
            self.age_clock = 0

    def progress_disease(self, phi, gamma_a, gamma_s, lambda_prob, fertility_drop_prob, fertility_drop_rate):
        if self.state == 'E' and self.epi_clock >= phi:
            if random.random() < rho:
                self.state = 'Ia'
            else:
                self.state = 'Is'
            self.epi_clock = 0
        elif self.state == 'Ia' and self.epi_clock >= gamma_a:
            self.state = 'R'
            self.epi_clock = 0
        elif self.state == 'Is' and self.epi_clock >= gamma_s:
            if random.random() < lambda_prob:
                self.state = 'R'
                if self.age_group == 'a' and random.random() < fertility_drop_prob:
                    self.fertility *= fertility_drop_rate 
            else:
                self.state = 'D'  # Dead - not part of the model, remove these at the end of each simulation step from the model
            self.epi_clock = 0
        elif self.state == 'R' and self.epi_clock >= delta:
            self.state = 'S'
            self.epi_clock = 0

