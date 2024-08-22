# library imports
import os

# project imports
from loading_bar import LoadingBar
from simulator_runner import SimulatorRunner

# global for the project
loading_bars = LoadingBar()


def run():
    # TODO: ARIEL - these numbers are wrong and probably not all you need for the simulation
    genders = ['m', 'f']
    ages = ['c', 'a', 'e']
    epistates = ['S', 'E', "Is", "Ia", "R"]
    fertilities = ['n', 'f']

    params = {
        # Disease parameters
        'phi_m,c': 5,  # Progression rate from S to E for male childhood
        'phi_m,a': 5,  # Progression rate from S to E for male adulthood
        'phi_m,e': 5,  # Progression rate from S to E for male elderly
        'phi_f,c': 5,  # Progression rate from S to E for female childhood
        'phi_f,a': 5,  # Progression rate from S to E for female adulthood
        'phi_f,e': 5,  # Progression rate from S to E for female elderly

        'gamma_a_m': 2,  # Recovery rate from Ia to R for male
        'gamma_s_m': 3,  # Recovery rate from Is to R for male
        'gamma_a_f': 2,  # Recovery rate from Ia to R for female
        'gamma_s_f': 3,  # Recovery rate from Is to R for female

        # Mortality and other parameters
        'delta_m': 0.1,  # Natural death rate for male
        'delta_f': 0.1,  # Natural death rate for female

        # Parameters for fertility-related dynamics
        'lambda_m': 0.05,  # Fertility rate for male
        'lambda_f': 0.05,  # Fertility rate for female
        'fertility_drop_prob': 0.1,  # Probability of fertility drop
        'fertility_drop_rate': 0.9,  # Rate of fertility drop

        # Aging parameters
        'alpha_ca': 10,  # Aging transition from childhood to adulthood
        'alpha_ae': 20,  # Aging transition from adulthood to elderly
        'alpha_ed': 30,  # Aging transition from elderly to deceased

        # Infection transition probabilities
        # TOOD: add later

        # Berth-related parameters
        "omega": 0.001,
        "xi": 0.5,

        # Disease dynamics and interactions
        'rho_m': 0.7,  # Probability of Ia state from E for male
        'rho_f': 0.7,  # Probability of Ia state from E for female
        'zeta': 0.5,  # Fraction of recovered individuals moving to susceptible state for male and female

        # Other parameters
        'infect': 0.01  # Base infection rate for susceptible group
    }
    for gender in genders:
        for age in ages:
            for epi_state in ["Is", "Ia"]:
                for fertility in fertilities:
                    key_i = f"{gender}-{age}-{epi_state}-{fertility}"
                    beta_key = f"beta_{key_i}"
                    params[beta_key] = 0.001
    
    # Initialize and run simulations
    simulator_runner = SimulatorRunner(population_size=1000,
                                       initial_infected=0.01,
                                       days=100,
                                       params=params)
    simulator_runner.run_multiple_simulations(n=5,
                                              save_path='simulation_results',
                                              verbose=LoadingBar())


if __name__ == '__main__':
    run()
