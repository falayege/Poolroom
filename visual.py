#!/usr/bin/env python3

import math
import random
import matplotlib.pyplot as plt
from Ball import Ball
from Pool import Pool
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors
import numpy as np
import matplotlib.patches as patches

def visualize_pool(pool,nb_balls):
    """
    Allow the visual representation of the pool
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, pool.width)
    ax.set_ylim(0, pool.height)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')
    ax.add_patch(plt.Rectangle((0, 0), pool.width, pool.height, linewidth=2, edgecolor='brown', facecolor='darkgreen'))
   
    # Drawing holes
    for hole in pool.holes:
        hole_circle = patches.Circle((hole.x, hole.y), hole.radius, fc='black')  # 'fc' stands for fill color
        plt.gca().add_patch(hole_circle)


    # Initialize ball_to_circle dictionary
    ball_to_circle = {ball: plt.Circle((ball.x, ball.y), ball.radius, fc=ball.color) for ball in pool.balls}
    for circle in ball_to_circle.values():
        ax.add_patch(circle)

    def update(frame):
        pool.step(0.002)

        # Update positions of balls that are still on the pool
        for ball in pool.balls:
            circle = ball_to_circle.get(ball, None)
            if circle:
                circle.center = (ball.x, ball.y)
            else:  # New ball
                circle = plt.Circle((ball.x, ball.y), ball.radius, fc=ball.color)
                ax.add_patch(circle)
                ball_to_circle[ball] = circle

        # Handle balls that have fallen into holes
        balls_on_pool = set(pool.balls)
        for ball in list(ball_to_circle.keys()):
            if ball not in balls_on_pool:  # Ball has been removed
                ball_to_circle[ball].remove()
                del ball_to_circle[ball]

        return ball_to_circle.values()

    ani=FuncAnimation(fig, update, frames=range(200), blit=True, interval=50)  # Assuming 200 frames for illustration; adjust as needed
    plt.draw()

    # Closing the window only when the balls are all stopped
    while not pool.all_balls_stopped():
        plt.pause(1)
    plt.close()