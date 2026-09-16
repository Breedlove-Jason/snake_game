import unittest
import random
from pathlib import Path
from tempfile import TemporaryDirectory
from engine import Game
from main import read_best

class EngineTests(unittest.TestCase):
    def test_food_is_free(self):
        for seed in range(100):
            game=Game(rng=random.Random(seed))
            self.assertNotIn(game.food,game.snake)
    def test_reversal_and_double_turn(self):
        game=Game();game.start()
        self.assertFalse(game.turn('left'))
        self.assertTrue(game.turn('up'))
        self.assertFalse(game.turn('left'))
        game.step();self.assertEqual(game.direction,'up')
        self.assertTrue(game.turn('left'))
    def test_growth(self):
        game=Game();game.start();x,y=game.snake[0];game.food=(x+1,y)
        game.step();self.assertEqual(game.score,1);self.assertEqual(len(game.snake),4)
        self.assertNotIn(game.food,game.snake)
    def test_wall_and_restart(self):
        game=Game();game.start();game.snake=[(23,2),(22,2),(21,2)];game.step()
        self.assertEqual(game.status,'over');game.reset()
        self.assertEqual((game.score,len(game.snake),game.status),(0,3,'ready'))
    def test_tail_cell_is_vacated(self):
        game=Game();game.start();game.snake=[(2,2),(2,3),(1,3),(1,2)];game.direction='left';game.food=(10,10)
        game.step();self.assertEqual(game.status,'running');self.assertEqual(game.snake[0],(1,2))
    def test_body_collision(self):
        game=Game();game.start();game.snake=[(2,2),(2,3),(1,3),(1,2),(1,1)];game.direction='left';game.food=(10,10)
        game.step();self.assertEqual(game.status,'over')
    def test_pause(self):
        game=Game();game.start();game.pause();old=game.snapshot();game.step();self.assertEqual(game.snapshot(),old)
        game.start();game.step();self.assertNotEqual(game.snapshot(),old)
    def test_full_board_wins(self):
        game=Game(size=4);game.start();game.snake=[(2,0)]+[(x,y) for y in range(4) for x in range(4) if (x,y) not in [(2,0),(3,0)]];game.food=(3,0)
        game.step();self.assertEqual(game.status,'won');self.assertIsNone(game.food)
    def test_missing_and_corrupt_score(self):
        with TemporaryDirectory() as directory:
            path=Path(directory)/'best';self.assertEqual(read_best(path),0)
            path.write_text('broken');self.assertEqual(read_best(path),0)
            path.write_text('17');self.assertEqual(read_best(path),17)

if __name__=='__main__':unittest.main()
