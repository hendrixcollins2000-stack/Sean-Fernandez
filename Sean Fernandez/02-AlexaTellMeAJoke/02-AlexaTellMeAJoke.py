
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import random

# Location of the jokes file
RESOURCE_FILE = Path(__file__).resolve().parent / "resources" / "randomJokes.txt"

jokes = []
current_joke = None


# Load jokes from the text file
def loadJokes():
    joke_list = []

    try:
        file = open(RESOURCE_FILE, "r", encoding="utf-8")

        for line in file:
            line = line.strip()

            if line == "":
                continue

            if "?" in line:
                parts = line.split("?", 1)
                setup = parts[0].strip()
                punchline = parts[1].strip()

                if setup != "" and punchline != "":
                    joke_list.append((setup + "?", punchline))

        file.close()

    except FileNotFoundError:
        messagebox.showerror(
            "Error",
            "Joke file not found! Check your resources folder."
        )

    except OSError as error:
        messagebox.showerror("File Error", str(error))

    return joke_list


# Display a random joke
def displayJoke():
    global current_joke

    if len(jokes) == 0:
        setup_label.config(text="No jokes available!")
        punchline_label.config(text="")
        punchline_button.config(state="disabled")
        next_button.config(state="disabled")
        return

    # Pick a different joke if possible
    new_jokes = []

    for joke in jokes:
        if joke != current_joke:
            new_jokes.append(joke)

    if len(new_jokes) == 0:
        new_jokes = jokes

    current_joke = random.choice(new_jokes)

    setup = current_joke[0]

    setup_label.config(text=setup)
    punchline_label.config(text="")
    punchline_button.config(state="normal")


# Show the answer to the joke
def showPunchline():
    if current_joke != None:
        punchline = current_joke[1]
        punchline_label.config(text=punchline)
        punchline_button.config(state="disabled")


# Main joke button
def startJoke():
    displayJoke()


# Close the program
def quitApplication():
    root.destroy()


# Create the main window
root = tk.Tk()
root.title("Alexa, Tell Me a Joke!")
root.geometry("600x430")
root.resizable(False, False)
root.config(bg="#10121c")

# Load the jokes
jokes = loadJokes()


# Title
title_label = tk.Label(
    root,
    text="ALEXA, TELL ME A JOKE!",
    font=("Arial", 22, "bold"),
    bg="#10121c",
    fg="#00d9ff"
)
title_label.pack(pady=(25, 10))


# Instructions
instruction_label = tk.Label(
    root,
    text="Click the button below to get a random joke.",
    font=("Arial", 12),
    bg="#10121c",
    fg="#c5c9d6"
)
instruction_label.pack(pady=5)


# Joke button
joke_button = tk.Button(
    root,
    text="Alexa tell me a Joke",
    font=("Arial", 13, "bold"),
    bg="#2563eb",
    fg="white",
    width=24,
    command=startJoke
)
joke_button.pack(pady=15)


# Joke setup
setup_label = tk.Label(
    root,
    text="Your joke will appear here!",
    font=("Arial", 16, "bold"),
    bg="#202638",
    fg="white",
    wraplength=500,
    width=42,
    height=3,
    relief="groove",
    padx=10,
    pady=10
)
setup_label.pack(pady=12, padx=25)


# Show punchline button
punchline_button = tk.Button(
    root,
    text="Show Punchline",
    font=("Arial", 12),
    bg="#9333ea",
    fg="white",
    width=20,
    command=showPunchline,
    state="disabled"
)
punchline_button.pack(pady=8)


# Punchline display
punchline_label = tk.Label(
    root,
    text="",
    font=("Arial", 14, "bold"),
    bg="#173b32",
    fg="#4ade80",
    wraplength=500,
    width=42,
    height=2,
    padx=10,
    pady=8
)
punchline_label.pack(pady=8, padx=25)


# Bottom buttons
bottom_frame = tk.Frame(root, bg="#10121c")
bottom_frame.pack(pady=15)


# Next joke button
next_button = tk.Button(
    bottom_frame,
    text="Next Joke",
    font=("Arial", 11, "bold"),
    bg="#0891b2",
    fg="white",
    width=15,
    command=displayJoke,
    state="normal" if jokes else "disabled"
)
next_button.pack(side=tk.LEFT, padx=10)


# Quit button
quit_button = tk.Button(
    bottom_frame,
    text="Quit",
    font=("Arial", 11, "bold"),
    bg="#dc2626",
    fg="white",
    width=15,
    command=quitApplication
)
quit_button.pack(side=tk.LEFT, padx=10)


# Keep the window running
root.mainloop()

