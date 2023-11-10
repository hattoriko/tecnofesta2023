import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

missile_pos_x = 0
missile_pos_y = 0
missile_vel_x = 0
missile_vel_y = -10

# 重力定数 
Omega_scl = 2 * math.pi /6
R = 5

def calculate_acceleration(position, velocity):
    ax = 2.0 * Omega_scl * velocity[1] + Omega_scl * Omega_scl * position[0]
    ay = -2.0 * Omega_scl * velocity[0] + Omega_scl * Omega_scl * (position[1] + R)
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

def calculate_missile_trajectory(i):
    global missile_pos_x, missile_pos_y, missile_vel_x, missile_vel_y
    h = 0.01
    [missile_pos_x, missile_pos_y], [missile_vel_x, missile_vel_y] = runge_kutta(h, [missile_pos_x, missile_pos_y],
                                                                                   [missile_vel_x, missile_vel_y])
    print(missile_pos_x, missile_pos_y)

    if i == 200:  # 300フレーム後に停止
        ani.event_source.stop()

# アニメーション用のフレームを初期化
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    return line,

def animate(i):
    calculate_missile_trajectory(i)
    x_data.append(missile_pos_x)
    y_data.append(missile_pos_y)
    line.set_data(x_data, y_data)
    return line,

# アニメーションを作成
ani = FuncAnimation(fig, animate, init_func=init, frames=1000, interval=10, blit=True)

# プロットの設定
plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.xlabel('axis x')
plt.ylabel('axis y')

# アニメーションを表示
plt.show()
