
import tkinter as tk
import random

# Create the main window
root = tk.Tk()
root.title("Maths Quiz")
root.geometry("550x500")
root.resizable(False, False)
root.config(bg="black")

# Quiz variables
difficulty = ""
score = 0
question_number = 0
attempts = 0
num1 = 0
num2 = 0
operation = ""
correct_answer = 0


# Clear the screen
def clearWindow():
    for widget in root.winfo_children():
        widget.destroy()


# Display the main menu
def displayMenu():
    clearWindow()

    tk.Label(
        root, text="MATHS QUIZ",
        font=("Arial", 26, "bold"),
        bg="black", fg="#CE93D8"
    ).pack(pady=30)

    tk.Label(
        root, text="Select your difficulty level:",
        font=("Arial", 14, "bold"),
        bg="black", fg="white"
    ).pack(pady=10)

    # Easy button
    tk.Button(
        root, text="Easy",
        width=20, font=("Arial", 12, "bold"),
        command=lambda: startQuiz("Easy"),
        bg="#29B6F6", fg="black"
    ).pack(pady=8)

    # Moderate button
    tk.Button(
        root, text="Moderate",
        width=20, font=("Arial", 12, "bold"),
        command=lambda: startQuiz("Moderate"),
        bg="#FFCA28", fg="black"
    ).pack(pady=8)

    # Advanced button
    tk.Button(
        root, text="Advanced",
        width=20, font=("Arial", 12, "bold"),
        command=lambda: startQuiz("Advanced"),
        bg="#F06292", fg="black"
    ).pack(pady=8)

    # Back button to exit
    tk.Button(
        root, text="Back / Exit",
        width=20, font=("Arial", 11, "bold"),
        command=root.destroy,
        bg="#B0BEC5", fg="black"
    ).pack(pady=20)


# Generate random numbers depending on difficulty
def randomInt(level):

    if level == "Easy":
        minimum = 0
        maximum = 9

    elif level == "Moderate":
        minimum = 10
        maximum = 99

    else:
        minimum = 1000
        maximum = 9999

    num1 = random.randint(minimum, maximum)
    num2 = random.randint(minimum, maximum)

    return num1, num2


# Choose addition or subtraction randomly
def decideOperation():
    return random.choice(["+", "-"])


# Display the maths question
def displayProblem():

    global num1, num2, operation, correct_answer, attempts

    clearWindow()

    # Check if all 10 questions are finished
    if question_number >= 10:
        displayResults(score)
        return

    # Create a random question
    num1, num2 = randomInt(difficulty)
    operation = decideOperation()

    if operation == "+":
        correct_answer = num1 + num2
    else:
        correct_answer = num1 - num2

    attempts = 0

    # Show question number
    tk.Label(
        root, text=f"Question {question_number + 1} of 10",
        font=("Arial", 17, "bold"),
        bg="black", fg="#CE93D8"
    ).pack(pady=15)

    # Show difficulty
    tk.Label(
        root, text=f"Difficulty: {difficulty}",
        font=("Arial", 12, "bold"),
        bg="black", fg="#29B6F6"
    ).pack(pady=5)

    # Show the maths problem
    tk.Label(
        root, text=f"{num1} {operation} {num2} = ?",
        font=("Arial", 28, "bold"),
        bg="#512DA8", fg="white",
        width=18
    ).pack(pady=20)

    tk.Label(
        root, text="Enter your answer:",
        font=("Arial", 12, "bold"),
        bg="black", fg="white"
    ).pack(pady=5)

    # Answer entry box
    answer_entry = tk.Entry(
        root, font=("Arial", 16),
        justify="center", width=15
    )
    answer_entry.pack(pady=10)
    answer_entry.focus()

    # Feedback message
    feedback_label = tk.Label(
        root, text="",
        font=("Arial", 11, "bold"),
        bg="black", fg="white",
        wraplength=450
    )
    feedback_label.pack(pady=8)

    # Submit button
    submit_button = tk.Button(
        root, text="Submit Answer",
        font=("Arial", 12, "bold"),
        bg="#7E57C2", fg="white",
        width=18
    )
    submit_button.pack(pady=8)

    # Check the user's answer
    def submitAnswer():

        global attempts, score

        answer = answer_entry.get().strip()

        # Check if the answer is a whole number
        try:
            user_answer = int(answer)

        except ValueError:
            feedback_label.config(
                text="Please enter a valid whole number.",
                fg="#FF5252"
            )
            return

        attempts += 1

        result, message = isCorrect(user_answer, correct_answer)

        if result:

            if attempts == 1:
                score += 10
                feedback_label.config(
                    text=message + " You earned 10 points!",
                    fg="#69F0AE"
                )

            else:
                score += 5
                feedback_label.config(
                    text=message + " You earned 5 points!",
                    fg="#69F0AE"
                )

            submit_button.config(state="disabled")
            answer_entry.config(state="disabled")

            tk.Button(
                root, text="Next Question",
                font=("Arial", 12, "bold"),
                bg="#66BB6A", fg="black",
                command=nextQuestion
            ).pack(pady=8)

        else:

            if attempts == 1:
                feedback_label.config(
                    text="Incorrect! Try again. You have one more attempt.",
                    fg="#FF5252"
                )
                answer_entry.delete(0, tk.END)
                answer_entry.focus()

            else:
                feedback_label.config(
                    text=f"Incorrect again! The correct answer was {correct_answer}.",
                    fg="#FF5252"
                )

                submit_button.config(state="disabled")
                answer_entry.config(state="disabled")

                tk.Button(
                    root, text="Next Question",
                    font=("Arial", 12, "bold"),
                    bg="#66BB6A", fg="black",
                    command=nextQuestion
                ).pack(pady=8)

    submit_button.config(command=submitAnswer)

    # Press Enter to submit the answer
    answer_entry.bind(
        "<Return>",
        lambda event: submitAnswer()
    )

    # Return to the difficulty menu
    tk.Button(
        root, text="Back to Menu",
        font=("Arial", 10, "bold"),
        bg="#FFAB91", fg="black",
        command=displayMenu
    ).pack(pady=8)


