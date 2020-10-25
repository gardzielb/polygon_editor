from math import sqrt
from typing import Tuple, Optional

from PyQt5.QtCore import QPoint


def get_line_equation( p1: QPoint, p2: QPoint ) -> Tuple[float, int]:
	dx = p1.x() - p2.x()
	if not dx:
		return 0, 0
	a = (p1.y() - p2.y()) / (p1.x() - p2.x())
	b = p1.y() - a * p1.x()
	return a, b


def line_length( p1: QPoint, p2: QPoint ) -> float:
	return sqrt( (p1.x() - p2.x()) ** 2 + (p1.y() - p2.y()) ** 2 )


def line_middle_point( p1: QPoint, p2: QPoint ) -> QPoint:
	x_mid = (p1.x() + p2.x()) / 2
	y_mid = (p1.y() + p2.y()) / 2
	return QPoint( x_mid, y_mid )


def circle_intersections( mid1: QPoint, r1: int, mid2: QPoint, r2: int ) -> Optional[Tuple[QPoint, QPoint]]:
	d = sqrt( (mid2.x() - mid1.x()) ** 2 + (mid2.y() - mid1.y()) ** 2 )

	# non intersecting
	if d > r1 + r2:
		return None
	# One circle within other
	if d < abs( r1 - r2 ):
		return None
	# coincident circles
	if d == 0 and r1 == r2:
		return None
	else:
		a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
		h = sqrt( r1 ** 2 - a ** 2 )
		x2 = mid1.x() + a * (mid2.x() - mid1.x()) / d
		y2 = mid1.y() + a * (mid2.y() - mid1.y()) / d
		x3 = x2 + h * (mid2.y() - mid1.y()) / d
		y3 = y2 - h * (mid2.x() - mid1.x()) / d

		x4 = x2 - h * (mid2.y() - mid1.y()) / d
		y4 = y2 + h * (mid2.x() - mid1.x()) / d

		return QPoint( x3, y3 ), QPoint( x4, y4 )


def solve_square_equation( a: float, b: float, c: float ) -> Optional[Tuple[float, float]]:
	delta = b ** 2 - 4 * a * c
	if delta < 0:
		return None

	delta_root = sqrt( delta )
	denominator = 2 * a

	return (-b - delta_root) / denominator, (-b + delta_root) / denominator
