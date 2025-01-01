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

    def run_step(self, h = 1):
        # calc general stuff we need
        born = self.calc_born()
        infects = self.infection_count()

        key = "s_c_m_n"
        self.population[key] = self.population[key] + h * (self.params["tau"] * born - self.population[key] * infects + self.params["delta"] * self.population["r_c_m_n"] - self.params["d_c"] * self.population[key] - self.params["alpha_ca"] * self.population[key])

        key = "s_c_f_n"
        self.population[key] = self.population[key] + h * ((1 - self.params["tau"]) * born - self.population[key] * infects + self.params["delta"] * self.population["r_c_m_n"] - self.params["d_c"] * self.population[key] - self.params["alpha_ca"] * self.population[key])

        key = "e_c_m_n"
        self.population[key] = self.population[key] + h * (self.population["s_c_m_n"] * infects - (self.params["phi"] + self.params["d_c"] + self.params["alpha_ca"]) * self.population[key])

        key = "e_c_f_n"
        self.population[key] = self.population[key] + h * (self.population["s_c_f_n"] * infects - (self.params["phi"] + self.params["d_c"] + self.params["alpha_ca"]) * self.population[key])

        key = "ia_c_m_n"
        self.population[key] = self.population[key] + h * (self.params["rho"] * self.params["phi"] * self.population["e_c_m_n"] - (self.params["gamma_a"] + self.params["d_c"] + self.params["alpha_ca"]) * self.population[key])

        key = "ia_c_f_n"
        self.population[key] = self.population[key] + h * (self.params["rho"] * self.params["phi"] * self.population["e_c_f_n"] - (self.params["gamma_a"] + self.params["d_c"] + self.params["alpha_ca"]) * self.population[key])

        key = "is_c_m_n"
        self.population[key] = self.population[key] + h * ((1 - self.params["rho"]) * self.params["phi"] * self.population["e_c_f_n"] - (self.params["gamma_s"] + self.params["d_c"] + self.params["alpha_ca"]) * self.population[key])

        key = "is_c_f_n"
        self.population[key] = self.population[key] + h * ((1 - self.params["rho"]) * self.params["phi"] * self.population["e_c_f_n"] - (self.params["gamma_s"] + self.params["d_c"] + self.params["alpha_ca"]) * self.population[key])

        key = "r_c_m_n"
        self.population[key] = self.population[key] + h * (self.params["gamma_a"] * self.population["ia_c_m_n"] + self.params["gamma_s"] * self.population["is_c_m_n"] - (self.params["delta"] + self.params["d_c"] + self.params["alpha_ca"]) * self.population[key])

        key = "r_c_f_n"
        self.population[key] = self.population[key] + h * (self.params["gamma_a"] * self.population["ia_c_f_n"] + self.params["gamma_s"] * self.population["is_c_f_n"] - (self.params["delta"] + self.params["d_c"] + self.params["alpha_ca"]) * self.population[key])

        key = "r_c_m_n"
        self.population[key] = self.population[key] + h * (self.params["gamma_a"] * self.population["ia_c_m_n"] + self.params["lambda"] * self.params["gamma_s"] * self.population["is_c_m_n"] - (self.params["delta"] + self.params["d_c"] + self.params["alpha_ca"]) * self.population[key])

        key = "r_c_f_n"
        self.population[key] = self.population[key] + h * (self.params["gamma_a"] * self.population["ia_c_f_n"] + self.params["lambda"] * self.params["gamma_s"] * self.population["is_c_f_n"] - (self.params["delta"] + self.params["d_c"] + self.params["alpha_ca"]) * self.population[key])

        key = "s_a_m_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ca"] * self.population["s_c_m_n"] - self.population[key] * infects + (1 - self.params["xi"])*self.params["delta"]*self.population["r_a_m_n"] - (self.params["d_a"] + self.params["alpha_ae"]) * self.population[key])

        key = "s_a_f_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ca"] * self.population["s_c_f_n"] - self.population[key] * infects + (1 - self.params["xi"])*self.params["delta"]*self.population["r_a_f_n"] - (self.params["d_a"] + self.params["alpha_ae"]) * self.population[key])

        key = "e_a_m_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ca"] * self.population["e_c_m_n"] + self.population["s_a_m_n"] * infects- (self.params["phi"] + self.params["d_a"] + self.params["alpha_ae"]) * self.population[key])

        key = "e_a_f_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ca"] * self.population["e_c_f_n"] + self.population["s_a_f_n"] * infects- (self.params["phi"] + self.params["d_a"] + self.params["alpha_ae"]) * self.population[key])

        key = "ia_a_m_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ca"] * self.population["ia_c_m_n"] + self.params["rho"] * self.params["phi"] * self.population["e_a_m_n"] - (self.params["d_a"] + self.params["gamma_a"] + self.params["alpha_ae"]) * self.population[key])

        key = "ia_a_f_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ca"] * self.population["ia_c_f_n"] + self.params["rho"] * self.params["phi"] * self.population["e_a_f_n"] - (self.params["d_a"] + self.params["gamma_a"] + self.params["alpha_ae"]) * self.population[key])

        key = "is_a_m_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ca"] * self.population["is_c_m_n"] + (1-self.params["rho"]) * self.params["phi"] * self.population["e_a_m_n"] - (self.params["d_a"] + self.params["gamma_s"] + self.params["alpha_ae"]) * self.population[key])

        key = "is_a_f_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ca"] * self.population["is_c_f_n"] + (1-self.params["rho"]) * self.params["phi"] * self.population["e_a_f_n"] - (self.params["d_a"] + self.params["gamma_s"] + self.params["alpha_ae"]) * self.population[key])

        key = "r_a_m_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ca"] * self.population["r_c_m_n"] + self.params["gamma_a"] * self.population["ia_a_m_n"] + self.params["lambda"] * self.params["gamma_s"] * self.population["is_a_m_n"] - (self.params["delta"] + self.params["d_a"] + self.params["alpha_ae"]) * self.population[key])

        key = "r_a_f_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ca"] * self.population["r_c_f_n"] + self.params["gamma_a"] * self.population["ia_a_f_n"] + self.params["lambda"] * self.params["gamma_s"] * self.population["is_a_f_n"] - (self.params["delta"] + self.params["d_a"] + self.params["alpha_ae"]) * self.population[key])

        key = "s_a_m_y"
        self.population[key] = self.population[key] + h * (self.params["xi"] * self.params["delta"] * self.population["r_a_m_y"] + self.params["delta"] * self.population["r_a_m_n"] - self.population[key] * infects - (self.params["d_a"] + self.params["alpha_ae"]) * self.population[key])

        key = "s_a_f_y"
        self.population[key] = self.population[key] + h * (self.params["xi"] * self.params["delta"] * self.population["r_a_f_y"] + self.params["delta"] * self.population["r_a_f_n"] - self.population[key] * infects - (self.params["d_a"] + self.params["alpha_ae"]) * self.population[key])

        key = "e_a_m_y"
        self.population[key] = self.population[key] + h * (self.population["s_a_m_y"] * infects - (self.params["phi"] + self.params["d_a"] + self.params["alpha_ae"]) * self.population[key])

        key = "e_a_f_y"
        self.population[key] = self.population[key] + h * (self.population["s_a_f_y"] * infects - (self.params["phi"] + self.params["d_a"] + self.params["alpha_ae"]) * self.population[key])

        key = "ia_a_m_y"
        self.population[key] = self.population[key] + h * (self.params["rho"] * self.params["phi"] * self.population["e_a_m_y"] - (self.params["gamma_a"] + self.params["d_a"] + self.params["alpha_ae"]) * self.population[key])

        key = "ia_a_f_y"
        self.population[key] = self.population[key] + h * (self.params["rho"] * self.params["phi"] * self.population["e_a_f_y"] - (self.params["gamma_a"] + self.params["d_a"] + self.params["alpha_ae"]) * self.population[key])

        key = "is_a_m_y"
        self.population[key] = self.population[key] + h * ((1-self.params["rho"]) * self.params["phi"] * self.population["e_a_m_y"] - (self.params["gamma_s"] + self.params["d_a"] + self.params["alpha_ae"]) * self.population[key])

        key = "is_a_f_y"
        self.population[key] = self.population[key] + h * ((1-self.params["rho"]) * self.params["phi"] * self.population["e_a_f_y"] - (self.params["gamma_s"] + self.params["d_a"] + self.params["alpha_ae"]) * self.population[key])

        key = "r_a_m_y"
        self.population[key] = self.population[key] + h * (self.params["gamma_a"] * self.population["ia_a_m_y"] + self.params["gamma_s"] * self.params["lambda"] * self.population["is_a_m_y"] - (self.params["delta"] + self.params["d_a"] + self.params["alpha_ae"]) * self.population[key])

        key = "r_a_f_y"
        self.population[key] = self.population[key] + h * (self.params["gamma_a"] * self.population["ia_a_f_y"] + self.params["gamma_s"] * self.params["lambda"] * self.population["is_a_f_y"] - (self.params["delta"] + self.params["d_a"] + self.params["alpha_ae"]) * self.population[key])

        key = "s_e_m_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ae"] * (self.population["s_a_m_n"] + self.population["s_a_m_y"]) - self.population[key] * infects + self.params["delta"] * self.population["r_e_m_n"] - (self.params["d_e"] + self.params["alpha_ed"]) * self.population[key])

        key = "s_e_f_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ae"] * (self.population["s_a_f_n"] + self.population["s_a_f_y"]) - self.population[key] * infects + self.params["delta"] * self.population["r_e_f_n"] - (self.params["d_e"] + self.params["alpha_ed"]) * self.population[key])

        key = "e_e_m_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ae"] * (self.population["e_a_m_n"] + self.population["e_a_m_y"]) + self.population[key] * infects - (self.params["phi"] + self.params["d_e"] + self.params["alpha_ed"]) * self.population[key])

        key = "e_e_f_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ae"] * (self.population["e_a_f_n"] + self.population["e_a_f_y"]) + self.population[key] * infects - (self.params["phi"] + self.params["d_e"] + self.params["alpha_ed"]) * self.population[key])

        key = "ia_e_m_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ae"] * (self.population["ia_a_m_n"] + self.population["ia_a_m_y"]) + self.params["rho"] * self.params["phi"] * self.population["e_e_m_n"] - (self.params["gamma_a"] + self.params["d_e"] + self.params["alpha_ed"]) * self.population[key])

        key = "ia_e_f_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ae"] * (self.population["ia_a_f_n"] + self.population["ia_a_f_y"]) + self.params["rho"] * self.params["phi"] * self.population["e_e_f_n"] - (self.params["gamma_a"] + self.params["d_e"] + self.params["alpha_ed"]) * self.population[key])

        key = "is_e_m_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ae"] * (self.population["is_a_m_n"] + self.population["is_a_m_y"]) + (1-self.params["rho"]) * self.params["phi"] * self.population["e_e_m_n"] - (self.params["gamma_s"] + self.params["d_e"] + self.params["alpha_ed"]) * self.population[key])

        key = "is_e_f_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ae"] * (self.population["is_a_f_n"] + self.population["is_a_f_y"]) + (1-self.params["rho"]) * self.params["phi"] * self.population["e_e_f_n"] - (self.params["gamma_s"] + self.params["d_e"] + self.params["alpha_ed"]) * self.population[key])

        key = "r_e_m_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ae"] * (self.population["r_a_m_n"] + self.population["r_a_m_y"]) + self.params["gamma_a"] * self.population["ia_e_m_n"] + self.params["lambda"] * self.params["gamma_s"] * self.population["is_e_m_n"] - (self.params["delta"] + self.params["d_e"] + self.params["alpha_ed"]) * self.population[key])

        key = "r_e_f_n"
        self.population[key] = self.population[key] + h * (self.params["alpha_ae"] * (self.population["r_a_f_n"] + self.population["r_a_f_y"]) + self.params["gamma_a"] * self.population["ia_e_f_n"] + self.params["lambda"] * self.params["gamma_s"] * self.population["is_e_f_n"] - (self.params["delta"] + self.params["d_e"] + self.params["alpha_ed"]) * self.population[key])

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
