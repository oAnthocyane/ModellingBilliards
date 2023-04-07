from math import *
import matplotlib.pyplot as plt
from Ball import Ball
import writer

def get_distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def scalar_product(x1, y1, x2, y2):
    return x1 * x2 + y1 * y2


def plot_graphics(alpha, data):
    plt.plot(alpha, data[0], 'o-r', label="first", lw=1)
    plt.plot(alpha, data[1], 'o-b', label="second", lw=1)
    plt.plot(alpha, data[2], 'o-g', label="third", lw=1)
    plt.legend()
    plt.grid(True)
    plt.savefig("graphic.png")


SCALE = 500
SCALE_COODS = 100
SCALE_RADIUS = 100
LENGTH_TABLE = 2 * SCALE
WIDTH_TABLE = 2 * SCALE
COORDINATE_LOOSE_X = 1 * SCALE_COODS
COORDINATE_LOOSE_Y = 0.3 * SCALE_COODS
COORDINATE_RED_BALL_X = 1 * SCALE_COODS
COORDINATE_RED_BALL_Y = 0.8 * SCALE_COODS
COORDINATE_GREEN_BALL_X = 1.5 * SCALE_COODS
COORDINATE_GREEN_BALL_Y = 0.8 * SCALE_COODS
RADIUS_LOOSE = 0.2 * SCALE_RADIUS
RADIUS_BALLS = 0.05 * SCALE_RADIUS
MASS_BALLS = 0.3 * SCALE
V0_RED_BALL = 2 * SCALE
FRICTION_COEFFICIENTS = [0.01, 5, 20]

# FRICTION_COEFFICIENTS = [0.01, 0.05, 0.1]

g = 9.82

MAX_ALPHA = 360
ALL_ALPHA = [i for i in range(MAX_ALPHA)]
ALL_ENERGY = [[0] * MAX_ALPHA, [0] * MAX_ALPHA, [0] * MAX_ALPHA]

for i in range(len(FRICTION_COEFFICIENTS)):
    for j in range(MAX_ALPHA):
        print(j)
        red_ball = Ball(COORDINATE_RED_BALL_X, COORDINATE_RED_BALL_Y, RADIUS_BALLS, MASS_BALLS,
                        V0_RED_BALL, 0)
        green_ball = Ball(COORDINATE_GREEN_BALL_X, COORDINATE_GREEN_BALL_Y, RADIUS_BALLS, MASS_BALLS,
                          0, 0)
        alpha = radians(j)
        is_collided = False
        acceleration = round(-g * FRICTION_COEFFICIENTS[i], 4)
        red_ball.ax = acceleration
        red_ball.calculate_velocity_and_acceleration_with_alpha(alpha)
        while round(red_ball.v, 3) > 0 or round(green_ball.v, 3) > 0:
            path_red_ball = "data/coords/red_ball/" + f"mu={i}/alpha={j}/coords.txt"
            path_green_ball = "data/coords/green_ball/" + f"mu={i}/alpha={j}/coords.txt"
            writer.write_to_file(path_red_ball, red_ball.x, red_ball.y)
            writer.write_to_file(path_green_ball, green_ball.x, green_ball.y)
            red_ball.calculate_velocity_with_acceleration()
            green_ball.calculate_velocity_with_acceleration()
            # Check on red ball in loose
            if get_distance(red_ball.x, red_ball.y, COORDINATE_LOOSE_X, COORDINATE_LOOSE_Y) <= RADIUS_LOOSE:
                red_ball.vx = 0
                red_ball.vy = 0
                red_ball.ax = 0
                red_ball.ay = 0
                red_ball.x = -100
                red_ball.y = 0
            # Check on green ball in loose
            if get_distance(green_ball.x, green_ball.y, COORDINATE_LOOSE_X, COORDINATE_LOOSE_Y) <= RADIUS_LOOSE:
                ALL_ENERGY[i][j] = MASS_BALLS * pow(green_ball.v, 2) / 2
                break
            red_ball.check_and_move_on_table(LENGTH_TABLE, WIDTH_TABLE)
            green_ball.check_and_move_on_table(LENGTH_TABLE, WIDTH_TABLE)
            # Check collided both balls
            if get_distance(red_ball.x, red_ball.y, green_ball.x, green_ball.y) <= 2 * RADIUS_BALLS and \
                    (not is_collided):
                is_collided = True
                normal_x = (green_ball.x - red_ball.x) / get_distance(red_ball.x, red_ball.y, green_ball.x,
                                                                      green_ball.y)
                normal_y = (green_ball.y - red_ball.y) / get_distance(red_ball.x, red_ball.y, green_ball.x,
                                                                      green_ball.y)
                if normal_x == 0:
                    normal_transpose_y = 0
                    normal_transpose_x = 1
                else:
                    normal_transpose_y = sqrt(1 / (1 + pow(normal_y, 2) / pow(normal_x, 2)))
                    normal_transpose_x = -1 * normal_transpose_y * normal_y / normal_x
                # Determination of new vector coordinates
                scalar_green_v_normal = scalar_product(green_ball.vx, green_ball.vy, normal_x, normal_y)
                scalar_red_v_transpose = scalar_product(red_ball.vx, red_ball.vy, normal_transpose_x,
                                                        normal_transpose_y)
                scalar_red_v_normal = scalar_product(red_ball.vx, red_ball.vy, normal_x, normal_y)
                scalar_green_v_transpose = scalar_product(green_ball.vx, green_ball.vy, normal_transpose_x,
                                                          normal_transpose_y)
                scalar_green_a_normal = scalar_product(green_ball.ax, green_ball.ay, normal_x, normal_y)
                scalar_red_a_transpose = scalar_product(red_ball.ax, red_ball.ay, normal_transpose_x,
                                                        normal_transpose_y)
                scalar_red_a_normal = scalar_product(red_ball.ax, red_ball.ay, normal_x, normal_y)
                scalar_green_a_transpose = scalar_product(green_ball.ax, green_ball.ay, normal_transpose_x,
                                                          normal_transpose_y)
                red_ball.vx = normal_x * scalar_green_v_normal + normal_transpose_x * scalar_red_v_transpose
                red_ball.vy = normal_y * scalar_green_v_normal + normal_transpose_y * scalar_red_v_transpose
                green_ball.vx = normal_x * scalar_red_v_normal + normal_transpose_x * scalar_green_v_transpose
                green_ball.vy = normal_y * scalar_red_v_normal + normal_transpose_y * scalar_green_v_transpose
                red_ball.ax = normal_x * scalar_green_a_normal + normal_transpose_x * scalar_red_a_transpose
                red_ball.ay = normal_y * scalar_green_a_normal + normal_transpose_y * scalar_red_a_transpose
                green_ball.ax = normal_x * scalar_red_a_normal + normal_transpose_x * scalar_green_a_transpose
                green_ball.ay = normal_y * scalar_red_a_normal + normal_transpose_y * scalar_green_a_transpose
            red_ball.calculate_velocity()
            green_ball.calculate_velocity()


plot_graphics(ALL_ALPHA, ALL_ENERGY)