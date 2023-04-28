import math

import numpy as np
from errors import GenerateConvexPolygonError
from utils.geometry.point import Point
from utils.geometry.polygon import Polygon


def generate_vectors(point_pool: list) -> list:
    """
    generate vectors
    """
    min_point = point_pool[0]
    max_point = point_pool[-1]

    last_top, last_bot = min_point, min_point
    vectors = []
    for item in point_pool[1:-1]:
        if np.random.choice([True, False]):
            vectors.append(item - last_top)
            last_top = item
        else:
            vectors.append(last_bot - item)
            last_bot = item
    vectors.append(max_point - last_top)
    vectors.append(last_bot - max_point)
    np.random.shuffle(vectors)
    return vectors

def generate_convex_polygon_randomly(n: int) -> Polygon:
    """
    Generate a convex polygon randomly.
    Reference: https://cglab.ca/~sander/misc/ConvexGeneration/convex.html
    """
    if n < 3:
        raise GenerateConvexPolygonError('The n must large than or equal to 3')

    x_pool = np.random.randint(0, 100, n)
    y_pool = np.random.randint(0, 100, n)

    x_pool.sort()
    y_pool.sort()

    x_vectors = generate_vectors(x_pool)
    y_vectors = generate_vectors(y_pool)

    vectors = list(zip(x_vectors, y_vectors))
    vectors.sort(key=lambda x: math.atan2(x[0], x[1]))

    x_coordinate = y_coordinate = 0
    min_polygon_x = min_polygon_y = 0
    points = []
    for i in range(n):
        points.append((x_coordinate, y_coordinate))
        x_coordinate += vectors[i][0]
        y_coordinate += vectors[i][1]
        min_polygon_x = min(min_polygon_x, x_coordinate)
        min_polygon_y = min(min_polygon_y, y_coordinate)

    x_shift = x_pool[0] - min_polygon_x
    y_shift = y_pool[0] - min_polygon_y

    points = [Point(item[0] + x_shift, item[1] + y_shift) for item in points]
    return Polygon(points)

def polygon_area_with_monte_carlo_method(polygon: Polygon) -> float:
    """
    calculate a polygon with the monte carlo method
    """
    polygon_points_x = [point.x for point in polygon.points]
    polygon_points_y = [point.y for point in polygon.points]
    min_x = min(polygon_points_x)
    max_x = max(polygon_points_x)
    min_y = min(polygon_points_y)
    max_y = max(polygon_points_y)

    # get the area of the square according to the bounds of the polygon
    square_area = (max_x - min_x) * (max_y - min_y)

    random_point_count = 100000
    in_polygon_count = 0
    random_points_x = np.random.randint(min_x, max_x, random_point_count)
    random_points_y = np.random.randint(min_y, max_y, random_point_count)
    for i in range(random_point_count):
        # randomly generate a point in the square
        random_point = Point(random_points_x[i], random_points_y[i])
        if polygon.contains(random_point):
            in_polygon_count += 1
    return round((in_polygon_count / random_point_count) * square_area, 2)


convex_polygon = generate_convex_polygon_randomly(np.random.randint(3, 100))
standard_math_res = convex_polygon.area
monte_carlo_res = polygon_area_with_monte_carlo_method(convex_polygon)

print("The area of a convex polygon is:")
print(f"calcuated by the standard math method: {standard_math_res}")
print(f"calcuated by the monto carlo method: {monte_carlo_res}")
