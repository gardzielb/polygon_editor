from typing import Union

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from geo_utils import get_line_equation, line_length
from geometry_drawer import GeometryDrawer
from geometry_object import GeometryObject
from geometry_visitor import GeometryObjectVisitor
from vertex import Vertex


class Edge( GeometryObject ):
	HIGHLIGHT_PEN = QColor( 255, 255, 0 )
	STROKE_WIDTH = 2

	def __init__( self, v1: Vertex, v2: Vertex ):
		super().__init__()
		self.move_origin: Union[QPoint, None] = None

		self.v1 = v1
		self.v2 = v2

		# line equation
		self.a, self.b = get_line_equation( v1.point, v2.point )
		self.length = line_length( v1.point, v2.point )

	def draw( self, drawer: GeometryDrawer ):
		prev_pen = drawer.pen()
		if self.highlight:
			drawer.set_pen( self.HIGHLIGHT_PEN )
		drawer.draw_line( self.v1.point, self.v2.point )
		drawer.set_pen( prev_pen )

	def move( self, dest_x: int, dest_y: int ):
		if self.move_origin:
			move_x = dest_x - self.move_origin.x()
			move_y = dest_y - self.move_origin.y()
			dest1 = (self.v1.x() + move_x, self.v1.y() + move_y)
			dest2 = (self.v2.x() + move_x, self.v2.y() + move_y)
			self.v1.move( dest1[0], dest1[1] )
			self.v2.move( dest2[0], dest2[1] )
		self.move_origin = QPoint( dest_x, dest_y )

	def is_hit( self, hit: QPoint ) -> bool:
		if not min( self.v1.y(), self.v2.y() ) <= hit.y() <= max( self.v1.y(), self.v2.y() ):
			return False
		if not min( self.v1.x(), self.v2.x() ) <= hit.x() <= max( self.v1.x(), self.v2.x() ):
			return False
		if self.v1.x() == self.v2.x():
			return True
		return abs( hit.y() - (self.a * hit.x() + self.b) ) <= self.STROKE_WIDTH

	def accept_visitor( self, visitor: GeometryObjectVisitor ) -> bool:
		return visitor.visit_edge( edge = self )

	def is_line_intersecting( self, v1: QPoint, v2: QPoint ) -> bool:
		a, b = get_line_equation( v1, v2 )
		if self.a == a:
			return False

		x_cross = (b - self.b) / (self.a - a)
		y_cross = a * x_cross + b
		return self.is_hit( hit = QPoint( x_cross, y_cross ) )

	def post_move_update( self ):
		self.a, self.b = get_line_equation( self.v1.point, self.v2.point )
		self.move_origin = None
		self.length = line_length( self.v1.point, self.v2.point )
