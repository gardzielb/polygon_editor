from __future__ import annotations

import math
from typing import Callable, Optional

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter
from abc import ABC, abstractmethod

from src.geo_utils import get_line_equation


def draw_pixel_opacity( p: QPoint, painter: QPainter, opacity: float ):
	painter.setOpacity( 1 - opacity )
	painter.drawPoint( p )


def draw_line_wu(
		p1: QPoint, p2: QPoint, painter: QPainter, transform: Callable[[QPoint], QPoint] = lambda p: p
):
	prev_opacity = painter.opacity()
	y = float( p1.y() )
	m, _ = get_line_equation( p1, p2 )

	for x in range( p1.x(), p2.x() + 1 ):
		c1 = y - math.floor( y )
		c2 = 1 - c1
		pixel1 = transform( QPoint( x, math.floor( y ) ) )
		pixel2 = transform( QPoint( x, math.ceil( y ) ) )
		draw_pixel_opacity( pixel1, painter, opacity = c1 )
		draw_pixel_opacity( pixel2, painter, opacity = c2 )
		y += m

	painter.setOpacity( prev_opacity )


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


def draw_line_qt(
		p1: QPoint, p2: QPoint, painter: QPainter, transform: Callable[[QPoint], QPoint] = lambda p: p
):
	painter.drawLine( transform( p1 ), transform( p2 ) )


class LineDrawer( ABC ):
	def __init__( self, draw_line_function: Callable ):
		self.next: Optional[LineDrawer] = None
		self.draw_line_function = draw_line_function

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
			self.draw_line_function( p1, p2, painter )
			return True
		return False


class SteepIncreaseLineDrawer( LineDrawer ):
	def try_draw_line( self, p1: QPoint, p2: QPoint, painter: QPainter ) -> bool:
		dx = p2.x() - p1.x()
		dy = p2.y() - p1.y()
		b = p1.y() - p1.x()
		if 0 <= dx <= dy:
			def transform( p: QPoint ):
				return QPoint( p.y() - b, p.x() + b )

			self.draw_line_function( p1, transform( p2 ), painter, transform )
			return True
		return False


class GentleDecreaseLineDrawer( LineDrawer ):
	def try_draw_line( self, p1: QPoint, p2: QPoint, painter: QPainter ) -> bool:
		dx = p2.x() - p1.x()
		dy = p2.y() - p1.y()
		if 0 <= -dy <= dx:
			def transform( p: QPoint ):
				return QPoint( p.x(), p1.y() - (p.y() - p1.y()) )

			self.draw_line_function( p1, transform( p2 ), painter, transform = transform )
			return True
		return False


class SteepDecreaseLineDrawer( LineDrawer ):
	def try_draw_line( self, p1: QPoint, p2: QPoint, painter: QPainter ) -> bool:
		dx = p2.x() - p1.x()
		dy = p2.y() - p1.y()
		b = p1.y() - p1.x()
		if 0 <= dx <= -dy:
			p2_trans = QPoint( 2 * p1.y() - p2.y() - b, p2.x() + b )
			self.draw_line_function(
				p1, p2_trans, painter, transform = lambda p: QPoint( p.y() - b, p1.y() - (p.x() + b - p1.y()) )
			)
			return True
		return False


def create_line_drawer_chain( draw_line_function: Callable ) -> LineDrawer:
	chain = GentleIncreaseLineDrawer( draw_line_function )
	chain.set_next( SteepIncreaseLineDrawer( draw_line_function ) ) \
		.set_next( GentleDecreaseLineDrawer( draw_line_function ) ) \
		.set_next( SteepDecreaseLineDrawer( draw_line_function ) )
	return chain