# Check if the answer is correct
def isCorrect(user_answer, answer):

    if user_answer == answer:
        return True, "Correct! Well done."

    else:
        return False, "That answer is incorrect."


# Go to the next question
def nextQuestion():

    global question_number

    question_number += 1

    displayProblem()


# Display the final results
def displayResults(final_score):

    clearWindow()

    # Calculate the grade
    if final_score > 90:
        grade = "A+"
        message = "Outstanding performance!"

    elif final_score >= 80:
        grade = "A"
        message = "Excellent work!"

    elif final_score >= 70:
        grade = "B"
        message = "Very good effort!"

    elif final_score >= 60:
        grade = "C"
        message = "Good effort!"

    elif final_score >= 50:
        grade = "D"
        message = "You passed. Keep practising!"

    else:
        grade = "F"
        message = "Keep practising. You can improve!"

    # Show the final score
    tk.Label(
        root, text="QUIZ COMPLETED!",
        font=("Arial", 23, "bold"),
        bg="black", fg="#CE93D8"
    ).pack(pady=25)

    tk.Label(
        root, text=f"Your final score: {final_score}/100",
        font=("Arial", 20, "bold"),
        bg="black", fg="#29B6F6"
    ).pack(pady=10)

    tk.Label(
        root, text=f"Your grade: {grade}",
        font=("Arial", 18, "bold"),
        bg="black", fg="#69F0AE"
    ).pack(pady=10)

    tk.Label(
        root, text=message,
        font=("Arial", 13, "bold"),
        bg="black", fg="white"
    ).pack(pady=10)

    tk.Label(
        root, text="Would you like to play again?",
        font=("Arial", 13),
        bg="black", fg="white"
    ).pack(pady=15)

    # Play again button
    tk.Button(
        root, text="Yes - Play Again",
        font=("Arial", 12, "bold"),
        width=18, bg="#81C784", fg="black",
        command=displayMenu
    ).pack(pady=5)

    # Exit button
    tk.Button(
        root, text="No - Exit",
        font=("Arial", 12, "bold"),
        width=18, bg="#EF9A9A", fg="black",
        command=root.destroy
    ).pack(pady=5)


# Start a new quiz
def startQuiz(level):

    global difficulty, score, question_number

    difficulty = level
    score = 0
    question_number = 0

    displayProblem()


# Run the program
displayMenu()

root.mainloop()