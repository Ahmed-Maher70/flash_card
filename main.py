from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

random_card = {}
try:
    updated_data = pd.read_csv("data/words_to_learn.csv")
    new_word = updated_data.to_dict(orient="records")
except FileNotFoundError:
    data = pd.read_csv("data/english_words.csv")
    word = data.to_dict(orient="records")


def new_card():
    global random_card, flip_card_timer
    window.after_cancel(flip_card_timer)
    try:
        random_card = random.choice(new_word)
    except NameError:
        random_card = random.choice(word)

    canvas.itemconfig(img, image=front_card_img)
    canvas.itemconfig(title, text="English", fill="black")
    canvas.itemconfig(random_word, text=random_card["English"], fill="black")
    flip_card_timer = window.after(3000, flip_card)


def flip_card():
    global random_card
    canvas.itemconfig(img, image=back_card_img)
    canvas.itemconfig(title, text="Italian", fill="white")
    canvas.itemconfig(random_word, text=random_card["Italian"], fill="white")


def known_words():
    global random_card
    try:
        new_word.remove(random_card)
        new_data = pd.DataFrame(new_word)
        new_data.to_csv("data/words_to_learn.csv")
    except NameError:
        word.remove(random_card)
        new_data = pd.DataFrame(word)
        new_data.to_csv("data/words_to_learn.csv")

    new_card()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_card_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0)
front_card_img = PhotoImage(file="images/card_front.png")
back_card_img = PhotoImage(file="images/card_back.png")
img = canvas.create_image(400, 263, image=front_card_img)
canvas.config(bg=BACKGROUND_COLOR)
title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
random_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

wrong_btn_img = PhotoImage(file="images/wrong.png")
wrong_btn = Button(image=wrong_btn_img, highlightthickness=0, command=new_card)
wrong_btn.grid(column=0, row=1)

right_btn_img = PhotoImage(file="images/right.png")
right_btn = Button(image=right_btn_img, highlightthickness=0, command=known_words)
right_btn.grid(column=1, row=1)

new_card()


window.mainloop()
