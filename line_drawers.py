from __future__ import annotations

from typing import Union

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter
from abc import ABC, abstractmethod

from drawing_utils import draw_line_bresenham


class LineDrawer( ABC ):
	def __init__( self ):
		self.next: Union[None, LineDrawer] = None

	def set_next( self, next_in_chain: LineDrawer ) -> LineDrawer:
		self.next = next_in_chain
		return self.next

	def draw_line( self, p1: QPoint, p2: QPoint, painter: QPainter ):
		if self.try_draw_line( p1, p2, painter ):
			return
		if not self.next:
			raise Exception( 'End of line drawing chain' )
		self.next.draw_line( p1, p2, painter )

	@abstractmethod
	def try_draw_line( self, p1: QPoint, p2: QPoint, painter: QPainter ) -> bool:
		return False


class GentleIncreaseLineDrawer( LineDrawer ):
	def try_draw_line( self, p1: QPoint, p2: QPoint, painter: QPainter ) -> bool:
		dx = p2.x() - p1.x()
		dy = p2.y() - p1.y()
		if 0 <= dy <= dx:
			draw_line_bresenham( p1, p2, painter )
			return True
		return False


class SteepIncreaseLineDrawer( LineDrawer ):
	def try_draw_line( self, p1: QPoint, p2: QPoint, painter: QPainter ) -> bool:
		dx = p2.x() - p1.x()
		dy = p2.y() - p1.y()
		b = p1.y() - p1.x()
		if 0 <= dx <= dy:
			transform = lambda p: QPoint( p.y() - b, p.x() + b )
			draw_line_bresenham( p1, transform( p2 ), painter, transform )
			return True
		return False


class GentleDecreaseLineDrawer( LineDrawer ):
	def try_draw_line( self, p1: QPoint, p2: QPoint, painter: QPainter ) -> bool:
		dx = p2.x() - p1.x()
		dy = p2.y() - p1.y()
		if 0 <= -dy <= dx:
			transform = lambda p: QPoint( p.x(), p1.y() - (p.y() - p1.y()) )
			draw_line_bresenham( p1, transform( p2 ), painter, transform = transform )
			return True
		return False


class SteepDecreaseLineDrawer( LineDrawer ):
	def try_draw_line( self, p1: QPoint, p2: QPoint, painter: QPainter ) -> bool:
		dx = p2.x() - p1.x()
		dy = p2.y() - p1.y()
		b = p1.y() - p1.x()
		if 0 <= dx <= -dy:
			p2_trans = QPoint( 2 * p1.y() - p2.y() - b, p2.x() + b )
			draw_line_bresenham(
				p1, p2_trans, painter, transform = lambda p: QPoint( p.y() - b, p1.y() - (p.x() + b - p1.y()) )
			)
			return True
		return False
