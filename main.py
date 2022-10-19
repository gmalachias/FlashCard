from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")
to_learn = {}
current_card = {}

try:
    to_learn = pandas.read_csv("data/words.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = to_learn.to_dict(orient="records")

# ----------------------------Functions----------------------- #


def random_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(language_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_image, image=front_image)
    flip_timer = window.after(3000, func=change)


def change():
    canvas.itemconfig(tagOrId=canvas_image, image=back_image)
    canvas.itemconfig(tagOrId=language_text, text="English", fill="white")
    canvas.itemconfig(tagOrId=word_text, text=current_card["English"], fill="white")


def is_know():
    to_learn.remove(current_card)
    random_word()
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words.csv", index=False)

# ----------------------------UI----------------------------- #


window = Tk()
window.title("Do you know the word?!")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, change)

canvas = Canvas(width=800, height=526)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=front_image)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

language_text = canvas.create_text(400, 150, text="French", font=LANGUAGE_FONT)
word_text = canvas.create_text(400, 263, text="", font=WORD_FONT)


right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_know)
right_button.grid(column=1, row=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=random_word)
wrong_button.grid(column=0, row=1)
random_word()


window.mainloop()
