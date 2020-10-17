from typing import Tuple

from PyQt5.QtCore import QPoint


def get_line_equation( p1: QPoint, p2: QPoint ) -> Tuple[float, int]:
	dx = p1.x() - p2.x()
	if not dx:
		return 0, 0
	a = (p1.y() - p2.y()) / (p1.x() - p2.x())
	b = p1.y() - a * p1.x()
	return a, b
