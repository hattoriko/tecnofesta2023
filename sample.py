import tkinter as tk
import math

# ゲームウィンドウの作成
window = tk.Tk()
window.title("2Dシューティングゲーム")

# ゲームウィンドウのサイズ
window.geometry("800x600")

# メインのゲームキャンバス
canvas = tk.Canvas(window, width=800, height=600)
canvas.pack()



# ロケットの初期位置
rocket_x = 400
rocket_y = 300

# ロケットのグラフィック
rocket = canvas.create_rectangle(rocket_x - 20, rocket_y - 20, rocket_x + 20, rocket_y + 20, fill="blue")

# キーボードの入力を受け付けるための関数
def move_rocket(event):
    global rocket_x
    if event.keysym == "Left" and rocket_x > 20:
        rocket_x -= 10
    elif event.keysym == "Right" and rocket_x < 780:
        rocket_x += 10
    canvas.coords(rocket, rocket_x - 20, rocket_y - 20, rocket_x + 20, rocket_y + 20)

# キーボードの入力をウィンドウにバインド
# bind() でキーボード押下などのイベントを取得
window.bind("<Left>", move_rocket)
window.bind("<Right>", move_rocket)

# デブリの初期位置
debris_x = 0
debris_y = 100

# デブリのグラフィック
debris = canvas.create_rectangle(debris_x - 20, debris_y - 20, debris_x + 20, debris_y + 20, fill="red")

# デブリの速度
debris_speed = 5

# ゲームループ内でデブリをアニメーションさせる関数
def animate_debris():
    global debris_x

    # デブリを左から右に移動
    debris_x += debris_speed
    canvas.coords(debris, debris_x - 20, debris_y - 20, debris_x + 20, debris_y + 20)

    # デブリが画面外に出た場合、再利用
    if debris_x > 800:
        debris_x = 0

    # ゲームループでこの関数を再帰的に呼び出す
    window.after(30, animate_debris)

# ゲームループ内でデブリのアニメーションを開始
animate_debris()

# ------------------------------------------------------------------------------------------
# ミサイルの動きについて
# ------------------------------------------------------------------------------------------

# ミサイルの初期位置
missile_pos_x = rocket_x  # ロケットの位置から発射
missile_pos_y = rocket_y
missile_vel_x = -10
missile_vel_y = 10
missile_first_pos_x = rocket_x
missile_fisrt_pos_y = rocket_y

# ゲームループ内でミサイルのアニメーションを開始
missile_animation_id = None  # ミサイルアニメーションのIDを保持

# ミサイルのグラフィック
#missile = canvas.create_oval(missile_pos_x - 5, missile_pos_y - 5, missile_pos_x + 5, missile_pos_y + 5, fill="green")
missile_img = tk.PhotoImage(file="missile.png")
missile = canvas.create_image(missile_pos_x,missile_pos_y,image=missile_img)
# 重力定数 
mu_scl = 3.986E+16;
# 軌道半径 [m]
R_scl = 7.3E+6;
# 角速度 [rad/s]
Omega_scl = math.sqrt(mu_scl/R_scl/R_scl/R_scl)

# ヒルの方程式に基づいてミサイルの加速度を計算
def calculate_acceleration(position, velocity):
    ax = 2.0 * Omega_scl * velocity[1]
    ay = -2.0 * Omega_scl * velocity[0] + 3.0 * Omega_scl * Omega_scl * position[1]
    return [ax, ay]

# ルンゲクッタ法で次のステップの位置と速度を計算
def runge_kutta(h, position, velocity):
    k1v = calculate_acceleration(position, velocity)
    k1p = velocity
    k2v = calculate_acceleration([p + 0.5 * v  for p, v in zip(position, k1p)], [v + 0.5 * a  for v, a in zip(velocity, k1v)])
    k2p = [v + 0.5 * a for v, a in zip(velocity, k1v)]
    k3v = calculate_acceleration([p + 0.5 * v  for p, v in zip(position, k2p)], [v + 0.5 * a  for v, a in zip(velocity, k2v)])
    k3p = [v + 0.5 * a for v, a in zip(velocity, k2v)]
    k4v = calculate_acceleration([p + v for p, v in zip(position, k3p)], [v + a  for v, a in zip(velocity, k3v)])
    k4p = [v + a for v, a in zip(velocity, k3v)]

    new_position = [p + (h / 6) * (k1 + 2*k2 + 2*k3 + k4) for p, k1, k2, k3, k4 in zip(position, k1p, k2p, k3p, k4p)]
    new_velocity = [v + (h / 6) * (k1 + 2*k2 + 2*k3 + k4) for v, k1, k2, k3, k4 in zip(velocity, k1v, k2v, k3v, k4v)]

    return new_position, new_velocity

# ルンゲクッタ法でミサイルの軌道を計算
def calculate_missile_trajectory():
    global missile_pos_x, missile_pos_y, missile_vel_x, missile_vel_y
    # ルンゲクッタ法のステップ幅
    h = 0.1
    # ルンゲクッタ法を使用して次のステップの位置と速度を計算
    [missile_pos_x, missile_pos_y], [missile_vel_x, missile_vel_y] = runge_kutta(h, [missile_pos_x,missile_pos_y], [missile_vel_x, missile_vel_y])

# スペースキーを押したときにミサイルを発射する関数
def fire_missile():
    global missile_pos_x, missile_pos_y, missile_vel_x, missile_vel_y
    missile_pos_x = rocket_x
    missile_pos_y = rocket_y
    missile_vel_x = 10
    missile_vel_y = -10  # ミサイルを上に向かって発射

def animate_missile():
    global missile_pos_x, missile_pos_y, missile_animation_id
    calculate_missile_trajectory()
    canvas.coords(missile, missile_pos_x /5 + 400, missile_pos_y /5   +300)

    if missile_pos_x < 0 or missile_pos_x > 800 or missile_pos_y < 0 or missile_pos_y > 600:
        fire_missile()
        stop_missile_animation()
    else:
        missile_animation_id = window.after(1, animate_missile)

# スペースキーを押すとミサイルを発射
def on_space_key(event):
    global missile_first_pos_x, missile_fisrt_pos_y
    if event.keysym == "space":
        fire_missile()  # スペースキーを押したらミサイル発射
        animate_missile()

# ミサイルアニメーションを停止
def stop_missile_animation():
    global missile_animation_id
    if missile_animation_id is not None:
        window.after_cancel(missile_animation_id)
        missile_animation_id = None

# スペースキーの入力をウィンドウにバインド
window.bind("<space>", on_space_key)

# ゲームループの開始
window.mainloop()