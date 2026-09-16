"""Desktop Turtle renderer for the shared Python game engine."""
from pathlib import Path
import turtle
from engine import Game


def read_best(path):
    try:
        return max(0, int(path.read_text().strip()))
    except (OSError, ValueError):
        return 0


def main():
    game = Game()
    score_path = Path.home() / '.snake_game_best'
    best = read_best(score_path)
    screen = turtle.Screen()
    screen.setup(600, 660)
    screen.bgcolor('#0b1412')
    screen.title('Snake / Jason Breedlove')
    screen.tracer(0)
    pen = turtle.Turtle(visible=False)
    pen.penup()
    pen.shape('square')
    pen.shapesize(.9, .9)
    label = turtle.Turtle(visible=False)
    label.penup()

    def render():
        pen.clearstamps()
        for index, (x, y) in enumerate(game.snake):
            pen.color('#d2ff66' if index == 0 else '#5eac80')
            pen.goto(x * 20 - 230, 230 - y * 20)
            pen.stamp()
        if game.food:
            x, y = game.food
            pen.color('#ff7191')
            pen.goto(x * 20 - 230, 230 - y * 20)
            pen.stamp()
        label.clear()
        label.goto(0, 280)
        label.color('white')
        label.write(f'SCORE {game.score:02}   BEST {best:02}', align='center', font=('Courier', 18, 'normal'))
        label.goto(0, -290)
        messages = {'ready':'SPACE to start', 'running':'Arrows / WASD · SPACE pause · R restart',
                    'paused':'Paused · SPACE to resume', 'over':'Game over · R to restart', 'won':'Board complete! · R to restart'}
        label.write(messages[game.status], align='center', font=('Courier', 12, 'normal'))
        screen.update()

    def toggle():
        game.pause() if game.status == 'running' else game.start()
        render()

    def reset():
        game.reset()
        render()

    def tick():
        nonlocal best
        game.step()
        if game.score > best:
            best = game.score
            try:
                score_path.write_text(str(best))
            except OSError:
                pass
        render()
        screen.ontimer(tick, max(65, 145 - game.score * 2))

    for key, direction in [('Up','up'),('w','up'),('Down','down'),('s','down'),('Left','left'),('a','left'),('Right','right'),('d','right')]:
        screen.onkey(lambda direction=direction: game.turn(direction), key)
    screen.onkey(toggle, 'space')
    screen.onkey(reset, 'r')
    screen.listen()
    tick()
    screen.mainloop()


if __name__ == '__main__':
    main()
