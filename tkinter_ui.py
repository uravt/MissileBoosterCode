import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import rocket_optimizer
import constrained_algorithm
import new_pop_off_booster_length
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
        
        constants.v_exhaust = constants.Isp * constants.g
        constants.m_bulkhead = (np.pi / 4) * (constants.d_total ** 2) * (constants.L_bulkhead) * (constants.rho_bulkhead)

        rocket_length = float(entry_length.get()) - 3 * constants.L_bulkhead
        if rocket_length <= 0:
            raise ValueError

        try:
            population_size = int(entry_population.get()) if entry_population.get() else 100
            if population_size <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Population size must be a positive integer.")
            return

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

        rocket_optimizer.rocket_length = rocket_length
        constrained_algorithm.rocket_length = rocket_length
        constrained_algorithm.L1 = new_pop_off_booster_length.compute_L1(burn_time=10, length_total=rocket_length)

        best_solution_opt, figures_opt = rocket_optimizer.genetic_algorithm(
            population_size, lower_bound, upper_bound, generations, mutation_rate, rocket_length
        )

        best_solution_constrained, figures_constrained = constrained_algorithm.genetic_algorithm_fixed_L1(
            population_size, lower_bound, upper_bound, generations, mutation_rate, rocket_length
        )

        delta_v_opt = rocket_optimizer.fitness_function(best_solution_opt, rocket_length)
        delta_v_constrained = constrained_algorithm.fitness_function_fixed_L1(best_solution_constrained, constrained_algorithm.L1, rocket_length)

        result_text.set(f"Best Solution (Unconstrained):\nL1 = {best_solution_opt[0]:.2f} m\n"
                        f"L2 = {best_solution_opt[1]:.2f} m\n"
                        f"L3 = {best_solution_opt[2]:.2f} m\n"
                        f"Delta V = {delta_v_opt:.2f} m/s\n\n"
                        f"Best Solution (Constrained):\nL1 = {constrained_algorithm.L1:.2f} m\n"
                        f"L2 = {best_solution_constrained[0]:.2f} m\n"
                        f"L3 = {best_solution_constrained[1]:.2f} m\n"
                        f"Delta V = {delta_v_constrained:.2f} m/s")

        # Clear old graphs
        for widget in graph_frame.winfo_children():
            widget.destroy()

        # Extract plots
        fig_opt, fig_lengths_opt, fig_fitness_opt = figures_opt
        fig_constrained, fig_lengths_constrained, fig_fitness_constrained = figures_constrained

        # Two labeled subframes for clarity
        unconstrained_frame = tk.LabelFrame(graph_frame, text="Unconstrained", padx=10, pady=10)
        unconstrained_frame.pack(side="left", padx=10)

        constrained_frame = tk.LabelFrame(graph_frame, text="Constrained", padx=10, pady=10)
        constrained_frame.pack(side="left", padx=10)

        # Unconstrained graphs
        FigureCanvasTkAgg(fig_lengths_opt, master=unconstrained_frame).get_tk_widget().pack()
        FigureCanvasTkAgg(fig_fitness_opt, master=unconstrained_frame).get_tk_widget().pack()

        # Constrained graphs
        FigureCanvasTkAgg(fig_lengths_constrained, master=constrained_frame).get_tk_widget().pack()
        FigureCanvasTkAgg(fig_fitness_constrained, master=constrained_frame).get_tk_widget().pack()

        # Plot final stage lengths
        stage_length_fig  = plot_final_stage_lengths(best_solution_opt, best_solution_constrained, constrained_algorithm.L1)
        stage_length_frame = tk.LabelFrame(graph_frame, text="Final Stage Length Comparison", padx=10, pady=10)
        stage_length_frame.pack(pady=10)
        FigureCanvasTkAgg(stage_length_fig, master=stage_length_frame).get_tk_widget().pack()

        # Stacked Rocket Visual
        stacked_fig = plot_stacked_rocket_visual(best_solution_opt, best_solution_constrained, constrained_algorithm.L1, delta_v_opt, delta_v_constrained)
        stacked_frame = tk.LabelFrame(graph_frame, text="Propulstion Stack Breakdown", padx=20, pady=20)
        stacked_frame.pack(pady=10)
        stacked_frame.pack(pady=10)

        # Delta V Comparison Graph
        delta_v_fig = plot_delta_v_comparison(delta_v_opt, delta_v_constrained)
        delta_v_frame = tk.LabelFrame(graph_frame, text="Delta V Comparison", padx=10, pady=10)
        delta_v_frame.pack(pady=10)
        FigureCanvasTkAgg(delta_v_fig, master=delta_v_frame).get_tk_widget().pack()

        FigureCanvasTkAgg(stacked_fig, master=stacked_frame).get_tk_widget().pack()
        

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a positive numeric value for rocket length.")

