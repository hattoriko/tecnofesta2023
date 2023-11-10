import tkinter as tk

class SatelliteGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Satellite Game")

        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="black")
        self.canvas.pack()

        self.earth = self.canvas.create_oval(195, 195, 205, 205, fill="blue")  # 地球を描画
        self.satellite = None  # 衛星のオブジェクト

        self.velocity_entry = tk.Entry(self.master, width=10)
        self.velocity_entry.pack()

        self.start_button = tk.Button(self.master, text="Start Game", command=self.start_game)
        self.start_button.pack()

    def start_game(self):
        velocity_str = self.velocity_entry.get()
        try:
            velocity = float(velocity_str)
            self.move_satellite(velocity)
        except ValueError:
            print("Please enter a valid numeric value for velocity.")

    def move_satellite(self, velocity):
        if self.satellite:
            self.canvas.delete(self.satellite)

        self.satellite = self.canvas.create_oval(200 - 10, 200 - 10, 200 + 10, 200 + 10, fill="red")  # 衛星を描画
        self.animate_satellite(velocity)

    def animate_satellite(self, velocity):
        angle = 0
        while True:
            x = 200 + 100 * velocity * angle
            y = 200
            self.canvas.coords(self.satellite, x - 10, y - 10, x + 10, y + 10)
            self.master.update()
            angle += 0.01  # 0.01ラジアンごとに更新

root = tk.Tk()
app = SatelliteGame(root)
root.mainloop()
