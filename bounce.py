
try:
    from Tkinter import * #for python2
except ImportError:
    from tkinter import * #for python3
import random
import time

global score
score = 0

class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.x += self.paddle.x
                return True
        return False
    
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos) == True:
            self.hit()
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3

    def hit(self):
        global score
        score += 1
        self.y = -3
    
class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.started = False
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Down>', self.turn_stop)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all("<Button-1>", self.start_game)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0
    
    def turn_left(self, evt):
        self.x = -3
        self.started = True

    def turn_stop(self, evt):
        self.x = 0
        self.started = True
        
    def turn_right(self, evt):
        self.x = 3
        self.started = True

    def start_game(self, evt):
        self.started = True

tk = Tk()
tk.title("Game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=500, bd=1, highlightthickness=1)
canvas.pack()
tk.update()

paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, 'red')
score_text = canvas.create_text(400, 50, text='Score : 0', state="normal")
game_over_text = canvas.create_text(250, 200, text='GAME OVER', state="hidden")

while True:
    if ball.hit_bottom == False and paddle.started == True:
        ball.draw()
        paddle.draw()
    if ball.hit_bottom == True:
        canvas.itemconfig(game_over_text, state='normal')
    canvas.itemconfig(score_text, text='Score : %s' %(score))
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
