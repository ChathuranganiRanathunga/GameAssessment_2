#I acknowledge the use of OpenAI ChatGPT to create the code in this file.
import random
import time
import tkinter as tk
from dataclasses import dataclass

WINDOW_W, WINDOW_H = 600, 700
PLAYER_SIZE = 32
ENEMY_W, ENEMY_H = 40, 20
SPAWN_EVERY_MS = 900
TICK_MS = 16  # ~60 FPS

@dataclass
class Vector:
    x: float
    y: float
class CampusDash:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Campus Dash")
        self.canvas = tk.Canvas(root, width=WINDOW_W, height=WINDOW_H, bg="white")
        self.canvas.pack()

        self.is_running = False

        # player
        self.player_x = WINDOW_W // 2
        self.player_y = WINDOW_H - 80
        self.player = self.canvas.create_rectangle(0, 0, PLAYER_SIZE, PLAYER_SIZE, fill="black")
        self._place_player()

        # HUD + game state
        self.score = 0
        self.best_score = 0  
        self.hud = self.canvas.create_text(10, 10, anchor="nw", text="", font=("Helvetica", 14), fill="blue")
        self.canvas.tag_raise(self.hud)

        self.enemies = []                  # list of (canvas_id, vy)
        self.elapsed_since_spawn = 0.0
        self.spawn_interval = SPAWN_EVERY_MS  
        self.last_tick = time.time()

        # input
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

    def _update_hud(self):
        self.canvas.itemconfig(self.hud, text=f"Score: {self.score}    Best: {self.best_score}")

    def _spawn_enemy(self):
        x = random.randint(ENEMY_W // 2, WINDOW_W - ENEMY_W // 2)
        vy = random.uniform(2.0, 4.0)
        eid = self.canvas.create_rectangle(x - ENEMY_W/2, -ENEMY_H, x + ENEMY_W/2, 0, fill="red", outline="darkred")
        self.enemies.append((eid, vy))

    def start(self):
        self.is_running = True
        # (keep best score across runs)
        self.best_score = max(self.best_score, self.score) if hasattr(self, "best_score") else 0
        self.score = 0

        self.enemies.clear()
        self.elapsed_since_spawn = 0.0
        self.spawn_interval = SPAWN_EVERY_MS 
        self._update_hud()
        self.last_tick = time.time()
        self._tick()

    def game_over(self):
        self.is_running = False
        self.best_score = max(self.best_score, self.score)
        self._update_hud()
        self.canvas.create_text(
            WINDOW_W/2, WINDOW_H/2,
            text=f"Game Over\nScore: {self.score}\nBest: {self.best_score}\nPress any key to exit",
            font=("Helvetica", 24, "bold"), fill="black",
            justify="center"
        )
        self.root.bind("<Key>", lambda e: self.root.destroy())

    def _tick(self):
        if not self.is_running: return
        now = time.time()
        dt = now - self.last_tick
        self.last_tick = now

        # spawn with difficulty ramp 
        self.elapsed_since_spawn += dt * 1000.0
        if self.elapsed_since_spawn >= self.spawn_interval:
            self._spawn_enemy()
            self.elapsed_since_spawn = 0.0
            self.spawn_interval = max(400, self.spawn_interval - 8)

        # move enemies
        to_remove = []
        for i, (eid, vy) in enumerate(self.enemies):
            x0, y0, x1, y1 = self.canvas.coords(eid)
            y0 += vy
            y1 += vy
            self.canvas.coords(eid, x0, y0, x1, y1)
            if y0 > WINDOW_H + 10:
                to_remove.append(i)

        # remove offscreen → score
        for idx in reversed(to_remove):
            eid, _ = self.enemies.pop(idx)
            self.canvas.delete(eid)
            self.score += 1
        if to_remove:
            self._update_hud()

        # collision
        px0, py0, px1, py1 = self.canvas.coords(self.player)
        for eid, _ in self.enemies:
            ex0, ey0, ex1, ey1 = self.canvas.coords(eid)
            if not (px1 < ex0 or px0 > ex1 or py1 < ey0 or py0 > ey1):
                self.game_over()
                return
        self.canvas.tag_raise(self.hud)
        # next frame
        self.root.after(TICK_MS, self._tick)

def main():
    root = tk.Tk()
    app = CampusDash(root)
    root.mainloop()

if __name__ == "__main__":
    main()
