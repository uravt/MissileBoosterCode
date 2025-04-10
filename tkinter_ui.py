import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from rocket_optimizer import genetic_algorithm, fitness_function  # Your main code should be saved as rocket_optimizer.py

def run_algorithm():
    try:
        rocket_length = float(entry_length.get())
        if rocket_length <= 0:
            raise ValueError

        # Parameters for GA
        population_size = 100
        lower_bound = 0
        upper_bound = rocket_length
        generations = 50
        mutation_rate = 0.5

        best_solution = genetic_algorithm(population_size, lower_bound, upper_bound, generations, mutation_rate, rocket_length)
        delta_v = fitness_function(best_solution, rocket_length)

        
        result_text.set(f"Best Solution:\nL1 = {best_solution[0]:.2f} m\n"
                        f"L2 = {best_solution[1]:.2f} m\n"
                        f"L3 = {best_solution[2]:.2f} m\n"
                        f"Delta V = {delta_v:.2f} m/s")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a positive numeric value for rocket length.")

# UI Setup
root = tk.Tk()
root.title("Rocket Stage Optimizer")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

tk.Label(frame, text="Enter Total Rocket Length (m):").grid(row=0, column=0, sticky="w")
entry_length = tk.Entry(frame)
entry_length.grid(row=0, column=1)

tk.Button(frame, text="Run Optimization", command=run_algorithm).grid(row=1, columnspan=2, pady=10)

result_text = tk.StringVar()
tk.Label(frame, textvariable=result_text, justify="left", fg="darkblue").grid(row=2, columnspan=2, sticky="w")

root.mainloop()