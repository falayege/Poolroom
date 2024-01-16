#TO DO perte énergétique quand collision entre les balles
#rajouter la balle blanche à la fin de chaque visualisation
import math
import random
import matplotlib.pyplot as plt
from Ball import Ball
from Pool import Pool
from matplotlib.animation import FuncAnimation
import matplotlib.cm as cm
from visual import visualize_pool
from matplotlib.widgets import Slider

if __name__ == '__main__':

    #VARIABLES POOL
    pool_x, pool_y = 1.5, 2.8 #pool size
    friction = 1 #friction coeff of the pool
    friction_edge = .7 #between 0 and 1
    radius_hole = .08 #radius for the holes

    #VARIABLES BALLS
    nb_balls = 2 #the black and white are in supplement
    radius = .05 #radius of the balls
    magnus_cst = .1 #constant for the spin (Magnus effect)

    #STEP
    dt = 0.0015

    #Initialization
    vx_0 = random.randint(-100,100) #initialization of the speed for the white ball
    vy_0 = random.randint(-100,100) 
    nb_balls_added = 0

    #Construction of the poolroom
    pool = Pool(pool_x,pool_y, friction,friction_edge,radius) #size of a billard pool
    pool.add_usual_holes(radius_hole)
    pool.add_white_black_balls(radius,magnus_cst)

    #Insure to add the right number of balls (white and black not counted)
    while nb_balls_added<nb_balls:
        nb_balls_added+=pool.add_rand_ball(radius,magnus_cst)

    # White in motion
    white_ball = pool.balls[0]
    white_ball.vx = vx_0
    white_ball.vy = vy_0
    pool.balls_in_motion = [white_ball]

    # Observe the evolution of the pool until no ball is moving
    while pool.balls_in_motion:
        visualize_pool(pool,nb_balls,dt)
    print("End of the game!")