from physics import PhysicsEngine


class Simulator:
    def __init__(self, time_step, total_simulation_time):
        self.isp = None
        self.bulkhead_density = None
        self.bulkhead_wall_density = None
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

    def set_inputs(self, isp, bulkhead_density, bulkhead_wall_density):
        self.isp = isp
        self.bulkhead_density = bulkhead_density
        self.bulkhead_wall_density = bulkhead_wall_density

    def get_position(self):
        return self.engine.position
