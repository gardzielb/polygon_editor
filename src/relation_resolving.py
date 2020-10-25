from typing import Optional

from PyQt5.QtCore import QPoint

from src.geo_utils import solve_square_equation, circle_intersections, line_length


def resolve_length_vertical( p_length: QPoint, p_vertical: QPoint, p_moved: QPoint, length: int ) -> Optional[QPoint]:
	x0 = p_vertical.x()
	solution = solve_square_equation(
		a = 1, b = 2 * p_length.y(),
		c = p_length.y() ** 2 + (x0 - p_length.x()) ** 2 - length ** 2
	)

	if not solution:
		return None

	dist1 = abs( p_moved.y() - solution[0] )
	dist2 = abs( p_moved.y() - solution[1] )
	if dist1 <= dist2:
		return QPoint( x0, solution[0] )
	return QPoint( x0, solution[1] )


def resolve_length_horizontal(
		p_length: QPoint, p_horizontal: QPoint, p_moved: QPoint, length: int
) -> Optional[QPoint]:
	y0 = p_horizontal.y()
	solution = solve_square_equation(
		a = 1, b = 2 * p_length.x(),
		c = p_length.x() ** 2 + (y0 - p_length.y()) ** 2 - length ** 2
	)

	if not solution:
		return None

	dist1 = abs( p_moved.x() - solution[0] )
	dist2 = abs( p_moved.x() - solution[1] )
	if dist1 <= dist2:
		return QPoint( solution[0], y0 )
	return QPoint( solution[1], y0 )


def resolve_length_length( p1: QPoint, p2: QPoint, p_moved: QPoint, l1: int, l2: int ) -> Optional[QPoint]:
	solution = circle_intersections( mid1 = p1, r1 = l1, mid2 = p2, r2 = l2 )
	if not solution:
		return None

	dist1 = line_length( p_moved, solution[0] )
	dist2 = line_length( p_moved, solution[1] )
	if dist1 <= dist2:
		return solution[0]
	return solution[1]
