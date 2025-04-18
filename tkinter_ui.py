import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from rocket_optimizer import genetic_algorithm, fitness_function
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import constants
import numpy as np

def run_algorithm():
    try:
        # Update constants from user input
        constants.g = float(entry_g.get())
        constants.Isp = float(entry_isp.get())
        constants.rho_prop = float(entry_rho_prop.get())
        constants.rho_wall = float(entry_rho_wall.get())
        constants.rho_bulkhead = float(entry_rho_bulkhead.get())
        constants.d_prop = float(entry_d_prop.get())
        constants.d_total = float(entry_d_total.get())
        constants.L_bulkhead = float(entry_L_bulkhead.get())
        constants.m_payload = float(entry_m_payload.get())
        
        # Recalculate derived constants
        constants.v_exhaust = constants.Isp * constants.g
        constants.m_bulkhead = (np.pi / 4) * (constants.d_total ** 2) * (constants.L_bulkhead) * (constants.rho_bulkhead)

        rocket_length = float(entry_length.get()) - 3 * constants.L_bulkhead
        if rocket_length <= 0:
            raise ValueError

        # Get population size (default 100)
        try:
            population_size = int(entry_population.get()) if entry_population.get() else 100
            if population_size <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Population size must be a positive integer.")
            return

        # Get number of generations (default 20)
        try:
            generations = int(entry_generations.get()) if entry_generations.get() else 20
            if generations <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Number of generations must be a positive integer.")
            return

        lower_bound = 0
        upper_bound = rocket_length
        mutation_rate = 10 / population_size

        import rocket_optimizer
        genetic_algorithm.rocket_length = rocket_length

        best_solution, figures = genetic_algorithm(
            population_size, lower_bound, upper_bound, generations, mutation_rate, rocket_length
        )
        delta_v = fitness_function(best_solution, rocket_length)

        result_text.set(f"Best Solution:\nL1 = {best_solution[0]:.2f} m\n"
                        f"L2 = {best_solution[1]:.2f} m\n"
                        f"L3 = {best_solution[2]:.2f} m\n"
                        f"Delta V = {delta_v:.2f} m/s")

        for widget in graph_frame.winfo_children():
            widget.destroy()

        fig, fig_lengths, fig_fitness = figures

        canvas_lengths = FigureCanvasTkAgg(fig_lengths, master=graph_frame)
        canvas_lengths.get_tk_widget().pack()
        canvas_lengths.draw()

        canvas_fitness = FigureCanvasTkAgg(fig_fitness, master=graph_frame)
        canvas_fitness.get_tk_widget().pack()
        canvas_fitness.draw()

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a positive numeric value for rocket length.")

def create_labeled_entry(label_text, default_value, row):
    tk.Label(frame, text=label_text).grid(row=row, column=0, sticky="w")
    entry = tk.Entry(frame)
    entry.insert(0, str(default_value))
    entry.grid(row=row, column=1)
    return entry

# UI Setup with fully scrollable window
root = tk.Tk()
root.title("Rocket Stage Optimizer")

# Canvas and scrollbar setup
main_canvas = tk.Canvas(root, borderwidth=0)
main_canvas.pack(side="left", fill="both", expand=True)

# Scrollable frame inside the canvas
container = tk.Frame(main_canvas)
canvas_window = main_canvas.create_window((0, 0), window=container, anchor="nw")

# Main content frame (inside scrollable container)
frame = tk.Frame(container, padx=20, pady=20)
frame.pack()

graph_frame = tk.Frame(container, padx=20, pady=20)
graph_frame.pack()

tk.Label(frame, text="Total Rocket Length (m):").grid(row=0, column=0, sticky="w")
entry_length = tk.Entry(frame)
entry_length.grid(row=0, column=1)

tk.Label(frame, text="Population Size (default: 100):").grid(row=1, column=0, sticky="w")
entry_population = tk.Entry(frame)
entry_population.grid(row=1, column=1)

tk.Label(frame, text="Generations (default: 20):").grid(row=2, column=0, sticky="w")
entry_generations = tk.Entry(frame)
entry_generations.grid(row=2, column=1)

tk.Label(frame, text="Gravity (g):").grid(row=5, column=0, sticky="w")
entry_g = tk.Entry(frame)
entry_g.insert(0, str(constants.g))
entry_g.grid(row=5, column=1)

tk.Label(frame, text="Specific Impulse (Isp):").grid(row=6, column=0, sticky="w")
entry_isp = tk.Entry(frame)
entry_isp.insert(0, str(constants.Isp))
entry_isp.grid(row=6, column=1)

tk.Label(frame, text="Propellant Density:").grid(row=7, column=0, sticky="w")
entry_rho_prop = tk.Entry(frame)
entry_rho_prop.insert(0, str(constants.rho_prop))
entry_rho_prop.grid(row=7, column=1)

tk.Label(frame, text="Wall Density:").grid(row=8, column=0, sticky="w")
entry_rho_wall = tk.Entry(frame)
entry_rho_wall.insert(0, str(constants.rho_wall))
entry_rho_wall.grid(row=8, column=1)

tk.Label(frame, text="Bulkhead Density:").grid(row=9, column=0, sticky="w")
entry_rho_bulkhead = tk.Entry(frame)
entry_rho_bulkhead.insert(0, str(constants.rho_bulkhead))
entry_rho_bulkhead.grid(row=9, column=1)

tk.Label(frame, text="Propellant Diameter:").grid(row=10, column=0, sticky="w")
entry_d_prop = tk.Entry(frame)
entry_d_prop.insert(0, str(constants.d_prop))
entry_d_prop.grid(row=10, column=1)

tk.Label(frame, text="Total Diameter:").grid(row=11, column=0, sticky="w")
entry_d_total = tk.Entry(frame)
entry_d_total.insert(0, str(constants.d_total))
entry_d_total.grid(row=11, column=1)

tk.Label(frame, text="Bulkhead Length:").grid(row=12, column=0, sticky="w")
entry_L_bulkhead = tk.Entry(frame)
entry_L_bulkhead.insert(0, str(constants.L_bulkhead))
entry_L_bulkhead.grid(row=12, column=1)

tk.Label(frame, text="Payload Mass:").grid(row=13, column=0, sticky="w")
entry_m_payload = tk.Entry(frame)
entry_m_payload.insert(0, str(constants.m_payload))
entry_m_payload.grid(row=13, column=1)

tk.Button(frame, text="Run Optimization", command=run_algorithm).grid(row=3, columnspan=2, pady=10)

result_text = tk.StringVar()
tk.Label(frame, textvariable=result_text, justify="left", fg="darkblue").grid(row=4, columnspan=2, sticky="w")

graph_frame = tk.Frame(root, padx=20, pady=20)
graph_frame.pack()

root.mainloop()