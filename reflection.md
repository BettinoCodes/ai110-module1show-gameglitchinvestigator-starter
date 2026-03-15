# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, it appeared to work on the surface but had several concrete problems hiding in the logic. The first bug I noticed was that clicking "New Game" did not fully reset the game -- the won or lost message from the previous round stayed on screen, and the game immediately stopped again because the `status` field was never reset to `"playing"`. The second bug was that the hint feedback was backwards and unreliable: on every even-numbered attempt, the code secretly cast the number to a string and compared it to the player's guess using string comparison, so `"9" > "10"` evaluated as `True` and the game would say "Go HIGHER" when it should have said "Go LOWER." A third problem was that the info message always showed "Guess a number between 1 and 100" even on Easy or Hard, and the "New Game" button always regenerated the secret using `randint(1, 100)` regardless of the selected difficulty.

---

## 2. How did you use AI as a teammate?

I used Claude Code (Claude Sonnet 4.6) as my primary AI assistant throughout this project. One example of a correct and useful suggestion was identifying that the string-casting on even attempts (`secret = str(st.session_state.secret)`) was the root cause of the broken hint feedback -- Claude explained that string comparisons are lexicographic, so `"9" > "10"` is `True`, which caused the wrong direction to be shown, and removing that code entirely fixed the issue immediately. An example of an initial assumption that needed correction was that the first prompt I used suggested the bug was the secret being "generated outside the valid range," but when we actually read the code, the initial generation on line 93 was already using `low` and `high` correctly -- the real problems were the hardcoded `randint(1, 100)` in the New Game button and the missing difficulty-change detection, which were more subtle than expected.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed by reading the relevant lines of code after each change and reasoning through the execution path to confirm the old bad behavior was no longer possible. For the hint-direction bug, I verified the fix by tracing through `check_guess(9, 10)` mentally -- with both arguments as integers, `9 > 10` is `False`, so it correctly returns `"Too Low"`, which is the right answer. The project also has a `tests/test_game_logic.py` file with three pytest cases covering `check_guess` for win, too-high, and too-low outcomes; those tests confirmed the function's return values match what the game logic expects. Claude helped me understand that `check_guess` needed to return a tuple like `("Too High", "...")` rather than just a string, which is what the tests were checking against.

---

## 4. What did you learn about Streamlit and state?

In the original app, the secret number kept being wrong across difficulty changes because Streamlit reruns the entire Python script from top to bottom on every user interaction, and the `if "secret" not in st.session_state` guard only runs once -- when the key doesn't exist yet. After that, switching difficulty had no effect on the stored secret because the guard was skipped, leaving a Normal-range secret active during an Easy game. I would explain Streamlit reruns to a friend like this: every time you click a button or change a dropdown, Streamlit re-executes your whole script like pressing refresh on a page, and `session_state` is a dictionary that survives those refreshes so your data isn't wiped out each time. The fix that finally gave the game a stable, correct secret was adding a `st.session_state.difficulty` tracker -- on each rerun, if the stored difficulty doesn't match the selected one, the game fully resets and generates a new secret within the correct range for the new difficulty.

---

## 5. Looking ahead: your developer habits

One habit I want to carry forward is reading the full source before touching anything -- in this project, the most misleading bug (the string-casting on even attempts) was completely invisible from the outside and only obvious after reading the code carefully. Next time I work with AI on a coding task, I would give it the actual code to read first rather than describing the symptoms, because the AI's initial suggestions based on the bug description alone pointed in a slightly wrong direction, whereas once it read the file it identified the exact lines causing the problem. This project changed how I think about AI-generated code: it can produce code that looks reasonable and even runs without errors, but contains small and minor logic bugs that only reveal themselves under specific conditions, so reading and understanding the code yourself is still essential even when AI wrote it.
