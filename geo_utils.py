from math import sqrt
from typing import Tuple

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
