class PhysicsEngine:
    def __init__(self, time_step, position=0, velocity=0, gravity=-9.8):  # set initial position, velocity
        self.time_step = time_step
        self.position = position
        self.velocity = velocity
        self.acceleration = 0
        self.gravity = gravity

    def calculate_acceleration(self):
        return self.gravity

    def calculate_velocity(self):
        return self.velocity + self.calculate_acceleration() * self.time_step

    def calculate_position(self):
        return self.position + self.velocity * self.time_step

    def iterate(self):
        self.acceleration = self.calculate_acceleration()
        self.velocity = self.calculate_velocity()
        self.position = self.calculate_position()


