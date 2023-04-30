from stable_baselines import results_plotter

results_plotter.plot_results(["./log/SAC_1"], 10e6, results_plotter.X_TIMESTEPS, "Breakout")