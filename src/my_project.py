import logging
import math


class TriangleCalculator:
    FIELD_SIZE = 100

    def process(self, a_raw, b_raw, c_raw):
        # 1. Парсинг
        try:
            a, b, c = float(a_raw), float(b_raw), float(c_raw)
        except (ValueError, TypeError) as ex:
            logging.warning(f"Нечисловые данные: A={a_raw!r}, B={b_raw!r}, C={c_raw!r}. {ex}")
            return "", [(-2, -2)] * 3

        # 2. Положительность
        if a <= 0 or b <= 0 or c <= 0:
            logging.warning(f"Стороны должны быть > 0: A={a}, B={b}, C={c}")
            return "не треугольник", [(-1, -1)] * 3

        # 3. Неравенство треугольника
        if not (a + b > c and a + c > b and b + c > a):
            logging.warning(f"Треугольник не существует: A={a}, B={b}, C={c}")
            return "не треугольник", [(-1, -1)] * 3

        # 4. Тип
        t_type = self._classify(a, b, c)
        logging.debug(f"Тип: {t_type}")

        # 5. Координаты
        try:
            vertices = self._compute_vertices(a, b, c)
        except Exception:
            logging.exception("Ошибка при расчёте координат:")
            return t_type, [(-1, -1)] * 3

        return t_type, vertices

    @staticmethod
    def _classify(a, b, c):
        eps = 1e-9
        if abs(a - b) < eps and abs(b - c) < eps:
            return "равносторонний"
        if abs(a - b) < eps or abs(b - c) < eps or abs(a - c) < eps:
            return "равнобедренный"
        return "разносторонний"

    def _compute_vertices(self, a, b, c):
        # A(0,0), B(c,0), C — через теорему косинусов
        cos_a = (b * b + c * c - a * a) / (2 * b * c)
        cos_a = max(-1.0, min(1.0, cos_a))
        cx, cy = b * cos_a, b * math.sqrt(max(0.0, 1 - cos_a ** 2))

        pts = [(0.0, 0.0), (c, 0.0), (cx, cy)]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        min_x, min_y = min(xs), min(ys)
        w, h = max(xs) - min_x, max(ys) - min_y

        pad = 10
        free = self.FIELD_SIZE - 2 * pad
        scale = min(
            free / w if w > 0 else float("inf"),
            free / h if h > 0 else float("inf"),
        )
        if scale == float("inf"):
            scale = 1.0

        def to_px(p):
            ox = (self.FIELD_SIZE - w * scale) / 2
            oy = (self.FIELD_SIZE - h * scale) / 2
            return int(round((p[0] - min_x) * scale + ox)), \
                   int(round((p[1] - min_y) * scale + oy))

        result = [to_px(p) for p in pts]
        logging.debug(f"Вершины: {result}")
        return result