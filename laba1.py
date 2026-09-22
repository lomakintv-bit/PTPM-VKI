import math

def check_triangle(a, b, c):
    if a + b <= c or a + c <= b or b + c <= a:
        return "не треугольник"

    if a == b == c:
        return "равносторонний"
    elif a == b or a == c or b == c:
        return "равнобедренный"
    else:
        return "разносторонний"


def get_coordinates(a, b, c, triangle_type):
    if triangle_type == "не треугольник":
        return [(-1, -1), (-1, -1), (-1, -1)]

    max_side = max(a, b, c)
    scale = 80.0 / max_side

    a_scaled = a * scale
    b_scaled = b * scale
    c_scaled = c * scale

    x1, y1 = 10, 90

    x2 = x1 + c_scaled
    y2 = y1

    cos_A = (b_scaled ** 2 + c_scaled ** 2 - a_scaled ** 2) / (2 * b_scaled * c_scaled)


    x3 = x1 + b_scaled * cos_A
    y3 = y1 - b_scaled * math.sqrt(1 - cos_A ** 2)

    return [(int(x1), int(y1)), (int(x2), int(y2)), (int(x3), int(y3))]


def main():
    lines = []
    for i in range(3):
        lines.append(input("Введите число: "))

    numbers = []
    for line in lines:
        try:
            num = float(line)
            if num <= 0:
                print("")
                print([(-1, -1), (-1, -1), (-1, -1)])
                return
            numbers.append(num)
        except ValueError:
            print("")
            print([(-2, -2), (-2, -2), (-2, -2)])
            return

    a, b, c = numbers

    triangle_type = check_triangle(a, b, c)
    coords = get_coordinates(a, b, c, triangle_type)

    print(triangle_type)
    print(coords)

main()