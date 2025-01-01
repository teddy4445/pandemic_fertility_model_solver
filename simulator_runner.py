# library imports
import numpy as np
import pandas as pd
from tqdm import tqdm
import statsmodels.api as sm

# project imports
from plotter import Plotter
from simulator import Simulation
from simulator_generator import SimulationGenerator

# CONSTS #
cities = ['Delhi, India', 'Shanghai, China', 'Paris, France', 'Istanbul, Turkey', 'London, UK', 'Toronto, Canada', 'Tel Aviv, Israel', 'New York, USA', 'Sao Paulo, Brazil', 'Berlin, Germany']
colors = ["#006400", "#00008b", "#b03060", "#ff0000", "#ffff00", "#deb887", "#00ff00", "#00ffff", "#ff00ff", "#6495ed"]
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
        # Define base parameters and calculate their 50-150% range
        base_parameters = SimulationGenerator.get_parameters_mean()

        parameters_min_max = {
            param: (value * 0.5, value * 1.5, f"Sensitivity of {param}")
            for param, value in base_parameters.items()
        }

        # Data storage
        raw_data = []
        stats_data = []

        # Perform sensitivity analysis for each parameter
        for parameter, min_max in parameters_min_max.items():
            means = []
            stds = []

            # Generate parameter range (50-150%)
            parameter_values = [
                min_max[0] + (min_max[1] - min_max[0]) * i / 10 for i in range(11)
            ]

            for param_value in parameter_values:
                vals = []

                for city in cities:
                    for _ in range(10):
                        # Generate case simulation
                        case_sim = SimulationGenerator.generate(
                            model_parameter_average=False,
                            city_initial_condition=city,
                            is_control_case=False
                        )
                        case_sim.params[parameter] = param_value
                        case_history = case_sim.run().history

                        # Generate control simulation
                        control_sim = SimulationGenerator.generate(
                            model_parameter_average=False,
                            city_initial_condition=city,
                            is_control_case=False
                        )
                        control_sim.params = case_sim.params.copy()
                        control_sim.params["beta"] = 0
                        control_history = control_sim.run().history

                        # Calculate b_over_time
                        b_over_time = [
                            (casee - control) / control if control != 0 else 0
                            for casee, control in zip(case_history, control_history)
                        ]
                        vals.append(np.mean(b_over_time))mean_val = np.mean(vals)
                    std_val = np.std(vals)
                    raw_data.append({
                        "parameter": parameter,
                        "value": param_value,
                        "city": city,
                        "mean": mean_val,
                        "std": std_val,
                    })
                    city_means.append(mean_val)

                aggregated_means.append(np.mean(city_means))
                aggregated_stds.append(np.std(city_means))

            # Perform linear regression
            slope, intercept, r_value, p_value, std_err = linregress(parameter_values, aggregated_means)
            confidence_interval = (slope - 1.96 * std_err, slope + 1.96 * std_err)
            stats_data.append({
                "parameter": parameter,
                "value": param_value,
                "p-value": p_value,
                "confidence_interval": confidence_interval,
            })

        # Save raw data to CSV
        raw_data_df = pd.DataFrame(raw_data)
        raw_data_df.to_csv("raw_table_3.csv", index=False)

        # Save statistical results to CSV
        stats_data_df = pd.DataFrame(stats_data)
        stats_data_df.to_csv("table_3.csv", index=False)


    def run_fig4(self):
        # Define base parameters (average values of Table 1 ranges)/
        base_parameters = SimulationGenerator.get_parameters_mean()

        # Heatmap configurations
        heatmaps = {
            "A": {"parameters": ["xi", "omega"], "values": []},
            "B": {"parameters": ["beta", "phi"], "values": []},
            "C": {"parameters": ["beta", "gamma_s"], "values": []},
        }

        sim_counts = len(cities)

        # Run simulations for each pair of parameters
        for heatmap_key, config in heatmaps.items():
            param1, param2 = config["parameters"]

            # Create a grid of 11x11 for parameter values
            param1_values = np.linspace(base_parameters[param1] * 0.5, base_parameters[param1] * 1.5, 11)
            param2_values = np.linspace(base_parameters[param2] * 0.5, base_parameters[param2] * 1.5, 11)

            # Collect means for each combination
            results_grid = []

            for p1 in param1_values:
                row = []
                for p2 in param2_values:
                    simulation_means = []

                    for city in cities:
                        b_values = []
                        for _ in range(sim_counts // len(cities)):  # Divide n by cities for balanced runs
                            # Case simulation
                            sim_case = SimulationGenerator.generate(
                                model_parameter_average=False,
                                city_initial_condition=city,
                                is_control_case=False
                            )
                            sim_case.params[param1] = p1
                            sim_case.params[param2] = p2
                            case_history = sim_case.run().history

                            # Control simulation (\(\beta = 0\))
                            sim_control = SimulationGenerator.generate(
                                model_parameter_average=False,
                                city_initial_condition=city,
                                is_control_case=True
                            )
                            sim_control.params["beta"] = 0
                            control_history = sim_control.run().history

                            # Calculate \( B \) over time
                            b_over_time = [
                                (casee - control) / control if control != 0 else 0
                                for casee, control in zip(case_history, control_history)
                            ]
                            b_values.append(np.mean(b_over_time))

                        simulation_means.extend(b_values)

                    row.append(np.mean(simulation_means))
                results_grid.append(row)

            # Save results and create heatmap
            heatmaps[heatmap_key]["values"] = results_grid

            # Use Plotter for visualization
            Plotter.fig4(
                values=results_grid,
                x_ticks=param2_values.round(3),
                y_ticks=param1_values.round(3),
                x_label=param2,
                y_label=param1,
                save_path=f"heatmap_{heatmap_key}.png"
            )

        # Save raw data
        for key, config in heatmaps.items():
            df = pd.DataFrame(config["values"],
                              index=param1_values,
                              columns=param2_values)
            df.to_csv(f"heatmap_{key}_data.csv")

    def run_fig5(self):
        # Define ranges for parameters
        base_parameters = SimulationGenerator.get_parameters_mean()
        xi_range = np.linspace(0.5 * base_parameters["xi"], 1.5 * base_parameters["xi"], 100)  # Example range for \xi
        beta_range = np.linspace(0.5 * base_parameters["beta"], 1.5 * base_parameters["beta"], 100)  # Example range for \beta

        # For reproducibility
        np.random.seed(42)

        n = 100

        # Randomly sample parameter pairs
        xi_samples = np.random.choice(xi_range, size=n, replace=False)
        beta_samples = np.random.choice(beta_range, size=n, replace=False)

        final_data = {"xi": [], "beta": [], "B_mean": [], "B_std": [], "city": []}

        for city_index, city in enumerate(cities):
            x_vals = []
            y_vals = []
            z_means = []
            z_stds = []

            for xi, beta in zip(xi_samples, beta_samples):
                b_values = []

                for _ in range(10):
                    # Case simulation
                    sim_case = SimulationGenerator.generate(
                        model_parameter_average=False,
                        city_initial_condition=city,
                        is_control_case=False
                    )
                    sim_case.params["xi"] = xi
                    sim_case.params["beta"] = beta
                    case_history = sim_case.run().history

                    # Control simulation (\(\beta = 0\))
                    sim_control = SimulationGenerator.generate(
                        model_parameter_average=False,
                        city_initial_condition=city,
                        is_control_case=True
                    )
                    sim_control.params["beta"] = 0
                    control_history = sim_control.run().history

                    # Calculate \( B \) over time
                    b_over_time = [
                        (casee - control) / control if control != 0 else 0
                        for casee, control in zip(case_history, control_history)
                    ]
                    b_values.append(np.mean(b_over_time))

                # Record mean and std for \( B \)
                x_vals.append(xi)
                y_vals.append(beta)
                z_means.append(np.mean(b_values))
                z_stds.append(np.std(b_values))

                # Append to final data
                final_data["xi"].append(xi)
                final_data["beta"].append(beta)
                final_data["B_mean"].append(np.mean(b_values))
                final_data["B_std"].append(np.std(b_values))
                final_data["city"].append(city)

            # Generate 3D scatter plot
            fig = plt.figure(figsize=(12, 10))
            ax = fig.add_subplot(111, projection="3d")
            ax.scatter(x_vals, y_vals, z_means, color="black", alpha=0.5)

            # Add STD visualization using `fill_between`
            for i in range(len(x_vals)):
                ax.plot(
                    [x_vals[i], x_vals[i]],
                    [y_vals[i], y_vals[i]],
                    [z_means[i] - z_stds[i], z_means[i] + z_stds[i]],
                    color="gray",
                    alpha=0.25
                )

            ax.set_xlabel("\u03BE (xi)", fontsize=16)
            ax.set_ylabel("\u03B2 (beta)", fontsize=16)
            ax.set_zlabel("B", fontsize=16)
            ax.grid(True, alpha=0.5)
            ax.view_init(30, 120)  # Customize view angle

            plt.tight_layout()
            plt.savefig(f"scatter_{city}.png", dpi=400)
            plt.close()


        # Generate final aggregated plot
        fig = plt.figure(figsize=(14, 12))
        ax = fig.add_subplot(111, projection="3d")

        for city_index, city in enumerate(cities):
            city_data = {
                "xi": np.array([xi for xi, c in zip(final_data["xi"], final_data["city"]) if c == city]),
                "beta": np.array([beta for beta, c in zip(final_data["beta"], final_data["city"]) if c == city]),
                "B_mean": np.array([b for b, c in zip(final_data["B_mean"], final_data["city"]) if c == city]),
                "B_std": np.array([std for std, c in zip(final_data["B_std"], final_data["city"]) if c == city]),
            }

            ax.scatter(city_data["xi"], city_data["beta"], city_data["B_mean"], color=colors[city_index],
                       label=city, alpha=0.5)

            for i in range(len(city_data["xi"])):
                ax.plot(
                    [city_data["xi"][i], city_data["xi"][i]],
                    [city_data["beta"][i], city_data["beta"][i]],
                    [city_data["B_mean"][i] - city_data["B_std"][i], city_data["B_mean"][i] + city_data["B_std"][i]],
                    color=colors[city_index],
                    alpha=0.25
                )

        ax.set_xlabel("\u03BE (xi)", fontsize=16)
        ax.set_ylabel("\u03B2 (beta)", fontsize=16)
        ax.set_zlabel("B", fontsize=16)
        ax.legend()
        ax.grid(True, alpha=0.5)
        ax.view_init(30, 120)  # Customize view angle
        plt.tight_layout()
        plt.savefig(f"scatter_all_cities.png", dpi=400)
        plt.close()
