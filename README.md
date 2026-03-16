# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**What is this game?**
This is a number guessing game where the player tries to guess a secret number within a limited number of attempts. Depending on the difficulty (Easy, Normal, or Hard), the range of numbers and number of attempts change. After each guess, the game tells you if your guess was too high, too low, or correct. The goal is to guess the right number before you run out of attempts.

**Bugs I found:**

1. **The hints were giving wrong directions.** When you guessed a number, the game would sometimes tell you to go "Higher" when you actually needed to go Lower, and vice versa. After reading the code, I found the issue — the original code was converting numbers to strings on certain attempts and then comparing them like words instead of numbers. In Python, `"9" > "10"` is `True` because it compares letter by letter (like alphabetical order), so the game got confused and flipped the hints.

2. **The "New Game" button didn't fully reset the game.** When you clicked New Game after winning or losing, the old win/loss message would stay on screen and the game would immediately stop again. The problem was that the `status` variable in session state was never reset back to `"playing"`, so the game thought it was already over.

3. **The difficulty ranges were wrong in some places.** The info bar always said "Guess a number between 1 and 100" no matter what difficulty you picked, and when you clicked New Game, it always picked a new secret number between 1 and 100 even on Easy mode. The correct ranges are Easy: 1–20, Normal: 1–100, and Hard: 1–50.

**How I fixed them:**

1. **Hint bug** — I removed the string-casting logic entirely. Since both the guess and the secret number are already integers, Python compares them correctly with `>` and `<` — no need to convert anything to a string. Now `check_guess(9, 10)` correctly returns `"Too Low"`.

2. **New Game reset bug** — I added `st.session_state.status = "playing"` inside the New Game button handler so the game fully resets when you start over. I also made sure the history list clears so nothing carries over from the previous game.

3. **Difficulty range bug** — I fixed the `get_range_for_difficulty` function in `logic_utils.py` to return the correct `(low, high)` values for each difficulty level, and updated all the places in `app.py` that were using the hardcoded `1` and `100` to use those values instead. I also added a difficulty-change detection block so switching the difficulty dropdown generates a fresh secret in the right range.

## 📸 Demo

