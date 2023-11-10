import tkinter as tk
import math

# ゲームウィンドウの作成
window = tk.Tk()
window.title("2Dシューティングゲーム")

# ゲームウィンドウのサイズ
window.geometry("800x600")

# メインのゲームキャンバス
canvas = tk.Canvas(window, width=800, height=600,bg="black")
canvas.pack()

"""
# 背景の設定
img = Image.open("space.png")
img = img.resize((1000, 600))
space_img= ImageTk.PhotoImage(img)
space = canvas.create_image(0, 0,image=space_img, anchor=tk.NW,tag="space")
"""

# flag (space and -> or <-)
flag_input = True

# the earthのグラフィック
earth_img = tk.PhotoImage(file="earth.png").subsample(1,2)
earth = canvas.create_image(400, 700,image=earth_img, tag="earth")

# ロケットの初期位置
rocket_x = 400
rocket_y = 300

missile_vel_x = 60
missile_vel_y = 0
missile_mod_vel_x = 60
missile_mod_vel_y = 0

# ロケットのグラフィック
rocket_img = tk.PhotoImage(file="satellite.png").subsample(3,3)
rocket = canvas.create_image(rocket_x, rocket_y,image=rocket_img, tag="sat")

arrow = canvas.create_line(rocket_x, rocket_y,rocket_x+missile_vel_x,rocket_y+missile_vel_y,arrow=tk.LAST,fill="red", width=5)

# キーボードの入力を受け付けるための関数
def move_rocket(event):
    global rocket_x,missile_vel_x,missile_vel_y
    if event.keysym == "Left" and rocket_x > 20 and flag_input :
        rocket_x -= 10
    elif event.keysym == "Right" and rocket_x < 780 and flag_input:
        rocket_x += 10
    elif event.keysym == "Down" and flag_input:
        missile_vel_x = missile_vel_x*math.cos(2*math.pi * 15 / 360) - math.sin(2*math.pi * 15 / 360)*missile_vel_y
        missile_vel_y = missile_vel_x*math.sin(2*math.pi * 15 / 360) + math.cos(2*math.pi * 15 / 360)*missile_vel_y
    elif event.keysym == "Up" and flag_input:
        missile_vel_x = missile_vel_x*math.cos(-2*math.pi * 15 / 360) - math.sin(-2*math.pi * 15 / 360)*missile_vel_y
        missile_vel_y = missile_vel_x*math.sin(-2*math.pi * 15 / 360) + math.cos(-2*math.pi * 15 / 360)*missile_vel_y
    canvas.coords(rocket, rocket_x ,rocket_y )
    canvas.coords(arrow,rocket_x, rocket_y,rocket_x+missile_vel_x,rocket_y+missile_vel_y)

# キーボードの入力をウィンドウにバインド
# bind() でキーボード押下などのイベントを取得
window.bind("<Left>", move_rocket)
window.bind("<Right>", move_rocket)
window.bind("<Up>", move_rocket)
window.bind("<Down>", move_rocket)

# デブリの初期位置
debris_x = 0
debris_y = 100

# デブリのグラフィック
debris_img = tk.PhotoImage(file="asteroid3.png").subsample(6,6)
debris = canvas.create_image(debris_x, debris_y,image=debris_img, tag="deb")
# デブリの速度
debris_speed = 0.1

# ゲームループ内でデブリをアニメーションさせる関数
def animate_debris():
    global debris_x

    # デブリを左から右に移動
    debris_x += debris_speed
    canvas.coords(debris, debris_x , debris_y )

    # デブリが画面外に出た場合、再利用
    if debris_x > 800:
        debris_x = 0

    # ゲームループでこの関数を再帰的に呼び出す
    #window.after(30, animate_debris)

# ------------------------------------------------------------------------------------------
# ミサイルの動きについて
# ------------------------------------------------------------------------------------------

# ミサイルに関するパラメータの初期化
missile_pos_x = 0 
missile_pos_y = 0
missile_first_pos_x = rocket_x
missile_fisrt_pos_y = rocket_y
missile_mod_pos_x = 0
missile_mod_pos_y = 0

# 重力定数 
mu_scl = 3.986E+16;
# 軌道半径 [m]
R_scl = 6.8E+6;
# 角速度 [rad/s]
Omega_scl = math.sqrt(mu_scl/R_scl/R_scl/R_scl)

