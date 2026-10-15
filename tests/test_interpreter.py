"""
Unit tests for the CodeLan lexer, parser, interpreter, and features.
"""

import unittest
from codelan.lexer import Lexer
from codelan.parser import Parser
from codelan.interpreter import Interpreter

def run_code(source: str):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    prog = parser.parse()
    interp = Interpreter()
    interp.run_program(prog)
    return interp

class TestCodeLan(unittest.TestCase):
    def test_arithmetic_and_variables(self):
        code = """
        let x = 10
        let y = 20
        let z = (x + y) * 2 - 10 / 2
        """
        interp = run_code(code)
        self.assertEqual(interp.global_env.get("z"), 55)

    def test_strings_and_interpolation(self):
        code = """
        let name = "Alex"
        let score = 100
        let msg = "Player {name} scored {score} points!"
        """
        interp = run_code(code)
        self.assertEqual(interp.global_env.get("msg"), "Player Alex scored 100 points!")

    def test_if_else(self):
        code = """
        let score = 75
        let grade = "F"
        if (score >= 90) {
            grade = "A"
        } else if (score >= 70) {
            grade = "B"
        } else {
            grade = "C"
        }
        """
        interp = run_code(code)
        self.assertEqual(interp.global_env.get("grade"), "B")

    def test_while_loop(self):
        code = """
        let count = 0
        let total = 0
        while (count < 5) {
            count += 1
            total += count
        }
        """
        interp = run_code(code)
        self.assertEqual(interp.global_env.get("count"), 5)
        self.assertEqual(interp.global_env.get("total"), 15)

    def test_for_in_and_lists(self):
        code = """
        let numbers = [1, 2, 3, 4]
        push(numbers, 5)
        let sum = 0
        for (num in numbers) {
            sum += num
        }
        """
        interp = run_code(code)
        self.assertEqual(interp.global_env.get("sum"), 15)

    def test_repeat_loop(self):
        code = """
        let hits = 0
        repeat (4) {
            hits += 2
        }
        """
        interp = run_code(code)
        self.assertEqual(interp.global_env.get("hits"), 8)

    def test_functions_and_recursion(self):
        code = """
        fn factorial(n) {
            if (n <= 1) {
                return 1
            }
            return n * factorial(n - 1)
        }
        let res = factorial(5)
        """
        interp = run_code(code)
        self.assertEqual(interp.global_env.get("res"), 120)

    def test_dictionaries_and_member_access(self):
        code = """
        let player = {
            x: 100,
            y: 200,
            speed: 5
        }
        player.x += player.speed
        """
        interp = run_code(code)
        p = interp.global_env.get("player")
        self.assertEqual(p["x"], 105)

    def test_collision_builtins(self):
        code = """
        let hit = collide_rect(10, 10, 20, 20, 15, 15, 20, 20)
        let miss = collide_rect(10, 10, 20, 20, 100, 100, 20, 20)
        let dist = distance(0, 0, 3, 4)
        """
        interp = run_code(code)
        self.assertTrue(interp.global_env.get("hit"))
        self.assertFalse(interp.global_env.get("miss"))
        self.assertEqual(interp.global_env.get("dist"), 5.0)

    def test_game_hooks_and_draw(self):
        code = """
        let player_x = 50
        setup {
            window("Test Game", 400, 300)
            player_x = 100
        }
        update {
            player_x += 10
        }
        draw {
            clear("black")
            rect(player_x, 50, 30, 30, "cyan")
        }
        """
        interp = run_code(code)
        interp.execute_setup()
        self.assertEqual(interp.window_width, 400)
        self.assertEqual(interp.window_height, 300)
        self.assertEqual(interp.global_env.get("player_x"), 100)

        interp.execute_update()
        self.assertEqual(interp.global_env.get("player_x"), 110)

        cmds = interp.execute_draw()
        self.assertEqual(len(cmds), 2)
        self.assertEqual(cmds[0]["type"], "clear")
        self.assertEqual(cmds[1]["type"], "rect")
        self.assertEqual(cmds[1]["x"], 110)

if __name__ == "__main__":
    unittest.main()
