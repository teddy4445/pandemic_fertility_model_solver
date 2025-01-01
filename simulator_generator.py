# library imports
import random

# project imports
from simulator import Simulation


class SimulationGenerator:

    def __init__(self):
        pass

    def __repr__(self):
        return "<SimulationGenerator>"

    def __str__(self):
        return "<SimulationGenerator>"

    @staticmethod
    def generate(model_parameter_average,
                 city_initial_condition,
                 is_control_case):
        params = SimulationGenerator.get_parameters_mean() if model_parameter_average else SimulationGenerator.get_parameters_sampled()
        city_data = get_cities_data()[city_initial_condition]
        if is_control_case:
            params["beta"] = 0
        answer = Simulation(params=params,
                            initial_condition=city_data,
                            is_control_case=is_control_case)
        return answer

    @staticmethod
    def get_parameters_mean():
        parameters = {
            "T": 3650,  # Single value
            "beta": (3.36e-2 + 1.73e-1) / 2,  # Average of range
            "phi": 1/((4 + 7) / 2),  # Average of range
            "d_c": 5.9e-6,  # Non-disease death rate for c
            "d_a": 1.51e-6,  # Non-disease death rate for as
            "d_e": 1.7e-4,  # Non-disease death rate for e
            "rho": (0.01 + 0.1) / 2,  # Average of range
            "gamma_s": (0.90 + 1.00) / 2,  # Average of range
            "gamma_a": (0.98 + 1.00) / 2,  # Average of range
            "lambda": 0.96,  # Single value
            "delta": 1.1e-2,  # Single value
            "alpha_ca": 1.52e-4,  # Single value
            "alpha_ae": 1.10e-4,  # Single value
            "alpha_ed": 7.94e-5,  # Single value
            "omega": (0.05661 + 0.06919) / 2,  # Average of range
            "xi": (0.04 + 0.06) / 2,  # Average of range
            "tau": (0.485 + 0.515) / 2,  # Single value
            "zeta": 0.95
        }
        return parameters

def get_parameters_sampled():
    parameters = {
        "T": 3650,  # Single value
        "beta": random.uniform(3.36e-2, 1.73e-1),  # Uniform sampling
        "phi": random.uniform(4, 7),  # Uniform sampling
        "d_c": 5.9e-6,  # Non-disease death rate for c (single value)
        "d_a": 1.51e-6,  # Non-disease death rate for as (single value)
        "d_e": 1.7e-4,  # Non-disease death rate for e (single value)
        "rho": random.uniform(0.01, 0.1),  # Uniform sampling
        "gamma_s": random.uniform(0.90, 1.00),  # Uniform sampling
        "gamma_a": random.uniform(0.98, 1.00),  # Uniform sampling
        "lambda": 0.96,  # Single value
        "delta": 1.1e-2,  # Single value
        "alpha_ca": 1.52e-4,  # Single value
        "alpha_ae": 1.10e-4,  # Single value
        "alpha_ed": 7.94e-5,  # Single value
        "omega": random.uniform(0.05661, 0.06919),  # Uniform sampling
        "xi": random.uniform(0.04, 0.06),  # Uniform sampling
        "tau": random.uniform(0.485, 0.515),  # Uniform sampling
        "zeta": 0.95
    }
    return parameters

@staticmethod
def get_cities_data():
    cities_data = {
        "Delhi, India": {
            "size": 16.78e6,
            "TFR": 2.100,
            "age": {"c": 37.2, "a": 43.4, "e": 19.4},
            "gender": {"f": 46.5, "m": 53.5},
        },
        "Shanghai, China": {
            "size": 24.87e6,
            "TFR": 1.281,
            "age": {"c": 12.6, "a": 35.3, "e": 52.1},
            "gender": {"f": 48.2, "m": 51.8},
        },
        "Paris, France": {
            "size": 2.14e6,
            "TFR": 1.460,
            "age": {"c": 16.2, "a": 49.4, "e": 34.4},
            "gender": {"f": 53.0, "m": 47.0},
        },
        "Istanbul, Turkey": {
            "size": 15.46e6,
            "TFR": 2.046,
            "age": {"c": 25.6, "a": 45.0, "e": 29.4},
            "gender": {"f": 49.9, "m": 50.1},
        },
        "London, UK": {
            "size": 8.78e6,
            "TFR": 1.530,
            "age": {"c": 21.5, "a": 47.5, "e": 31.0},
            "gender": {"f": 51.5, "m": 48.5},
        },
        "Toronto, Canada": {
            "size": 2.79e6,
            "TFR": 1.440,
            "age": {"c": 16.1, "a": 40.9, "e": 43.0},
            "gender": {"f": 51.6, "m": 48.4},
        },
        "Tel Aviv, Israel": {
            "size": 0.46e6,
            "TFR": 3.000,
            "age": {"c": 18.4, "a": 38.7, "e": 42.9},
            "gender": {"f": 50.3, "m": 49.7},
        },
        "New York, USA": {
            "size": 19.99e6,
            "TFR": 1.560,
            "age": {"c": 23.3, "a": 33.7, "e": 43.0},
            "gender": {"f": 51.1, "m": 48.9},
        },
        "Sao Paulo, Brazil": {
            "size": 11.45e6,
            "TFR": 1.630,
            "age": {"c": 45.6, "a": 37.4, "e": 17.0},
            "gender": {"f": 53.0, "m": 47.0},
        },
        "Berlin, Germany": {
            "size": 3.80e6,
            "TFR": 1.616,
            "age": {"c": 17.0, "a": 39.0, "e": 44.0},
            "gender": {"f": 51.0, "m": 49.0},
        },
    }
    return cities_data


