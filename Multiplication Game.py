from tkinter import *
import random
from tkinter import messagebox

class MultiplicationGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Multiplication with 2 Players")
        self.root.geometry("800x400")
        self.root.resizable(True, True)

        self.current_player = 1
        self.scores = [0, 0]
        self.correct_answer = None
        self.arrow_labels = []

        self.create_widgets()

    def create_widgets(self):
        # Game guide page
        self.game_guide_frame = Frame(self.root)
        self.game_guide_frame.pack(pady=20)

        guide_text = (
            "Welcome to Multiplication with 2 Players!\n\n"
            "Instructions:\n"
            "1. Two players take turns answering multiplication questions.\n"
            "2. Each player's goal is to fill all 7 boxes with correct answers.\n"
            "3. Click on the button with the correct answer.\n"
            "4. The player who fills all boxes first wins the game.\n\n"
            "Click 'Start Game' to begin!\n\n"
            "Icons guide:\n"
            "⇨ - Indicates the progress of the current player.\n"
            "✔ - Indicates a correct answer filled by the player."
        )

        self.guide_label = Label(self.game_guide_frame, text=guide_text, font=("Helvetica", 14))
        self.guide_label.pack(pady=20)

        self.start_button = Button(self.game_guide_frame, text="Start Game", font=("Helvetica", 12), command=self.start_game)
        self.start_button.pack()

        # Game page
        self.game_frame = Frame(self.root)

        # Create top and bottom placeholders
        self.top_frame = Frame(self.game_frame)
        self.top_frame.pack(side=TOP, pady=10)

        self.middle_frame = Frame(self.game_frame)
        self.middle_frame.pack(side=TOP, pady=20)

        self.bottom_frame = Frame(self.game_frame)
        self.bottom_frame.pack(side=TOP, pady=10)

        # Create player indicators
        self.red_circle = Label(self.top_frame, bg="red", width=2, height=1, relief="solid")
        self.red_circle.grid(row=0, column=0, padx=5, pady=5)

        self.blue_circle = Label(self.bottom_frame, bg="blue", width=2, height=1, relief="solid")
        self.blue_circle.grid(row=0, column=0, padx=5, pady=5)

        # Create top and bottom placeholders
        self.top_placeholders = []
        for k in range(7):
            label = Label(self.top_frame, text="", width=10, height=2, bg="lightgray", relief="solid")
            label.grid(row=0, column=k + 1, padx=5, pady=5)
            self.top_placeholders.append(label)

        self.bottom_placeholders = []
        for k in range(7):
            label = Label(self.bottom_frame, text="", width=10, height=2, bg="lightgray", relief="solid")
            label.grid(row=0, column=k + 1, padx=5, pady=5)
            self.bottom_placeholders.append(label)

        # Create question label in the center
        self.question_label = Label(self.middle_frame, text="", font=("Helvetica", 24))
        self.question_label.pack(side=LEFT, padx=20)

        # Create buttons in the center
        self.answer_buttons = []
        for i in range(5):
            button = Button(self.middle_frame, text="", width=10, height=2)
            button.config(command=lambda b=button: self.check_answer(b))
            button.pack(side=LEFT, padx=5)
            self.answer_buttons.append(button)

        # Create a status label at the bottom
        self.status_label = Label(self.game_frame, text="Information about players' progress.", font=("Helvetica", 12), relief="solid", justify=LEFT)
        self.status_label.pack(side=TOP, pady=20)

    def start_game(self):
        self.game_guide_frame.pack_forget()
        self.game_frame.pack()
        self.update_status()
        self.next_question()

    def next_question(self):
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        self.correct_answer = num1 * num2
        self.question_label.config(text=f"{num1} x {num2} = ?")

        answers = [self.correct_answer]
        while len(answers) < 5:
            fake_answer = random.randint(1, 100)
            if fake_answer not in answers:
                answers.append(fake_answer)

        random.shuffle(answers)
        for i in range(5):
            self.answer_buttons[i].config(text=str(answers[i]))

    def check_answer(self, button):
        try:
            selected_answer = int(button["text"])
        except ValueError:
            messagebox.showerror("Invalid Input", "Please select a valid number.")
            return

        if selected_answer == self.correct_answer:
            self.scores[self.current_player - 1] += 1
            if self.scores[self.current_player - 1] == 8:  # Check if player has filled all 7 boxes
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
                return
            self.move_player()  # Place check icon for correct answer
        else:
            messagebox.showinfo("Wrong Answer", "Incorrect answer. Switching player.")
            self.current_player = 2 if self.current_player == 1 else 1

        self.update_status()
        self.next_question()

    def move_player(self):
        # Remove previous arrow labels
        for label in self.arrow_labels:
            label.destroy()
        self.arrow_labels = []

        if self.current_player == 1:
            for label in self.top_placeholders:
                if label["text"] == "":
                    label.config(text="✔")
                    arrow_label = Label(self.top_frame, text="➜", font=("Helvetica", 12))
                    arrow_label.grid(row=0, column=label.grid_info()["column"], padx=5, pady=5)
                    self.arrow_labels.append(arrow_label)
                    break
        else:
            for label in self.bottom_placeholders:
                if label["text"] == "":
                    label.config(text="✔")
                    arrow_label = Label(self.bottom_frame, text="➜", font=("Helvetica", 12))
                    arrow_label.grid(row=0, column=label.grid_info()["column"], padx=5, pady=5)
                    self.arrow_labels.append(arrow_label)
                    break

    def update_status(self):
        self.status_label.config(text=f"Player 1: {self.scores[0]} correct answers\nPlayer 2: {self.scores[1]} correct answers\nPlayer {self.current_player}'s turn")

    def reset_game(self):
        self.scores = [0, 0]
        self.current_player = 1
        for label in self.top_placeholders:
            label.config(text="", bg="lightgray")
        for label in self.bottom_placeholders:
            label.config(text="", bg="lightgray")
        self.update_status()
        self.game_frame.pack_forget()  # Hide the game frame
        self.game_guide_frame.pack()   # Show the game guide frame again

if __name__ == "__main__":
    root = Tk()
    game = MultiplicationGame(root)
    root.mainloop()
