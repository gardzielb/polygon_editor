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


def setup_x_symmetrically( p1: QPoint, p2: QPoint, mid_x: int, dist: float ):
	if p1.x() > p2.x():
		p1.setX( mid_x + dist )
		p2.setX( mid_x - dist )
	else:
		p1.setX( mid_x - dist )
		p2.setX( mid_x + dist )


def setup_y_symmetrically( p1: QPoint, p2: QPoint, mid_y: int, dist: float ):
	if p1.y() > p2.y():
		p1.setY( mid_y + dist )
		p2.setY( mid_y - dist )
	else:
		p1.setY( mid_y - dist )
		p2.setY( mid_y + dist )