# ヒル 　の方程式に基づいてミサイルの加速度を計算
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
    global missile_pos_x, missile_pos_y, missile_vel_x, missile_vel_y,missile_mod_pos_x,missile_mod_pos_y
    # ルンゲクッタ法のステップ幅
    h = 0.1
    # ルンゲクッタ法を使用して次のステップの位置と速度を計算
    [x,y], [missile_vel_x, missile_vel_y] = runge_kutta(h, [missile_pos_x - 400  ,missile_pos_y - missile_fisrt_pos_y], [missile_vel_x, missile_vel_y])
    missile_pos_x = x + missile_first_pos_x
    missile_pos_y = y + missile_fisrt_pos_y
    print(missile_pos_x, missile_pos_y)
    missile_mod_pos_x = x/100 + missile_first_pos_x 
    missile_mod_pos_y = y/100 + missile_fisrt_pos_y

def animate_missile():
    calculate_missile_trajectory()
    canvas.coords(missile, missile_mod_pos_x ,missile_mod_pos_y)

# ミサイルのグラフィック
missile_img = tk.PhotoImage(file="missile.png")
missile = None # Nilもこういうことだったのか．．．
#arrow = None
isCollision = None
# スペースキーを押すとミサイルを発射
def on_space_key(event):
    global missile_mod_vel_x,missile_mod_vel_y,missile_first_pos_x,missile_fisrt_pos_y,missile_pos_x,missile_pos_y, missile, missile_vel_x,missile_vel_y, missile_mod_pos_x,missile_mod_pos_y,arrow,isCollision
    if event.keysym == "space" and flag_input:
        missile_pos_x = rocket_x
        missile_pos_y = rocket_y
        missile_first_pos_x = rocket_x
        missile_fisrt_pos_y = rocket_y
        missile_mod_pos_x = rocket_x
        missile_mod_pos_y = rocket_y
        missile_mod_vel_x = missile_vel_x
        missile_mod_vel_y = missile_vel_y
        isCollision = False
        missile = canvas.create_image(missile_first_pos_x, missile_fisrt_pos_y,image=missile_img, tag="m1")
        #arrow = canvas.create_line(missile_first_pos_x,missile_fisrt_pos_y,missile_first_pos_x+missile_vel_x,missile_fisrt_pos_y+missile_vel_y,arrow=tk.LAST,fill="red", width=5)

# ミサイルアニメーションを停止
def stop_missile_animation():
    global missile,arrow,flag_input,missile_vel_y,missile_vel_x
    canvas.delete("m1")
    missile = None
    #canvas.delete(arrow)
    #arrow = None
    missile_vel_x = missile_mod_vel_x
    missile_vel_y = missile_mod_vel_y
    flag_input = True

def is_tagged_canvas_present(canvas, tag):
    tagged_items = canvas.find_withtag(tag)
    return bool(tagged_items)

net_img = tk.PhotoImage(file="net.png").subsample(10,10)
net = canvas.create_image(missile_first_pos_x, missile_fisrt_pos_y,image=net_img, tag="net")
def animate_net(isCollision):
    global net
    if not isCollision:
        canvas.coords(net, 5000,5000)
    elif isCollision:
        canvas.coords(net, debris_x ,debris_y)

# スペースキーの入力をウィンドウにバインド
window.bind("<space>", on_space_key)

# star main
def main_proc():
    global isCollision,flag_input
    animate_debris()
    
    if is_tagged_canvas_present(canvas,"m1"):
        flag_input = False
        animate_missile()
        distance = math.sqrt((missile_mod_pos_x-debris_x)**2+(missile_mod_pos_y-debris_y)**2)
        if missile_mod_pos_x < 0 or missile_mod_pos_x > 800 or missile_mod_pos_y < 0 or missile_mod_pos_y > 600:
            print("finish")
            stop_missile_animation()
        elif distance<20:
            print("finish")
            stop_missile_animation()
            isCollision = True
    animate_net(isCollision)
        
    # ゲームループでこの関数を再帰的に呼び出す
    window.after(1, main_proc)

main_proc()

# ゲームループの開始
# This display window
window.mainloop()