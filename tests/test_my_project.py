import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from my_project import TriangleCalculator


class TestTriangleClassification(unittest.TestCase):
    """Тесты классификации треугольника по сторонам."""

    def setUp(self):
        self.calc = TriangleCalculator()

    # ---------- Определение типа ----------

    def test_equilateral_triangle_is_detected(self):
        t, _ = self.calc.process("5", "5", "5")
        self.assertEqual(t, "равносторонний")

    def test_isosceles_triangle_two_equal_sides(self):
        t, _ = self.calc.process("5", "5", "8")
        self.assertEqual(t, "равнобедренный")

    def test_isosceles_triangle_other_pair(self):
        t, _ = self.calc.process("8", "5", "5")
        self.assertEqual(t, "равнобедренный")

    def test_scalene_triangle_is_detected(self):
        t, _ = self.calc.process("3", "4", "5")
        self.assertEqual(t, "разносторонний")

    def test_float_sides_scalene(self):
        t, _ = self.calc.process("2.5", "3.5", "4.5")
        self.assertEqual(t, "разносторонний")

    def test_equilateral_with_floats(self):
        t, _ = self.calc.process("1.5", "1.5", "1.5")
        self.assertEqual(t, "равносторонний")

    # ---------- Не треугольник ----------

    def test_zero_side_is_not_triangle(self):
        t, coords = self.calc.process("0", "5", "5")
        self.assertEqual(t, "не треугольник")
        self.assertEqual(coords, [(-1, -1)] * 3)

    def test_negative_side_is_not_triangle(self):
        t, coords = self.calc.process("-3", "4", "5")
        self.assertEqual(t, "не треугольник")
        self.assertEqual(coords, [(-1, -1)] * 3)

    def test_degenerate_triangle_sides_1_2_3(self):
        t, _ = self.calc.process("1", "2", "3")
        self.assertEqual(t, "не треугольник")

    def test_too_long_side_fails_inequality(self):
        t, _ = self.calc.process("1", "2", "10")
        self.assertEqual(t, "не треугольник")

    def test_all_sides_equal_zero(self):
        t, coords = self.calc.process("0", "0", "0")
        self.assertEqual(t, "не треугольник")
        self.assertEqual(coords, [(-1, -1)] * 3)

    # ---------- Нечисловые данные ----------

    def test_non_numeric_a_returns_empty_type(self):
        t, coords = self.calc.process("abc", "4", "5")
        self.assertEqual(t, "")
        self.assertEqual(coords, [(-2, -2)] * 3)

    def test_non_numeric_all_returns_empty_type(self):
        t, coords = self.calc.process("a", "b", "c")
        self.assertEqual(t, "")
        self.assertEqual(coords, [(-2, -2)] * 3)

    def test_none_value_returns_empty_type(self):
        t, coords = self.calc.process(None, "4", "5")
        self.assertEqual(t, "")
        self.assertEqual(coords, [(-2, -2)] * 3)

    def test_empty_string_returns_empty_type(self):
        t, coords = self.calc.process("", "4", "5")
        self.assertEqual(t, "")
        self.assertEqual(coords, [(-2, -2)] * 3)

    # ---------- Координаты ----------

    def test_vertices_count_is_three(self):
        _, coords = self.calc.process("3", "4", "5")
        self.assertEqual(len(coords), 3)

    def test_vertices_are_int_tuples(self):
        _, coords = self.calc.process("3", "4", "5")
        for pt in coords:
            self.assertIsInstance(pt, tuple)
            self.assertEqual(len(pt), 2)
            self.assertIsInstance(pt[0], int)
            self.assertIsInstance(pt[1], int)

    def test_vertices_fit_in_field_100x100(self):
        _, coords = self.calc.process("3", "4", "5")
        for x, y in coords:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 100)

    def test_vertices_for_equilateral_fit_in_field(self):
        _, coords = self.calc.process("7", "7", "7")
        for x, y in coords:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 100)

    def test_two_vertices_share_baseline_y(self):
        _, coords = self.calc.process("3", "4", "5")
        self.assertEqual(coords[0][1], coords[1][1])

    # ---------- Автономия ----------

    def test_two_calls_give_same_result(self):
        r1 = self.calc.process("3", "4", "5")
        r2 = self.calc.process("3", "4", "5")
        self.assertEqual(r1, r2)

    def test_non_numeric_does_not_break_next_call(self):
        self.calc.process("abc", "x", "y")
        t, coords = self.calc.process("3", "4", "5")
        self.assertEqual(t, "разносторонний")
        self.assertEqual(len(coords), 3)


if __name__ == "__main__":
    unittest.main()