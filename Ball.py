import math
import random
import matplotlib.colors as mcolors
import numpy as np

class Ball:
    """
    The class Ball represents a ball on a poolroom
    A ball in defined by its position and speed in 2D
    """
    def __init__(self, x, y, radius, magnus_cst, vx=0, vy=0,color=None,omega=0):
        """Initialization of a ball with its position and speed."""
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx
        self.vy = vy
        self.magnus_cst = magnus_cst
        self.omega = omega  # Angular velocity
        self.grid_cel = None
        self.marker_angle = 0 #initial angle of the marker
        if color is None:
            self.color = mcolors.hsv_to_rgb([np.random.rand(), 1, 1])
        else:
            self.color = color

        
    def move(self, dt):
        """Move the ball during an interval dt"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        #spin 
        magnus_effect = self.magnus_cst * self.omega
        self.vx += magnus_effect * self.vy * dt
        self.vy -= magnus_effect * self.vx * dt

    def speed(self):
        return math.sqrt(self.vx**2 + self.vy**2)

    def rebound(self, normal_x, normal_y,friction_edge):
        """Rebound of the ball"""
        dot = self.vx * normal_x + self.vy * normal_y
        self.vx -= 2 * dot * normal_x
        self.vx *= friction_edge
        self.vy -= 2 * dot * normal_y
        self.vy *= friction_edge

    def collide(self, other):
        """Handle collision with another ball."""
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        overlap = self.radius + other.radius - distance

        threshold = 0.005  # Smaller than the decalage in overlap
        if distance >= self.radius + other.radius + threshold:
            return
        
        nx = dx / distance
        ny = dy / distance
        tx = -ny
        ty = nx

        # Separate the overlapping balls
        correction = (overlap+threshold) / 2.0  # Each ball will be moved away by half of the overlap to separate them
        self.x -= correction * nx
        self.y -= correction * ny
        other.x += correction * nx
        other.y += correction * ny

        v1n = self.vx * nx + self.vy * ny
        v1t = self.vx * tx + self.vy * ty
        v2n = other.vx * nx + other.vy * ny
        v2t = other.vx * tx + other.vy * ty
        v1n_after = ((self.radius - other.radius) / (self.radius + other.radius)) * v1n + (2 * other.radius / (self.radius + other.radius)) * v2n
        v2n_after = (2 * self.radius / (self.radius + other.radius)) * v1n + ((other.radius - self.radius) / (self.radius + other.radius)) * v2n
        self.vx = v1t * tx + v1n_after * nx
        self.vy = v1t * ty + v1n_after * ny
        other.vx = v2t * tx + v2n_after * nx
        other.vy = v2t * ty + v2n_after * ny

        # Calculate the change in spin due to collision
        tangential_velocity_self = -self.omega * self.radius
        tangential_velocity_other = other.omega * other.radius
        relative_tangential_velocity = tangential_velocity_self + tangential_velocity_other

        # Assuming a simple model where the spin change is proportional to the relative tangential velocity
        spin_change_self = relative_tangential_velocity / self.radius
        spin_change_other = -relative_tangential_velocity / other.radius

        self.omega += spin_change_self
        other.omega += spin_change_other