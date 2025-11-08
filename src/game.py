#I acknowledge the use of OpenAI ChatGPT to create the code in this file.
import time
import tkinter as tk

WINDOW_W, WINDOW_H = 600, 700
PLAYER_SIZE = 32
TICK_MS = 16  # ~60 FPS

class CampusDash:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Campus Dash")
        self.canvas = tk.Canvas(root, width=WINDOW_W, height=WINDOW_H, bg="white")
        self.canvas.pack()

        self.is_running = False
        self.player_x = WINDOW_W // 2
        self.player_y = WINDOW_H - 80
        self.player = self.canvas.create_rectangle(0, 0, PLAYER_SIZE, PLAYER_SIZE, fill="black")
        self._place_player()

        root.bind("<Left>",  lambda e: self._move(-20, 0))
        root.bind("<Right>", lambda e: self._move(20, 0))
        root.bind("<Up>",    lambda e: self._move(0, -20))
        root.bind("<Down>",  lambda e: self._move(0, 20))

        self.start()

    def _place_player(self):
        x0 = self.player_x - PLAYER_SIZE/2
        y0 = self.player_y - PLAYER_SIZE/2
        x1 = self.player_x + PLAYER_SIZE/2
        y1 = self.player_y + PLAYER_SIZE/2
        self.canvas.coords(self.player, x0, y0, x1, y1)

    def _move(self, dx, dy):
        if not self.is_running: return
        self.player_x = min(max(self.player_x + dx, PLAYER_SIZE/2), WINDOW_W - PLAYER_SIZE/2)
        self.player_y = min(max(self.player_y + dy, PLAYER_SIZE/2), WINDOW_H - PLAYER_SIZE/2)
        self._place_player()

    def start(self):
        self.is_running = True
        self._tick()

    def _tick(self):
        if not self.is_running: return
        # No enemies yet — just keep updating at ~60 FPS
        self.root.after(TICK_MS, self._tick)

def main():
    root = tk.Tk()
    app = CampusDash(root)
    root.mainloop()

if __name__ == "__main__":
    main()
