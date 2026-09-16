# Snake Game

A Python Snake project by Jason Breedlove, with a Turtle desktop edition and a responsive browser edition. Both editions use `engine.py` for movement, growth, food placement, and collisions.

## Play on desktop

Run `python3 main.py` with Python 3.10+ and Tk/Turtle installed. Arrow keys or WASD turn, Space starts/pauses/resumes, and R restarts. A personal best is saved to `~/.snake_game_best`; missing, damaged, or unwritable score files do not prevent play.

The original beginner implementation is preserved in `legacy_turtle/` for comparison. The root-level `snake.py`, `food.py`, and `scoreboard.py` are original modules retained for reference; the current entry point uses the shared engine.

## Play in the browser

Run `npm run build`, then `python3 -m http.server 8000 --directory dist` and visit http://localhost:8000.

The browser loads the pinned Pyodide 314.0.7 runtime from jsDelivr and executes the actual Python engine. JavaScript handles canvas drawing, input, and local personal-best storage. First load requires downloading the Python runtime, so an internet connection is required. No account, backend server, or database is needed. Pyodide supports static hosting: https://pyodide.org/en/stable/usage/downloading-and-deploying.html

- Start a run with **Start game**; arrows/WASD work while the board is focused.
- Space pauses/resumes. R restarts to the ready screen.
- Touch users can swipe on the board or use the direction buttons.
- Switching tabs or windows pauses the game.
- One turn is accepted per tick; direct reversal is rejected.
- Food appears only on free grid cells. Filling the board wins.
- Personal best is local to this browser/device and still works for the current visit if storage is blocked.

## Vercel settings

Import this repository, preset **Other**, root `./`, build command `npm run build`, output `dist`. No environment variables. `vercel.json` supplies the build/output settings. Once deployed, attach `snake.jasonbreedlove.dev` to Production.

## Checks

`python3 -m unittest discover -s tests` runs nine tests covering food placement, queued direction changes, growth, wall/self collisions, moving into a vacated tail cell, pause/restart, full-board wins, and score-file recovery. The actual Pyodide runtime also passed start, turn, tick, pause, restart, and JSON-bridge checks. `node --check web/app.js` checks browser JavaScript syntax. `npm run build` generates the static site.

The hosted browser edition was visually reviewed and gameplay was verified after deployment. Desktop Turtle window interaction and dedicated touch-device testing remain separate checks.
