#!/usr/bin/env python3

#TO DO perte énergétique quand collision entre les balles
#rajouter la balle blanche à la fin de chaque visualisation
#plus interactif comme jeu : interface etc

import math
import random
import matplotlib.pyplot as plt
from Ball import Ball
from Pool import Pool
from matplotlib.animation import FuncAnimation
import matplotlib.cm as cm
from visual import visualize_pool

if __name__ == '__main__':
    plt.ion() #plt on to be able to close the window

    #VARIABLES POOL
    pool_x, pool_y = 1.5, 2.8
    friction = 10
    friction_edge = .7 #between 0 and 1
    radius_hole = .08

    #VARIABLES BALLS
    nb_balls = 5 #the black and white are in supplement
    radius = .05
    vx_0 = 4
    vy_0 = 44
    nb_balls_added = 0

    step = 0.002

    #Construction of the poolroom
    pool = Pool(pool_x,pool_y, friction,friction_edge) #size of a billard pool
    pool.add_usual_holes(radius_hole)
    pool.add_white_black_balls(radius)

    #Insure to add the right number of balls (white and black not counted)
    while nb_balls_added<nb_balls:
        nb_balls_added+=pool.add_rand_ball(radius)

    # White in motion
    ball = pool.balls[0]
    ball.vx = vx_0
    ball.vy = vy_0
    pool.balls_in_motion = [ball]

    # Observe the evolution of the pool until no ball is moving
    while pool.balls_in_motion:
        pool.step(0.002)  # Assuming a very small dt
        visualize_pool(pool,nb_balls)
        user_input = input("To modify the white ball's speed, enter a float (speed vx) otherwise type 'no' \n New vx speed: ")
        if user_input.lower() == 'no':
            break  # Exit the loop if the user doesn't want to continue


        new_vx = float(user_input.lower())
        new_vy = float(input("New vy speed: "))

        # Update the white ball speed
        pool.balls[0].vx = new_vx
        pool.balls[0].vy = new_vy

        # Add it to the ball in motion
        pool.balls_in_motion.append(pool.balls[0])
    print("End of simulation")