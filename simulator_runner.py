# library imports

# project imports
from plotter import Plotter
from simulator import Simulation
from simulator_generator import SimulationGenerator

# CONSTS #
cities = ['Delhi, India', 'Shanghai, China', 'Paris, France', 'Istanbul, Turkey', 'London, UK', 'Toronto, Canada', 'Tel Aviv, Israel', 'New York, USA', 'Sao Paulo, Brazil', 'Berlin, Germany']
# END - CONSTS #

class SimulatorRunner:
    
    def __init__(self):
        pass

    def __repr__(self):
        return "<SimulatorRunner>"

    def __str__(self):
        return "<SimulatorRunner>"

    def paper_run(self):
        """
        A single function to run all the logic needed to produce all the results for the paper
        :return:
        """
        self.run_fig2()
        self.run_fig3()
        self.run_table3()
        self.run_fig4()
        self.run_fig5()

    def run_fig2(self):
        history_cases = []
        for case in ["a", "b", "c"]:
            histories = {}
            for name in cities:
                vals = []
                for i in range(100):
                    case_sim = SimulationGenerator.generate(model_parameter_average=False,
                                                            city_initial_condition=name,
                                                            is_control_case=False)
                    if case == "a":
                        case_sim.params["beta"] = 0
                        case_sim.params["xi"] = 0
                    if case == "b":
                        case_sim.params["xi"] = 0
                    case = case_sim.run().history

                    control_sim = SimulationGenerator.generate(model_parameter_average=False,
                                                            city_initial_condition=name,
                                                            is_control_case=False)
                    control_sim.params = case_sim.params
                    control_sim.params["beta"] = 0
                    control = control_sim.run().history
                    b_over_time = [(case[i] - control[i])/control[i] if control[i] != 0 else 0 for i in range(len(case))]
                    vals.append(b_over_time)
                histories[name] = vals
            history_cases.append(histories)

        Plotter.fig2(histories=histories,
                     save_paths=["fig2_a.pdf", "fig2_b.pdf", "fig2_c.pdf"])

    def run_fig3(self):

        parameters_min_max = {"beta": (3.36e-2, 1.73e-1, "Average fertility decline (B)"),
                              "xi": (0.04, 0.06, "Pandemic-caused fertility decline ($\\xi$)"),
                              "delta": (1.1e-2 * 0.5, 1.1e-2 * 1.5, "Pandemic-caused fertility decline ($\\delta$)")}

        for parameter, min_max in parameters_min_max.items():

            means = []
            stds = []
            parameter_values = [min_max[0] + (min_max[1] - min_max[0]) * i / 10 for i in range(11)]
            for index, beta in enumerate(parameter_values):
                vals = []
                for name in cities:
                    for i in range(100):
                        case_sim = SimulationGenerator.generate(model_parameter_average=False,
                                                                city_initial_condition=name,
                                                                is_control_case=False)
                        case_sim.params[parameter] = beta
                        case = case_sim.run().history

                        control_sim = SimulationGenerator.generate(model_parameter_average=False,
                                                                   city_initial_condition=name,
                                                                   is_control_case=False)
                        control_sim.params = case_sim.params
                        control_sim.params["beta"] = 0
                        control = control_sim.run().history
                        b_over_time = [(case[i] - control[i]) / control[i] if control[i] != 0 else 0 for i in range(len(case))]
                        vals.append(sum(b_over_time)/len(b_over_time))
                means.append(np.mean(vals))
                stds.append(np.std(vals))

            Plotter.fig3(means=means,
                         stds=stds,
                         x_label="Average infection rate ($\\beta$)",
                         y_label=min_max[2],
                         save_path=f"fig3_{parameter}.pdf")


    def run_table3(self):
        pass

    def run_fig4(self):
        pass

    def run_fig5(self):
        pass