def create_labeled_entry(label_text, default_value, row):
    tk.Label(frame, text=label_text).grid(row=row, column=0, sticky="w")
    entry = tk.Entry(frame)
    entry.insert(0, str(default_value))
    entry.grid(row=row, column=1)
    return entry

def plot_final_stage_lengths(best_unconstrained, best_constrained, fixed_L1):
    fig, ax = plt.subplots(figsize=(6, 3))

    stages = ['L1', 'L2', 'L3']
    unconstrained = best_unconstrained
    constrained = [fixed_L1, *best_constrained]

    bar_width = 0.35
    x = np.arange(len(stages))

    ax.bar(x - bar_width/2, unconstrained, width=bar_width, label='Multistage', color='steelblue')
    ax.bar(x + bar_width/2, constrained, width=bar_width, label='Pop Off Booster', color='orange')

    ax.set_ylabel('Length (m)')
    ax.set_title('Final Stage Lengths')
    ax.set_xticks(x)
    ax.set_xticklabels(stages)
    ax.legend()

    plt.tight_layout()
    return fig

def plot_stacked_rocket_visual(best_unconstrained, best_constrained, fixed_L1, delta_v_unconstrained, delta_v_constrained):
    fig, ax = plt.subplots(figsize=(6, 7))  # Slightly larger figure for clarity

    # Segment definitions with unique labels to control legend
    unconstrained = [
        ('L1', best_unconstrained[0], 'lightblue'),
        ('Bulkhead', constants.L_bulkhead, 'gray'),
        ('L2_U', best_unconstrained[1], 'dodgerblue'),
        ('Bulkhead', constants.L_bulkhead, 'gray'),
        ('L3_U', best_unconstrained[2], 'royalblue'),
        ('Bulkhead', constants.L_bulkhead, 'gray')
    ]

    constrained = [
        ('Pop Off Booster Stage', fixed_L1, 'moccasin'),
        ('Bulkhead', constants.L_bulkhead, 'gray'),
        ('L2_C', best_constrained[0], 'orange'),
        ('Bulkhead', constants.L_bulkhead, 'gray'),
        ('L3_C', best_constrained[1], 'darkorange'),
        ('Bulkhead', constants.L_bulkhead, 'gray')
    ]

    used_labels = set()
    label_map = {
        'Bulkhead': 'Bulkhead',
        'L1': 'L1',
        'L2_U': 'L2',
        'L3_U': 'L3',
        'Pop Off Booster Stage': 'Pop Off Booster Stage',
        'L2_C': 'L2',
        'L3_C': 'L3'
    }

    # Plot unconstrained rocket
    bottom_u = 0
    for label, height, color in unconstrained:
        plot_label = None
        if label not in used_labels:
            plot_label = label_map[label]
            used_labels.add(label)
        ax.bar(0, height, bottom=bottom_u, color=color, label=plot_label)
        ax.text(0, bottom_u + height / 2, f'{height:.2f} m', ha='center', va='center', fontsize=7, color='black')
        bottom_u += height

    # Plot constrained rocket
    bottom_c = 0
    for label, height, color in constrained:
        plot_label = None
        if label not in used_labels:
            plot_label = label_map[label]
            used_labels.add(label)
        ax.bar(1.5, height, bottom=bottom_c, color=color, label=plot_label)
        ax.text(1.5, bottom_c + height / 2, f'{height:.2f} m', ha='center', va='center', fontsize=7, color='black')
        bottom_c += height

    # Y-axis
    max_height = max(bottom_u, bottom_c)
    ax.set_yticks(np.arange(0, max_height + 0.5, 0.5))

    # Axis and titles
    ax.set_xticks([0, 1.5])
    ax.set_xticklabels(['Multistage', 'Pop Off Booster'], fontsize=10)
    ax.set_ylabel('Lengths (m)', fontsize=11)
    ax.set_title('Propulsion Stack Breakdown', fontsize=12, pad=15)

    # Annotations
    ax.text(0, -0.75, f'Bulkhead = {constants.L_bulkhead:.2f} m', ha='center', fontsize=10)
    ax.text(1.5, -0.75, f'Bulkhead = {constants.L_bulkhead:.2f} m', ha='center', fontsize=10)
    ax.text(0, -1, f'Δv = {delta_v_unconstrained:.2f} m/s', ha='center', fontsize=10)
    ax.text(1.5, -1, f'Δv = {delta_v_constrained:.2f} m/s', ha='center', fontsize=10)

    # Legend order: Bulkhead, L1, L2 (U), L3 (U), Pop-off, L2 (C), L3 (C)
    legend_order = ['Bulkhead', 'L1', 'L2', 'L3', 'Pop Off Booster Stage', 'L2', 'L3']
    handles, labels = ax.get_legend_handles_labels()
    seen = set()
    ordered = []
    for name in legend_order:
        for h, l in zip(handles, labels):
            if l == name and (name, id(h)) not in seen:
                ordered.append((h, l))
                seen.add((name, id(h)))
                break  # Only one occurrence per entry
    handles, labels = zip(*ordered)

    ax.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')
    plt.tight_layout(pad=3)
    return fig

