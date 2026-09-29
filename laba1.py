import logging
import sys
from triangle import TriangleCalculator

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | [%(levelname)-7s] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/file_txt.log", encoding="utf-8"),
    ],
)


def main():
    logging.info("Приложение запущено")
    calc = TriangleCalculator()

    a = input("Введите сторону A: ")
    b = input("Введите сторону B: ")
    c = input("Введите сторону C: ")
    logging.info(f"Входные данные: A={a}, B={b}, C={c}")

    try:
        t_type, vertices = calc.process(a, b, c)
        logging.info(f"Результат: тип={t_type!r}, вершины={vertices}")
        print("Тип треугольника:", t_type or "(пусто)")
        print("Координаты вершин:", vertices)

    except Exception:
        logging.exception("Непредвиденная ошибка:")
        print("Ошибка при обработке данных")


if __name__ == "__main__":
    main()