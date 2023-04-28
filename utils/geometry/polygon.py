from typing import List

from utils.geometry.point import Point
from errors import GenerateConvexPolygonError


class Polygon:
    """
    A convex polygon class
    """
    def __init__(self, points: List[Point]) -> None:
        if len(points) < 3:
            raise GenerateConvexPolygonError('The Point is not')
        self._points = points

    @property
    def points(self):
        """
        Get all the points from this convex polygon
        """
        return self._points

    @property
    def area(self) -> float:
        """
        Get the area of this convex polygon
        """
        res = 0
        points = self.points
        first_point, second_point = points[0], points[1]
        for third_point in points[2:]:
            res += abs(
                first_point[0] * (second_point[1] - third_point[1])
                + second_point[0] * (third_point[1] - first_point[1])
                + third_point[0] * (first_point[1] - second_point[1])
            ) / 2
            second_point = third_point
        return res
    
    def contains(self, point: Point) -> bool:
        """
        Whether the point is in the polygon
        """
        point_x = point.x
        point_y = point.y
        is_in = False
        polygon_points = self.points
        previous_point = polygon_points[-1]
        for current_point in polygon_points:
            if (previous_point.x == point_x and previous_point.y == point_y) or (current_point.x == point_x and current_point.y == point_y):
                is_in = True
                break
            if min(previous_point.y, current_point.y) < point_y <= max(previous_point.y, current_point.y):
                x = previous_point.x + (point_y - previous_point.y) * (current_point.x - previous_point.x) / (current_point.y - previous_point.y)
                if x == point.x: # on the edge
                    is_in = True
                    break
                if x > point_x:
                    is_in = not is_in
            previous_point = current_point
        return is_in