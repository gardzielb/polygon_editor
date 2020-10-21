from abc import ABC, abstractmethod
from math import sqrt

from geo_utils import line_middle_point, setup_x_symmetrically, setup_y_symmetrically
from polygon import Polygon
from edge import Edge
from vertex import Vertex, VerticalEdgeVertexRelation, HorizontalEdgeVertexRelation, FixedEdgeLengthVertexRelation, \
	VertexObserver


class EdgeAction( ABC ):

	@abstractmethod
	def apply( self, edge: Edge ) -> bool:
		pass


class AddMiddlePointEdgeAction( EdgeAction ):

	def __init__( self, polygon: Polygon ):
		self.polygon = polygon

	def apply( self, edge: Edge ) -> bool:
		e_index = self.polygon.edges.index( edge )
		self.polygon.edges.remove( edge )

		new_point = line_middle_point( edge.p1, edge.p2 )

		v1_index = v2_index = -1
		for i in range( len( self.polygon.vertices ) ):
			point = self.polygon.vertices[i].point
			if point == edge.p1:
				v1_index = i
			if point == edge.p2:
				v2_index = i

		if v1_index < 0 or v2_index < 0:
			return False

		# first and last vertex
		if abs( v1_index - v2_index ) == len( self.polygon.vertices ) - 1:
			self.polygon.vertices.append( Vertex( new_point ) )
		else:
			self.polygon.vertices.insert( max( v1_index, v2_index ), Vertex( new_point ) )

		self.polygon.edges.insert( e_index, Edge( edge.p1, new_point ) )
		self.polygon.edges.insert( e_index + 1, Edge( edge.p2, new_point ) )
		return True


class VerticalConstraintEdgeAction( EdgeAction ):

	def apply( self, edge: Edge ) -> bool:
		mid_point = line_middle_point( edge.p1, edge.p2 )
		edge.p1.setX( mid_point.x() )
		edge.p2.setX( mid_point.x() )
		setup_y_symmetrically( edge.p1, edge.p2, mid_y = mid_point.y(), dist = edge.length / 2 )
		return True


class HorizontalConstraintEdgeAction( EdgeAction ):

	def apply( self, edge: Edge ) -> bool:
		mid_point = line_middle_point( edge.p1, edge.p2 )
		edge.p1.setY( mid_point.y() )
		edge.p2.setY( mid_point.y() )
		setup_x_symmetrically( edge.p1, edge.p2, mid_x = mid_point.x(), dist = edge.length / 2 )
		return True


class FixedLengthConstraintEdgeAction( EdgeAction ):

	def __init__( self, length: float ):
		self.length = length

	def apply( self, edge: Edge ) -> bool:
		mid_point = line_middle_point( edge.p1, edge.p2 )
		dx = self.length / sqrt( 1 + edge.a )
		dy = edge.a * dx
		setup_x_symmetrically( edge.p1, edge.p2, mid_x = mid_point.x(), dist = dx / 2 )
		setup_y_symmetrically( edge.p1, edge.p2, mid_y = mid_point.y(), dist = dy / 2 )
		return True
