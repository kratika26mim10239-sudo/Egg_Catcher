# Egg_Catcher


import random
import tkinter as tk
from tkinter import messagebox

# Window Setup
root = tk.Tk()
root.title("Egg Catcher Game")
root.resizable(False, False)

# Canvas Dimensions
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400

canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="deep sky blue")
canvas.pack()

# Game Variables
score = 0
lives = 3
egg_speed = 5
game_running = True

# Draw Background Details (Grass & Sun)
canvas.create_rectangle(0, 350, CANVAS_WIDTH, CANVAS_HEIGHT, fill="light green", outline="")
canvas.create_oval(500, 20, 580, 100, fill="yellow", outline="")

# Create Basket
basket_width = 100
basket_height = 20
basket_x1 = (CANVAS_WIDTH - basket_width) / 2
basket_y1 = CANVAS_HEIGHT - 40
basket_x2 = basket_x1 + basket_width
basket_y2 = basket_y1 + basket_height

basket = canvas.create_rectangle(basket_x1, basket_y1, basket_x2, basket_y2, fill="saddle brown")

# Create Egg
egg_width = 25
egg_height = 35

def create_egg():
    x = random.randint(20, CANVAS_WIDTH - 20)
    egg = canvas.create_oval(x, 0, x + egg_width, egg_height, fill="white", outline="gray")
    return egg

current_egg = create_egg()

# UI Text for Score and Lives
score_text = canvas.create_text(60, 20, text=f"Score: {score}", font=("Arial", 14, "bold"), fill="black")
lives_text = canvas.create_text(CANVAS_WIDTH - 60, 20, text=f"Lives: {lives}", font=("Arial", 14, "bold"), fill="black")

# Controls for Movement
def move_left(event):
    coords = canvas.coords(basket)
    if coords[0] > 0:
        canvas.move(basket, -20, 0)

def move_right(event):
    coords = canvas.coords(basket)
    if coords[2] < CANVAS_WIDTH:
        canvas.move(basket, 20, 0)

root.bind("<Left>", move_left)
root.bind("<Right>", move_right)

# Game Loop logic
def update_game():
    global score, lives, egg_speed, current_egg, game_running

    if not game_running:
        return

    # Move Egg Downwards
    canvas.move(current_egg, 0, egg_speed)
    egg_pos = canvas.coords(current_egg)
    basket_pos = canvas.coords(basket)

    # Check Collision with Basket (Catch)
    if (egg_pos[3] >= basket_pos[1] and egg_pos[1] <= basket_pos[3]):
        if (egg_pos[2] >= basket_pos[0] and egg_pos[0] <= basket_pos[2]):
            score += 10
            canvas.itemconfig(score_text, text=f"Score: {score}")
            canvas.delete(current_egg)
            current_egg = create_egg()
            
            # Slightly increase speed as score grows
            if score % 50 == 0:
                egg_speed += 1

    # Check Missed Egg (Hits Bottom)
    if egg_pos[3] >= CANVAS_HEIGHT:
        lives -= 1
        canvas.itemconfig(lives_text, text=f"Lives: {lives}")
        canvas.delete(current_egg)
        
        if lives > 0:
            current_egg = create_egg()
        else:
            game_running = False
            messagebox.showinfo("Game Over", f"Game Over!\nYour Final Score: {score}")
            root.destroy()
            return

    # Call update_game again after 30 milliseconds
    root.after(30, update_game)

# Start Game
update_game()
root.mainloop()
