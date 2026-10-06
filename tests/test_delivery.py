import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import delivery_service as ds


class TestDeliveryInputValidation(unittest.TestCase):
    """Проверки границ входных данных."""

    def test_weight_below_minimum_returns_error(self):
        cost, date = ds.calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_at_minimum_is_accepted(self):
        cost, date = ds.calculate_delivery_cost(0.1, 100, "обычный")
        self.assertNotEqual(cost, -1)

    def test_weight_at_maximum_50_is_accepted(self):
        cost, date = ds.calculate_delivery_cost(50.0, 100, "обычный")
        self.assertNotEqual(cost, -1)

    def test_weight_above_maximum_returns_error(self):
        cost, date = ds.calculate_delivery_cost(50.1, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_distance_zero_returns_error(self):
        cost, _ = ds.calculate_delivery_cost(5, 0, "обычный")
        self.assertEqual(cost, -1)

    def test_distance_at_maximum_5000_is_accepted(self):
        cost, _ = ds.calculate_delivery_cost(5, 5000, "обычный")
        self.assertNotEqual(cost, -1)

    def test_distance_above_maximum_returns_error(self):
        cost, _ = ds.calculate_delivery_cost(5, 5001, "обычный")
        self.assertEqual(cost, -1)

    def test_unknown_package_type_returns_error(self):
        cost, _ = ds.calculate_delivery_cost(5, 100, "жидкий")
        self.assertEqual(cost, -1)

    def test_empty_package_type_returns_error(self):
        cost, _ = ds.calculate_delivery_cost(5, 100, "")
        self.assertEqual(cost, -1)


class TestDeliveryBaseCost(unittest.TestCase):
    """Базовая тарифная сетка."""

    def test_base_tariff_for_light_short_delivery(self):
        # weight=1 (<=5), distance=100 -> 200 + 100*5 = 700
        cost, _ = ds.calculate_delivery_cost(1, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_distance_multiplied_by_5(self):
        cost100, _ = ds.calculate_delivery_cost(1, 100, "обычный")
        cost200, _ = ds.calculate_delivery_cost(1, 200, "обычный")
        self.assertEqual(cost200 - cost100, 500)

    def test_base_cost_200_applied(self):
        # distance=1 -> 200 + 5 = 205
        cost, _ = ds.calculate_delivery_cost(1, 1, "обычный")
        self.assertEqual(cost, 205)


class TestDeliveryWeightCoefficients(unittest.TestCase):
    """Весовые коэффициенты 1.2 и 1.5."""

    def test_weight_below_5_no_coefficient(self):
        # 5.0 не должно получать коэффициент (граница вниз)
        cost, _ = ds.calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_weight_above_5_gets_1_2(self):
        # weight=5.1 -> (200+500)*1.2 = 840
        cost, _ = ds.calculate_delivery_cost(5.1, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_weight_at_19_9_gets_1_2(self):
        cost, _ = ds.calculate_delivery_cost(19.9, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_weight_at_20_gets_1_5(self):
        cost, _ = ds.calculate_delivery_cost(20.0, 100, "обычный")
        self.assertEqual(cost, int(700 * 1.5))

    def test_weight_at_50_gets_1_5(self):
        cost, _ = ds.calculate_delivery_cost(50.0, 100, "обычный")
        self.assertEqual(cost, int(700 * 1.5))


class TestDeliveryPackageType(unittest.TestCase):
    """Надбавки за тип посылки."""

    def test_fragile_adds_300(self):
        normal, _ = ds.calculate_delivery_cost(1, 100, "обычный")
        fragile, _ = ds.calculate_delivery_cost(1, 100, "хрупкий")
        self.assertEqual(fragile - normal, 300)

    def test_dangerous_adds_1000(self):
        normal, _ = ds.calculate_delivery_cost(1, 100, "обычный")
        dangerous, _ = ds.calculate_delivery_cost(1, 100, "опасный")
        self.assertEqual(dangerous - normal, 1000)

    def test_fragile_with_heavy_weight(self):
        # (200+500)*1.2 + 300 = 1140
        cost, _ = ds.calculate_delivery_cost(10, 100, "хрупкий")
        self.assertEqual(cost, 1140)


class TestDeliveryExpress(unittest.TestCase):
    """Экспресс-доставка."""

    def test_express_is_more_expensive_than_normal(self):
        normal, _ = ds.calculate_delivery_cost(1, 100, "обычный", is_express=False)
        express, _ = ds.calculate_delivery_cost(1, 100, "обычный", is_express=True)
        self.assertGreater(express, normal, "Экспресс должен быть дороже обычной доставки")

    def test_express_multiplier_is_1_5(self):
        normal, _ = ds.calculate_delivery_cost(1, 100, "обычный")
        express, _ = ds.calculate_delivery_cost(1, 100, "обычный", is_express=True)
        self.assertEqual(express, int(normal * 1.5))


class TestDeliveryDate(unittest.TestCase):
    """Дата доставки."""

    def test_delivery_date_format(self):
        _, date = ds.calculate_delivery_cost(1, 100, "обычный")
        self.assertRegex(date, r"^\d{4}-\d{2}-\d{2}$")

    def test_short_distance_takes_at_least_one_day(self):
        # Базовая дата 2026-09-03
        _, date = ds.calculate_delivery_cost(1, 100, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_distance_1000_takes_two_days(self):
        _, date = ds.calculate_delivery_cost(1, 1000, "обычный")
        self.assertEqual(date, "2026-09-05")

    def test_express_short_distance_takes_at_least_one_day(self):
        # Даже экспресс не может доставить в тот же день
        _, date = ds.calculate_delivery_cost(1, 100, "обычный", is_express=True)
        self.assertNotEqual(date, "2026-09-03", "Экспресс не может доставить за 0 дней")

    def test_express_is_faster_than_normal(self):
        _, normal_date = ds.calculate_delivery_cost(1, 2000, "обычный")
        _, express_date = ds.calculate_delivery_cost(1, 2000, "обычный", is_express=True)
        self.assertLess(express_date, normal_date)


class TestDeliveryAutonomy(unittest.TestCase):
    """Автономия тестов."""

    def test_repeated_calls_give_same_result(self):
        r1 = ds.calculate_delivery_cost(10, 500, "хрупкий", True)
        r2 = ds.calculate_delivery_cost(10, 500, "хрупкий", True)
        self.assertEqual(r1, r2)

    def test_error_does_not_break_next_call(self):
        ds.calculate_delivery_cost(-5, -5, "нет")
        cost, _ = ds.calculate_delivery_cost(1, 100, "обычный")
        self.assertEqual(cost, 700)


if __name__ == "__main__":
    unittest.main()