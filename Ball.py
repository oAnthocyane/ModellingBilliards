from math import *


class Ball:
    def __init__(self, x, y, r, m, vx, vy, step_t=0.001):
        self.x = x # coordinate x
        self.y = y # coordinate y
        self.r = r # radius
        self.m = m # mass
        self.vx = vx # velocity for x
        self.vy = vy # velocity for y
        self.v = 0 # velocity
        self.ax = 0
        self.ay = 0
        self.step_t = step_t # step time
        self.calculate_velocity()

    def calculate_velocity(self):
        self.v = (self.vx ** 2 + self.vy ** 2) ** 0.5

    def calculate_velocity_and_acceleration_with_alpha(self, alpha):
        self.vx, self.vy = cos(alpha) * self.vx - sin(alpha) * self.vy, sin(alpha) * self.vx + cos(alpha) * self.vy
        self.ax, self.ay = cos(alpha) * self.ax - sin(alpha) * self.ay, sin(alpha) * self.ax + cos(alpha) * self.ay

    def calculate_velocity_with_acceleration(self):
        self.vx, self.x = self.vx + self.ax * self.step_t, self.x + self.vx * self.step_t + self.ax * pow(self.step_t, 2) / 2
        self.vy, self.y = self.vy + self.ay * self.step_t, self.y + self.vy * self.step_t + self.ay * pow(self.step_t, 2) / 2

    def check_and_move_on_table(self, length_table, width_table):
        if self.x <= self.r:
            self.x = self.r
            self.vx *= -1
            self.ax *= -1
        if self.x >= length_table - self.r:
            self.x = length_table - self.r
            self.vx *= -1
            self.ax *= -1
        if self.y <= self.r:
            self.y = self.r
            self.vy *= -1
            self.ay *= -1
        if self.y >= width_table - self.r:
            self.y = width_table - self.r
            self.vy *= -1
            self.ay *= -1



