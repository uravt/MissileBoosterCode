import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from rocket_optimizer import genetic_algorithm, fitness_function  # Your main code should be saved as rocket_optimizer.py
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def run_algorithm():
    try:
        rocket_length = float(entry_length.get())
        if rocket_length <= 0:
            raise ValueError

        # Parameters for GA
        population_size = 100
        lower_bound = 0
        upper_bound = rocket_length
        generations = 100
        mutation_rate = 10 / population_size

        # Set the global rocket_length in the imported module
        import rocket_optimizer
        genetic_algorithm.rocket_length = rocket_length

        # Run the genetic algorithm
        best_solution, figures = genetic_algorithm(population_size, lower_bound, upper_bound, generations, mutation_rate, rocket_length)
        delta_v = fitness_function(best_solution, rocket_length)
        
        # Update result text
        result_text.set(f"Best Solution:\nL1 = {best_solution[0]:.2f} m\n"
                        f"L2 = {best_solution[1]:.2f} m\n"
                        f"L3 = {best_solution[2]:.2f} m\n"
                        f"Delta V = {delta_v:.2f} m/s")
        
        # Clear previous graphs
        for widget in graph_frame.winfo_children():
            widget.destroy()

        # Display the graphs in Tkinter window
        fig, fig_lengths, fig_fitness = figures

        # Create canvas for L1, L2, L3 plot
        canvas_lengths = FigureCanvasTkAgg(fig_lengths, master=graph_frame)
        canvas_lengths.get_tk_widget().pack()
        canvas_lengths.draw()

        # Create canvas for delta V plot
        canvas_fitness = FigureCanvasTkAgg(fig_fitness, master=graph_frame)
        canvas_fitness.get_tk_widget().pack()
        canvas_fitness.draw()

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

# Create a frame to hold the graphs
graph_frame = tk.Frame(root, padx=20, pady=20)
graph_frame.pack()

root.mainloop()