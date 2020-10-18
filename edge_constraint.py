from abc import ABC, abstractmethod
from math import sqrt

from PyQt5.QtCore import QPoint

from geo_utils import line_middle_point, setup_x_symmetrically, setup_y_symmetrically
from polygon_objects import Edge


class EdgeConstraint( ABC ):

	@abstractmethod
	def apply( self, edge: Edge ):
		pass


class VerticalEdgeConstraint( EdgeConstraint ):

	def apply( self, edge: Edge ):
		mid_point = line_middle_point( edge.p1, edge.p2 )
		edge.p1.setX( mid_point.x() )
		edge.p2.setX( mid_point.x() )
		setup_y_symmetrically( edge.p1, edge.p2, mid_y = mid_point.y(), dist = edge.length / 2 )


class HorizontalEdgeConstraint( EdgeConstraint ):

	def apply( self, edge: Edge ):
		mid_point = line_middle_point( edge.p1, edge.p2 )
		edge.p1.setY( mid_point.y() )
		edge.p2.setY( mid_point.y() )
		setup_x_symmetrically( edge.p1, edge.p2, mid_x = mid_point.x(), dist = edge.length / 2 )


class LengthEdgeConstraint( EdgeConstraint ):

	def __init__( self, length: float ):
		self.length = length

	def apply( self, edge: Edge ):
		mid_point = line_middle_point( edge.p1, edge.p2 )
		dx = self.length / sqrt( 1 + edge.a )
		dy = edge.a * dx
		setup_x_symmetrically( edge.p1, edge.p2, mid_x = mid_point.x(), dist = dx / 2 )
		setup_y_symmetrically( edge.p1, edge.p2, mid_y = mid_point.y(), dist = dy / 2 )
