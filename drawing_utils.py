from typing import Callable

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter


def draw_line_bresenham(
		p1: QPoint, p2: QPoint, painter: QPainter, transform: Callable[[QPoint], QPoint] = lambda p: p
):
	dx = p2.x() - p1.x()
	dy = p2.y() - p1.y()
	d = 2 * dy - dx
	incr_e = 2 * dy
	incr_ne = 2 * (dy - dx)
	x = p1.x()
	y = p1.y()
	painter.drawPoint( x, y )

	while x < p2.x():
		if d < 0:  # choose E
			d += incr_e
		else:  # choose NE
			d += incr_ne
			y += 1
		x += 1
		painter.drawPoint( transform( QPoint( x, y ) ) )
