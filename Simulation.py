import tkinter as tk

root = tk.Tk()
root.geometry("300x300+50+50")

canvas = tk.Canvas(root, width=800, height=800)
canvas.pack()

class Entity:
    def __init__(self, position, size):
        self.pos = position
        self.size = size
        self.entity = canvas.create_oval(
            position[0]-size/2,
            position[1]-size/2,
            position[0]+size/2,
            position[1]+size/2,
            fill="blue"
        )
    
    def move(self, offset):
        canvas.move(self.entity, offset[0], offset[1])
        self.pos[0] += offset[0]
        self.pos[1] += offset[1]

sphere = Entity([20, 20], 20)

def game_loop():
    sphere.move([0, 0])
    root.after(1, game_loop)

game_loop()

root.mainloop()