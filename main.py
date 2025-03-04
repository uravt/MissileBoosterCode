from simulator import Simulator

if __name__ == "__main__":
    simulator = Simulator(0.001, 4)  # run simulation for 4s with a timestep of 0.001s
    simulator.set_initial_conditions(100)  # set position to 100 meters
    simulator.run_simulation()  # run the simulation
    print(simulator.get_position())  # get position after simulation has completed
