import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

missile_pos_x = 0
missile_pos_y = 0
missile_vel_x = -10
missile_vel_y = 10

# 重力定数 
mu_scl = 3.986E+14
R_scl = 6.8E+6
Omega_scl = math.sqrt(mu_scl / R_scl / R_scl / R_scl)

def calculate_acceleration(position, velocity):
    ax = 2.0 * Omega_scl * velocity[1]
    ay = -2.0 * Omega_scl * velocity[0] + 3.0 * Omega_scl * Omega_scl * position[1]
    return [ax, ay]

def runge_kutta(h, position, velocity):
    k1v = calculate_acceleration(position, velocity)
    k1p = velocity
    k2v = calculate_acceleration([p + 0.5 * v for p, v in zip(position, k1p)], [v + 0.5 * a for v, a in zip(velocity, k1v)])
    k2p = [v + 0.5 * a for v, a in zip(velocity, k1v)]
    k3v = calculate_acceleration([p + 0.5 * v for p, v in zip(position, k2p)], [v + 0.5 * a for v, a in zip(velocity, k2v)])
    k3p = [v + 0.5 * a for v, a in zip(velocity, k2v)]
    k4v = calculate_acceleration([p + v for p, v in zip(position, k3p)], [v + a for v, a in zip(velocity, k3v)])
    k4p = [v + a for v, a in zip(velocity, k3v)]

    new_position = [p + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4) for p, k1, k2, k3, k4 in zip(position, k1p, k2p, k3p, k4p)]
    new_velocity = [v + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4) for v, k1, k2, k3, k4 in zip(velocity, k1v, k2v, k3v, k4v)]

    return new_position, new_velocity

def calculate_missile_trajectory():
    global missile_pos_x, missile_pos_y, missile_vel_x, missile_vel_y
    h = 0.1
    [missile_pos_x, missile_pos_y], [missile_vel_x, missile_vel_y] = runge_kutta(h, [missile_pos_x, missile_pos_y], [missile_vel_x, missile_vel_y])

# アニメーション用のフレームを初期化
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    return line,

def animate(i):
    calculate_missile_trajectory()
    x_data.append(missile_pos_x)
    y_data.append(missile_pos_y)
    line.set_data(x_data, y_data)
    return line,

# アニメーションを作成
ani = FuncAnimation(fig, animate, init_func=init, frames=1000, interval=0.01, blit=True)

# プロットの設定
plt.xlim(-50000, 50000)
plt.ylim(-50000, 50000)
plt.xlabel('X座標')
plt.ylabel('Y座標')
plt.title('Missile Trajectory Animation')

# アニメーションを表示
plt.show()
