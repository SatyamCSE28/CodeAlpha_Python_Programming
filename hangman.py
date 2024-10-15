import random
import tkinter as tk
from tkinter import messagebox

# List of words for the game
words_list = ['python', 'hangman', 'random', 'programming', 'developer']

# Function to choose a random word from the list
def choose_word():
    return random.choice(words_list)

# Function to update the word display with guessed letters
def update_word_display():
    display = [letter if letter in guessed_letters else '_' for letter in word_to_guess]
    word_display_var.set(' '.join(display))

# Function to handle the guess
def handle_guess():
    guess = guess_entry.get().lower()  # Get the user's input
    guess_entry.delete(0, tk.END)  # Clear the entry box
    
    # Check if input is valid
    if len(guess) != 1 or not guess.isalpha():
        messagebox.showerror("Invalid Input", "Please enter a single alphabetic character.")
        return
    
    # Check if the letter has already been guessed
    if guess in guessed_letters:
        messagebox.showinfo("Already Guessed", f"You already guessed '{guess}'. Try another letter.")
        return

    # Add the guessed letter to the guessed_letters set
    guessed_letters.add(guess)

    # Update the display based on the guess
    if guess in word_to_guess:
        result_label.config(text=f"Good guess! '{guess}' is in the word.")
    else:
        result_label.config(text=f"Wrong guess! '{guess}' is not in the word.")
        global attempts_left
        attempts_left -= 1
        attempts_label.config(text=f"Attempts left: {attempts_left}")
    
    # Update the word display
    update_word_display()

    # Check if the user has guessed the word
    if all(letter in guessed_letters for letter in word_to_guess):
        messagebox.showinfo("Congratulations", f"You guessed the word: {word_to_guess}")
        root.quit()  # End the game

    # Check if attempts are over
    if attempts_left == 0:
        messagebox.showinfo("Game Over", f"Game over! The word was: {word_to_guess}")
        root.quit()  # End the game

# Main GUI setup
root = tk.Tk()
root.title("Hangman Game")
root.geometry("400x300")

# Choose a random word for the game
word_to_guess = choose_word()
guessed_letters = set()
attempts_left = 6

# Word display (label)
word_display_var = tk.StringVar()
update_word_display()
word_display_label = tk.Label(root, textvariable=word_display_var, font=("Arial", 24))
word_display_label.pack(pady=20)

# Result label (show messages for correct or wrong guess)
result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack()

# Attempts left label
attempts_label = tk.Label(root, text=f"Attempts left: {attempts_left}", font=("Arial", 14))
attempts_label.pack(pady=10)

# Entry for user input
guess_entry = tk.Entry(root, font=("Arial", 14), width=5)
guess_entry.pack(pady=10)

# Guess button to submit the input
guess_button = tk.Button(root, text="Guess", command=handle_guess, font=("Arial", 14))
guess_button.pack(pady=10)

# Run the main loop
root.mainloop()
