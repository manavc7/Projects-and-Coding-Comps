from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Input, Label, Button, Static, DataTable
from textual.containers import Vertical, Container
import random
import os
import json

FILENAME = "high_scores.json"
FILENAME_2 = "all_scores.json"


def load_score() -> dict:
    if not os.path.exists(FILENAME):
        return {}
    with open(FILENAME, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_score(scores) -> None:
    with open(FILENAME, "w") as f:
        json.dump(scores, f)


class SetupScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="setup_container"):
            yield Label("Enter User_ID: ", id="user_prompt")
            yield Input(placeholder="e.g Manav", id="user_id_input")
            yield Label("Enter the Level: ", id="level_prompt_label")
            yield Input(placeholder="1, 2 or 3", id="level_input")
            yield Button("Start Game", id="start_button", disabled=True)
        yield Footer()

    def check_if_ready(self) -> None:
        """Checks if user_id and level has been entered and stored"""
        if self.app.user_id is not None and self.app.level is not None:
            self.query_one("#start_button").disabled = False

    def on_input_submitted(self, event: Input.Submitted) -> None:
        # event value is what user submits
        if event.input.id == "level_input":
            level_text = event.value
            try:
                level_num = int(level_text)
                if level_num in (1, 2, 3):
                    self.app.level = level_num
                    self.query_one("#level_prompt_label").update(f"You chose {self.app.level}")
                    self.check_if_ready()  # checks if button can be enabled
                else:
                    self.query_one("#level_prompt_label").update(
                        "[bold red]Error: Level must be 1, 2, or 3.[/bold red]"
                    )
            except ValueError:
                self.query_one("#level_prompt_label").update(
                    "[bold red]Error: Please enter a number.[/bold red]"
                )

        elif event.input.id == "user_id_input":
            self.app.user_id = event.value.lower()
            self.query_one("#user_prompt").update(f"User ID is: {self.app.user_id}")
            self.check_if_ready()  # checks if button can be enabled

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start_button":
            self.app.push_screen(GameScreen())


class GameScreen(Screen):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.time_left = 30  # simple text timer (adjust to taste)
        self.correct_answer = 0
        self.game_timer = None
        self.best_score = 0

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static(f"🏆 Score: {self.score}", id="score_display"),
            Static(f"⏳ Time left: {self.time_left}", id="time_display"),
            Static("", id="problem_display"),
            Input(placeholder="Your Answer...", id="answer_input"),
            id="game_container",
        )
        yield Footer()

    def on_mount(self) -> None:
        # Focus input so player can start typing right away
        self.query_one("#answer_input").focus()

        # Load best score
        scores = load_score()
        user_id = self.app.user_id
        level_str = str(self.app.level)
        self.best_score = scores.get(user_id, {}).get(level_str, 0)

        # Show initial score + best
        self._update_score_display()

        # Show timer
        self.query_one("#time_display").update(f"⏳ Time left: {self.time_left}")

        # Start game
        self.new_question()
        self.game_timer = self.set_interval(1, self.update_timer)

    def _update_score_display(self) -> None:
        self.query_one("#score_display").update(f"🏆 Score: {self.score}   (Best: {self.best_score})")

    def update_timer(self) -> None:
        self.time_left -= 1
        self.query_one("#time_display").update(f"⏳ Time left: {self.time_left}")

        if self.time_left <= 0:
            self.game_timer.stop()
            self.update_high_score()
            self.app.SCREENS["game_over"] = GameOverScreen(final_score=self.score)
            self.app.push_screen(self.app.SCREENS["game_over"])

    def update_high_score(self):
        scores = load_score()
        user_id = self.app.user_id
        level_str = str(self.app.level)
        if user_id not in scores:
            scores[user_id] = {}
        best_score = scores[user_id].get(level_str, 0)
        if self.score > best_score:
            scores[user_id][level_str] = self.score
            save_score(scores)

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "answer_input":
            try:
                if int(event.value) == self.correct_answer:
                    self.score += 1
                    # live-update best score shown if we surpass it mid-run
                    if self.score > self.best_score:
                        self.best_score = self.score
                    self._update_score_display()
                    self.new_question()
                    event.input.value = ""
            except ValueError:
                pass

    def new_question(self) -> None:
        question, answer = self.generate_problem()
        self.correct_answer = answer
        self.query_one("#problem_display").update(question)

    def generate_problem(self) -> tuple[str, int]:
        """Generates numbers for addition, multiplication, division (integer), subtraction."""
        lvl = self.app.level
        # Addition
        add_x = random.randint(max(10 ** (lvl - 1), 1), 10**lvl - 1)
        add_y = random.randint(max(10 ** (lvl - 1), 1), 10**lvl - 1)
        # Multiplication (smaller)
        mul_x = random.randint(1, 4 * lvl)
        mul_y = random.randint(1, 4 * lvl)
        # Division (ensure integer result)
        div_x = random.randint(2, 4 * lvl)
        div_y = div_x * random.randint(2, 4 * lvl)
        # Subtraction
        sub_x = random.randint(max(10 ** (lvl - 1), 1), 10**lvl - 1)
        sub_y = random.randint(max(10 ** (lvl - 1), 1), 10**lvl - 1)

        operator = random.choice([1, 2, 3, 4])
        if operator == 1:
            return f"{add_x} + {add_y} =", add_x + add_y
        elif operator == 2:
            return f"{mul_x} × {mul_y} =", mul_x * mul_y
        elif operator == 3:
            return f"{div_y} ÷ {div_x} =", div_y // div_x
        else:
            return f"{sub_y} - {sub_x} =", sub_y - sub_x


class GameOverScreen(Screen):
    def __init__(self, final_score: int):
        super().__init__()
        self.final_score = final_score

    def compose(self) -> ComposeResult:
        with Vertical(id="game_over_container"):
            yield Static(f"[bold green]Time's Up!\n\nFinal Score: {self.final_score}[/bold green]")
            yield Button("Play Again (Same User)", id="play_again", variant="primary")
            yield Button("View High Scores", id="view_scores", variant="success")
            yield Button("Return to Main Menu", id="main_menu")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "play_again":
            # Simpler: replace current screen with a new GameScreen
            self.app.switch_screen(GameScreen())
        elif event.button.id == "view_scores":
            self.app.push_screen(HighScoresScreen())
        elif event.button.id == "main_menu":
            # Reset user/level and go to setup freshly
            self.app.user_id = None
            self.app.level = None
            self.app.switch_screen(SetupScreen())


class HighScoresScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(id="scores_table")
        yield Footer()
        yield Button("Back", id="back_button")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("User ID", "Level 1", "Level 2", "Level 3")
        scores = load_score()
        for user, level_scores in scores.items():
            table.add_row(
                user,
                str(level_scores.get("1", "-")),
                str(level_scores.get("2", "-")),
                str(level_scores.get("3", "-")),
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back_button":
            self.app.pop_screen()


class MathGame(App):
    CSS_PATH = "math_game.tcss"

    SCREENS = {
        "high_scores": HighScoresScreen
    }

    user_id: str | None = None
    level: int | None = None

    def __init__(self):
        super().__init__()
        self.user_id: str | None = None
        self.level: int | None = None

    def on_mount(self) -> None:
        self.SCREENS["setup"] = SetupScreen()
        self.push_screen(self.SCREENS["setup"])


if __name__ == "__main__":
    MathGame().run()
