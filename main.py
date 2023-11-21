from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pandas.read_csv("data/words_to_learn_csv")
except FileNotFoundError:
    orignal_data = pandas.read_csv("data/french_words.csv")
    to_learn = orignal_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
current_card = {}

def next_card():
    global current_card
    global flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text = "French", fill = "black")
    canvas.itemconfig(card_word, text = current_card["French"], fill = "black")
    canvas.itemconfig(card_background, image = card_front_img)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text = "English", fill = "white")
    canvas.itemconfig(card_word, text = current_card["English"], fill = "white")
    canvas.itemconfig(card_background, image = card_back_img)

def is_known():
    to_learn.remove(current_card)
    pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn_csv", index= False)
    next_card()

window = Tk()
window.title("Flash Card app")
window.config(pady=50, padx=50, bg = BACKGROUND_COLOR)

flip_timer = window.after(3000, func = flip_card)

canvas = Canvas(width = 800, height = 526, bg = BACKGROUND_COLOR)
card_front_img =PhotoImage(file = "images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image = card_front_img)
card_title = canvas.create_text(400, 150, text = "", font = ("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text = "", font = ("Ariel", 60, "bold"))
canvas.grid(row = 0, column = 0, columnspan = 2)
canvas.config(highlightthickness = 0)

cross_image = PhotoImage(file = "images/wrong.png")
unknown_button = Button(image = cross_image, command=next_card)
unknown_button.grid(row = 1, column = 0)
unknown_button.config(highlightthickness = 0)

check_image = PhotoImage(file = "images/right.png")
known_button = Button(image = check_image, command=is_known)
known_button.grid(row =1, column = 1)
known_button.config(highlightthickness = 0)

next_card()

window.mainloop()