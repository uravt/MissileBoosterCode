from physics import PhysicsEngine


class Simulator:
    def __init__(self, time_step, total_simulation_time):
        self.time_step = time_step  # in seconds
        self.total_simulation_time = total_simulation_time  # in seconds
        self.engine = PhysicsEngine(time_step)

    def run_simulation(self):
        current_time = 0
        while current_time < self.total_simulation_time:
            current_time += self.time_step
            self.engine.iterate()

    def set_initial_conditions(self, position=0, velocity=0, gravity=-9.8):
        self.engine.position = position
        self.engine.velocity = velocity
        self.engine.gravity = gravity

    def get_position(self):
        return self.engine.position
