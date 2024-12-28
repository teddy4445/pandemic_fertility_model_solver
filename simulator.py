# library imports

# project imports


class Simulation:

    def __init__(self, params, initial_condition, is_control_case, initial_infraction_rate = 0.0001):
        # setup for them model
        self.params = params
        self.initial_condition = initial_condition

        self.population = {}
        for epi_state in ["s", "e", "is", "ia", "r"]:
            for gender in ["m", "f"]:
                for age in ["c", "a", "e"]:
                    for f_d in ["y", "n"]:
                        if f_d == "y" or epi_state != "s":
                            self.population[f"{epi_state}_{age}_{gender}_{f_d}"] = 0
                        else:
                            self.population[f"{epi_state}_{age}_{gender}_{f_d}"] = initial_condition["size"] * initial_condition["age"][age]/100 * initial_condition["gender"][gender]/100

        # set initial infection population
        if not is_control_case:
            self.population["is_a_m_n"] = initial_condition["size"] * initial_infraction_rate / 2
            self.population["is_a_f_n"] = initial_condition["size"] * initial_infraction_rate / 2
        
        # technical vars
        self.history = []

    def __repr__(self):
        return "<Simulator>"

    def __str__(self):
        return "<Simulator>"

    def get_history(self):
        return self.history

    def get_result(self):
        return sum(self.history)/len(self.history)
        
    def run(self):
        [self.run_step() for _ in range(self.params["T"])]
        return self

    def run_step(self):
        # calc general stuff we need
        born = self.calc_born()
        infects = self.infection_count()

        key = "s_c_m_n"
        self.population[key] = self.params["tau"] * born - self.population[key] * infects + self.params["delta"] * self.population["r_c_m_n"] - self.params["d_c"] * self.population[key] - self.params["alpha_ca"] * self.population[key]

        key = "s_c_f_n"
        self.population[key] = (1 - self.params["tau"]) * born - self.population[key] * infects + self.params["delta"] * self.population["r_c_m_n"] - self.params["d_c"] * self.population[key] - self.params["alpha_ca"] * self.population[key]

        # TODO: finish the other equations - note Eq. (1) in the paper shows half of the equations as we have both males and females

        # Log the current state
        self.history.append(born)

    def calc_born(self):
        m_healthy = 0
        f_healthy = 0
        m_sick = 0
        f_sick = 0

        for epi_state in ["s", "e", "is", "ia", "r"]:
            m_healthy += self.population[f"{epi_state}_a_m_n"]
            f_healthy += self.population[f"{epi_state}_a_f_n"]
            m_sick += self.population[f"{epi_state}_a_m_y"]
            f_sick += self.population[f"{epi_state}a_f_y"]

        return self.params["omega"] * (self.params["xi"] * m_healthy * f_sick +
                                       self.params["xi"]**2 * m_sick * f_sick +
                                       m_healthy * f_healthy +
                                       self.params["xi"] * m_sick * f_healthy)

def infection_count(self):
    infection_rate = 0

    # Iterate over each gender, age group, and infection category
    for g in ['m', 'f']:  # Gender: 'm', 'f'
        for i in ['c', 'a', 'e']:  # Age groups: 'c' (child), 'a' (adult), 'e' (elderly)
            for f_d in ['y', 'n']:  # Focused infection: 'y' or 'n'
                # Calculate infection rate from susceptible to infected (both s and a)
                infection_rate += (
                        self.params["beta"] * self.population.get(f"is_{i}_{g}_{f_d}", 0) +
                        self.params["beta"] * self.population.get(f"ia_{i}_{g}_{f_d}", 0)
                )

    return infection_rate