def plot_delta_v_comparison(delta_v_unconstrained, delta_v_constrained):
    fig, ax = plt.subplots(figsize=(5, 4))

    labels = ['Multistage', 'Pop Off Booster']
    delta_vs = [delta_v_unconstrained, delta_v_constrained]
    colors = ['steelblue', 'orange']

    bars = ax.bar(labels, delta_vs, color=colors)

    # Add delta-v value at center of each bar
    for bar, dv in zip(bars, delta_vs):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height / 2,
            f'{dv:.0f} m/s',
            ha='center', va='center',
            color='white', fontsize=10, weight='bold'
        )

    # Calculate and annotate percentage improvement
    loss = (((delta_v_unconstrained - delta_v_constrained) / delta_v_unconstrained) * 100)
    ax.text(
        0.5, max(delta_vs) * 1.05,
        f'{loss:.1f}% Perfomance Loss',
        ha='center', va='bottom',
        fontsize=11, color='red', weight='bold'
    )

    ax.set_ylabel('Delta V (m/s)')
    ax.set_title('Delta V Comparison')
    ax.set_ylim(0, max(delta_vs) * 1.2)
    plt.tight_layout()
    return fig

# ----- Root + Scrollable Canvas Setup -----
root = tk.Tk()
root.title("Rocket Stage Optimizer")

# Create main canvas
main_canvas = tk.Canvas(root, borderwidth=0)

# Scrollbars
v_scrollbar = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
h_scrollbar = tk.Scrollbar(root, orient="horizontal", command=main_canvas.xview)

main_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

# Pack scrollbars and canvas
v_scrollbar.pack(side="right", fill="y")
h_scrollbar.pack(side="bottom", fill="x")
main_canvas.pack(side="left", fill="both", expand=True)

# Frame inside the canvas
container = tk.Frame(main_canvas)
canvas_window = main_canvas.create_window((0, 0), window=container, anchor="nw")

# Update scrollregion when container size changes
def on_configure(event):
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))

container.bind("<Configure>", on_configure)

# Mousewheel for vertical scrolling
def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Horizontal scrolling with Shift + Mousewheel
def _on_shift_mousewheel(event):
    main_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

main_canvas.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)

main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

# ----- Input & Graph Frames -----
frame = tk.Frame(container, padx=20, pady=20)
frame.pack()

graph_frame = tk.Frame(container, padx=20, pady=20)
graph_frame.pack()

# ----- Input Fields -----
tk.Label(frame, text="Total Rocket Length (m):").grid(row=0, column=0, sticky="w")
entry_length = tk.Entry(frame)
entry_length.grid(row=0, column=1)

tk.Label(frame, text="Population Size (default: 100):").grid(row=1, column=0, sticky="w")
entry_population = tk.Entry(frame)
entry_population.grid(row=1, column=1)

tk.Label(frame, text="Generations (default: 20):").grid(row=2, column=0, sticky="w")
entry_generations = tk.Entry(frame)
entry_generations.grid(row=2, column=1)

tk.Button(frame, text="Run Optimization", command=run_algorithm).grid(row=3, columnspan=2, pady=10)

result_text = tk.StringVar()
tk.Label(frame, textvariable=result_text, justify="left", fg="darkblue").grid(row=4, columnspan=2, sticky="w")

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

root.mainloop()