import tkinter
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT = 'Arial'
current_card = {}
original_data = {}

try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas_card.itemconfig(card_title, text="French", fill="black")
    canvas_card.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas_card.itemconfig(card_background, image=image_card)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas_card.itemconfig(card_title, text="English", fill="white")
    canvas_card.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas_card.itemconfig(card_background, image=new_image)


def remove_word():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("words_to_learn.csv", index=False)
    next_card()


window = tkinter.Tk()
window.title("Flash cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas_card = tkinter.Canvas(width=800, height=526)
image_card = tkinter.PhotoImage(file="images/card_front.png")
new_image = tkinter.PhotoImage(file="images/card_back.png")
card_background = canvas_card.create_image(400, 263, image=image_card)
card_title = canvas_card.create_text(400, 150, text="Title", font=(FONT, 40, "italic"))
card_word = canvas_card.create_text(400, 263, text="word", font=(FONT, 60, "bold"))
canvas_card.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_card.grid(column=0, row=0, columnspan=2)

image_wrong = tkinter.PhotoImage(file="images/wrong.png")
button_wrong = tkinter.Button(image=image_wrong, highlightthickness=0, command=next_card)
button_wrong.grid(column=0, row=1)

image_right = tkinter.PhotoImage(file="images/right.png")
button_right = tkinter.Button(image=image_right, highlightthickness=0, command=remove_word)
button_right.grid(column=1, row=1)

next_card()

window.mainloop()
