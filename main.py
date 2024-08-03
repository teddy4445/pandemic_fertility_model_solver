# library imports
import os

# project imports 
from simulator_runner import SimulatorRunner

def run():
    # TODO: ARIEL - these numbers are wrong and probably not all you need for the simulation

    alpha_ca = 3650  # Children to adults in 10 years (3650 days)
    alpha_ae = 10950  # Adults to elderly in 30 years (10950 days)
    alpha_ed = 3650  # Elderly death rate (arbitrary example)
    rho = 0.3  # Probability of being asymptomatic
    phi = 5  # Days to move from exposed to infectious
    gamma_a = 7  # Days to recover for asymptomatic
    gamma_s = 14  # Days to recover for symptomatic
    lambda_prob = 0.02  # Probability of dying when symptomatic
    delta = 180  # Days to lose immunity
    fertility_drop_prob = 0.1  # Probability of fertility dropping after symptomatic recovery
    omega = 0.01  # Birth rate coefficient (example value)
    xi = 0.5  # Fertility rate adjustment for recovered individuals (example value)

    # Infection rates (arbitrary for example)
    beta_s = 0.05
    beta_a = 0.01
    
    # Initialize and run simulations
    simulator_runner = SimulatorRunner(population_size=1000, initial_infected=0.01, days=200, alpha_ca=alpha_ca, alpha_ae=alpha_ae, alpha_ed=alpha_ed, beta_s=beta_s, beta_a=beta_a, phi=phi, gamma_a=gamma_a, gamma_s=gamma_s, lambda_prob=lambda_prob, fertility_drop_prob=fertility_drop_prob, omega=omega, xi=xi)
    simulator_runner.run_multiple_simulations(n=5, save_path_prefix='simulation_results')


if __name__ == '__main__':
    run()
