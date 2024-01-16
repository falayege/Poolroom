import math 
from Ball import Ball
from Hole import Hole
import matplotlib.pyplot as plt
import random
import math

class Pool:
    def __init__(self, width, height, friction, friction_edge,rad):
        """Initialisation of the board with its size and friction coefficient"""
        self.width = width
        self.height = height
        self.friction = friction
        self.friction_edge = friction_edge
        self.balls = []
        self.balls_in_motion = []
        self.holes = []
        self.white_ball = None
        self.hide_white_ball = False
        self.a_f= 9.81 * self.friction
        self.speed_stop = 0.2
        self.rho = 0.4
        self.C_d = 1.2

        #for grid method
        self.grid_size = 2 * rad  # Assuming 'radius' is the radius of the largest ball
        self.grid = {} 


    def add_ball(self, ball: Ball) -> bool:
        """
        Add a ball to the board. 
        Returns True if the ball is added successfully, otherwise returns False.
        """
        # Check boundaries
        if (ball.x - ball.radius < 0 or ball.x + ball.radius > self.width or
            ball.y - ball.radius < 0 or ball.y + ball.radius > self.height):
            return False

        # Check for overlap with existing balls
        for existing_ball in self.balls:
            dx = existing_ball.x - ball.x
            dy = existing_ball.y - ball.y
            distance = math.sqrt(dx**2 + dy**2)

            # If distance between centers is less than the sum of the radii, they overlap
            if distance < existing_ball.radius + ball.radius:
                return False
        if self.ball_in_hole(ball):
            return False
        self.balls.append(ball)
        if ball.speed()>0:
            self.balls_in_motion.append(ball)
        # Update the grid with the new ball
        self.add_ball_to_grid(ball)
        return True
    
    def add_ball_to_grid(self, ball: Ball):
        """
        Add ball to grid
        """
        grid_row = int(ball.y / self.grid_size)
        grid_col = int(ball.x / self.grid_size)
        grid_key = (grid_row, grid_col)
        if grid_key not in self.grid:
            self.grid[grid_key] = []
        self.grid[grid_key].append(ball)
        ball.grid_cell = grid_key

    def remove_ball_from_grid(self, ball: Ball):
        if ball.grid_cell in self.grid and ball in self.grid[ball.grid_cell]:
            self.grid[ball.grid_cell].remove(ball)

    def add_rand_ball(self,radius,magnus_cst,color=None)->bool:
        """
        Add a ball generated randomly
        If the ball can be added to the board, it's added and the method return True
        """
        x = random.uniform(radius, self.width-radius)
        y = random.uniform(radius, self.height-radius)
        ball = Ball(x, y, radius,magnus_cst,0,0,color) 
        return(self.add_ball(ball))
    
    def add_white_black_balls(self,radius,magnus_cst):
        """
        Add the two balls of pool the black and the white
        """
        while not(self.add_rand_ball(radius,magnus_cst,'white')):
            pass
        self.balls[0].omega = 100
        self.white_ball = self.balls[0]
        while not(self.add_rand_ball(radius,magnus_cst,'black')):
            pass


    def remove_ball(self, ball: Ball):
        "Remove a ball"
        ball.vx = 0
        ball.vy = 0
        if ball in self.balls:
            if ball is self.white_ball:  # If the removed ball is the white ball
                self.hide_white_ball = True
                # Display a banner for the white ball
                plt.gcf().text(0.5, 0.5, 'White ball potted!', 
                            horizontalalignment='center', verticalalignment='center', 
                            fontsize=14, color='white', bbox=dict(facecolor='red', alpha=0.8))
                plt.pause(1)  # Display the message for 1 second
                plt.gcf().texts.clear()  # Clear the text
                plt.draw()  # Redraw the current figure to update the display
            self.remove_ball_from_grid(ball)
            self.balls.remove(ball)
        if ball in self.balls_in_motion:
            self.balls_in_motion.remove(ball)

    def add_hole(self,hole: Hole):
        """Add a hole to the board"""
        self.holes.append(hole)

    def add_usual_holes(self,radius):
        """Add the 6 usual holes of a billard board, the radius of the hole is given"""
        # Corner holes
        eps=radius/3 #to make them reachable
        self.holes.append(Hole(eps, eps, radius))         # Up Left
        self.holes.append(Hole(self.width-eps, eps, radius))      # Up Right
        self.holes.append(Hole(eps, self.height-eps, radius))     # Down Left
        self.holes.append(Hole(self.width-eps, self.height-eps, radius))  # Down Right

        # Middle holes
        self.holes.append(Hole(0, self.height / 2, radius))       # Middle Left
        self.holes.append(Hole(self.width, self.height / 2, radius))   # Middle Right
    
    def ball_in_hole(self,ball:Ball)->bool:
        "chek if a ball is in a hole"
        for hole in self.holes:
            dx = hole.x - ball.x
            dy = hole.y - ball.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance < ball.radius/4+hole.radius: #consider that it falls into the hole
                return True
        return False

    def all_balls_stopped(self):
        """Check if all balls have come to a stop."""
        for ball in self.balls:
            if ball.speed() > 0.2:  # Using the threshold you've defined for "stopped" 
                return False
        return True
    
    def check_collisions(self, ball: Ball):
        """Check collisions for a given ball with balls in adjacent cells and in self cell"""
        grid_row, grid_col = ball.grid_cell
        for row in range(grid_row - 1, grid_row + 2):
            for col in range(grid_col - 1, grid_col + 2):
                neighbor_key = (row, col)
                if neighbor_key in self.grid:
                    for other_ball in self.grid[neighbor_key]:
                        if ball != other_ball:
                            ball.collide(other_ball)

    def get_adjacent_cells_to_motion(self):
        adjacent_cells = set()
        for ball in self.balls_in_motion:
            grid_row, grid_col = ball.grid_cell
            for row in range(grid_row - 1, grid_row + 2):
                for col in range(grid_col - 1, grid_col + 2):
                    adjacent_cells.add((row, col))
        return adjacent_cells

    def step(self, dt):
        """Update of the position of the balls  and thier speed during a dt interval"""
        update_balls_in_motion = set()  # Using a set to ensure uniqueness

        for ball in self.balls_in_motion:
            self.remove_ball_from_grid(ball)
            #ball.omega=0
            if self.ball_in_hole(ball):
                if isinstance(ball.color,str):
                    if ball.color == 'black':
                        # Instead of printing to the console and exiting, display a message on the plot
                        plt.text(self.width / 2, self.height / 2, 'Game Over! Black ball fell into a hole.', 
                                horizontalalignment='center', verticalalignment='center', 
                                fontsize=14, bbox=dict(facecolor='red', alpha=0.5))
                        plt.pause(2)  # Pause to display the message before closing
                        plt.close()
                        print("Game Lost! Black ball fell into a hole.")
                        exit()
                    elif ball.color == 'white':
                        ball.x = random.uniform(ball.radius, self.width - ball.radius)  # Reset position
                        ball.y = random.uniform(ball.radius, self.height - ball.radius)
                        ball.vx = 0  # Reset velocity
                        ball.vy = 0
                        self.remove_ball(ball)  # Remove the white ball from the game
                    continue
                else:
                    self.remove_ball(ball)
                    continue
            ball.move(dt)
            self.add_ball_to_grid(ball)
            self.check_collisions(ball)

            # Friction pool
            theta = math.atan2(ball.vy, ball.vx)
            ball.vx -= self.a_f * dt * math.cos(theta)
            ball.vy -= self.a_f * dt * math.sin(theta)
            # Friction air 
            v = ball.speed()
            drag_force_magnitude = 0.5 * self.C_d * self.rho * math.pi * (ball.radius ** 2) * (v ** 2)
            drag_force_x = drag_force_magnitude * (ball.vx / v)
            drag_force_y = drag_force_magnitude * (ball.vy / v)
            ball.vx -= drag_force_x * dt
            ball.vy -= drag_force_y * dt

            # If ball is still moving, add to the list of balls in motion
            if ball.speed() > self.speed_stop:  # Consider a threshold for "stopped"
                update_balls_in_motion.add(ball)

            # Rebound taking into account the ball's radius
            if ball.x - ball.radius < 0:
                ball.x = ball.radius
                ball.rebound(1, 0,self.friction_edge)
            elif ball.x + ball.radius > self.width:
                ball.x = self.width - ball.radius
                ball.rebound(-1, 0,self.friction_edge)

            if ball.y - ball.radius < 0:
                ball.y = ball.radius
                ball.rebound(0, 1,self.friction_edge)
            elif ball.y + ball.radius > self.height:
                ball.y = self.height - ball.radius
                ball.rebound(0, -1,self.friction_edge)

        # Adding the balls in motion to the list
        for ball in self.balls:
            if ball.speed() > self.speed_stop: 
                update_balls_in_motion.add(ball)
            
        # Update the list of balls in motion
        self.balls_in_motion = list(update_balls_in_motion)

        if self.all_balls_stopped():
        #If the white ball should be added back into the game - once fallen in a hole
            if self.hide_white_ball:
                self.balls.insert(0,self.white_ball) #insert the white ball at its position
                self.hide_white_ball = False
                self.balls_in_motion.append(self.white_ball)
                self.add_ball_to_grid(self.white_ball)
