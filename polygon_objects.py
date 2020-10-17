from typing import Union

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from geo_utils import get_line_equation
from geometric_object import GeometricObject
from geometry_drawer import GeometryDrawer


class Vertex( GeometricObject ):
	RADIUS = 2
	HIGHLIGHT_PEN = QColor( 0, 200, 0 )

	def __init__( self, point: QPoint ):
		super().__init__()
		self.point = point

	def draw( self, drawer: GeometryDrawer ):
		radius = self.RADIUS
		prev_pen = drawer.pen()
		if self.highlight:
			drawer.set_pen( self.HIGHLIGHT_PEN )
			radius += 1
		drawer.draw_point( self.point, radius )
		drawer.set_pen( prev_pen )

	def move( self, dest_point: QPoint ):
		self.point.setX( dest_point.x() )
		self.point.setY( dest_point.y() )

	def is_hit( self, hit: QPoint ) -> bool:
		if abs( self.point.x() - hit.x() ) > self.RADIUS:
			return False
		return abs( self.point.y() - hit.y() ) <= self.RADIUS


class Edge( GeometricObject ):
	HIGHLIGHT_PEN = QColor( 255, 255, 0 )
	STROKE_WIDTH = 2

	def __init__( self, p1: QPoint, p2: QPoint ):
		super().__init__()
		self.move_origin: Union[QPoint, None] = None

		self.p1 = p1
		self.p2 = p2

		# line equation
		self.a, self.b = get_line_equation( p1, p2 )

	def draw( self, drawer: GeometryDrawer ):
		prev_pen = drawer.pen()
		if self.highlight:
			drawer.set_pen( self.HIGHLIGHT_PEN )
		drawer.draw_line( self.p1, self.p2 )
		drawer.set_pen( prev_pen )

	def post_move_update( self ):
		self.a, self.b = get_line_equation( self.p1, self.p2 )
		self.move_origin = None

	def move( self, dest_point: QPoint ):
		if self.move_origin:
			move_x = dest_point.x() - self.move_origin.x()
			move_y = dest_point.y() - self.move_origin.y()
			self.p1.setX( self.p1.x() + move_x )
			self.p1.setY( self.p1.y() + move_y )
			self.p2.setX( self.p2.x() + move_x )
			self.p2.setY( self.p2.y() + move_y )
		self.move_origin = dest_point

	def is_hit( self, hit: QPoint ) -> bool:
		if not min( self.p1.y(), self.p2.y() ) <= hit.y() <= max( self.p1.y(), self.p2.y() ):
			return False
		if not min( self.p1.x(), self.p2.x() ) <= hit.x() <= max( self.p1.x(), self.p2.x() ):
			return False
		if self.p1.x() == self.p2.x():
			return True
		return abs( hit.y() - (self.a * hit.x() + self.b) ) <= self.STROKE_WIDTH

	def is_line_intersecting( self, p1: QPoint, p2: QPoint ) -> bool:
		a, b = get_line_equation( p1, p2 )
		if self.a == a:
			return False

		x_cross = (b - self.b) / (self.a - a)
		y_cross = a * x_cross + b
		return self.is_hit( hit = QPoint( x_cross, y_cross ) )
