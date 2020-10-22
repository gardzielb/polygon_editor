from abc import ABC, abstractmethod
from math import sqrt
from typing import Tuple

from geo_utils import line_middle_point
from polygon import Polygon
from edge import Edge
from vertex import Vertex, VerticalEdgeVertexRelation, HorizontalEdgeVertexRelation, FixedEdgeLengthVertexRelation, \
	VertexObserver, VertexRelation


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

		new_vertex = Vertex( line_middle_point( edge.v1.point, edge.v2.point ) )

		v1_index = v2_index = -1
		for i in range( len( self.polygon.vertices ) ):
			vertex = self.polygon.vertices[i]
			if vertex == edge.v1:
				v1_index = i
			if vertex == edge.v2:
				v2_index = i

		if v1_index < 0 or v2_index < 0:
			return False

		# first and last vertex
		if abs( v1_index - v2_index ) == len( self.polygon.vertices ) - 1:
			self.polygon.vertices.append( new_vertex )
		else:
			self.polygon.vertices.insert( max( v1_index, v2_index ), new_vertex )

		self.polygon.edges.insert( e_index, Edge( edge.v1, new_vertex ) )
		self.polygon.edges.insert( e_index + 1, Edge( edge.v2, new_vertex ) )
		return True


def setup_x_symmetrically( edge: Edge, mid_x: int, dist: float = -1 ) -> Tuple[int, int]:
	if dist < 0:
		dist = edge.length / 2
	if edge.v1.x() > edge.v2.x():
		return int( mid_x + dist ), int( mid_x - dist )
	else:
		return int( mid_x - dist ), int( mid_x + dist )


def setup_y_symmetrically( edge: Edge, mid_y: int, dist: float = -1 ) -> Tuple[int, int]:
	if dist < 0:
		dist = edge.length / 2
	if edge.v1.y() > edge.v2.y():
		return int( mid_y + dist ), int( mid_y - dist )
	else:
		return int( mid_y + dist ), int( mid_y - dist )


def setup_observer( edge: Edge, relation: VertexRelation ):
	observer = VertexObserver( edge.v1, edge.v2, relation )
	edge.v1.move_observers.append( observer )
	edge.v2.move_observers.append( observer )


class VerticalConstraintEdgeAction( EdgeAction ):

	def apply( self, edge: Edge ) -> bool:
		mid_point = line_middle_point( edge.v1.point, edge.v2.point )
		y1, y2 = setup_y_symmetrically( edge, mid_y = mid_point.y() )
		edge.v1.move( mid_point.x(), y1 )
		edge.v2.move( mid_point.x(), y2 )
		setup_observer( edge, relation = VerticalEdgeVertexRelation() )
		return True


class HorizontalConstraintEdgeAction( EdgeAction ):

	def apply( self, edge: Edge ) -> bool:
		mid_point = line_middle_point( edge.v1.point, edge.v2.point )
		x1, x2 = setup_x_symmetrically( edge, mid_x = mid_point.x() )
		edge.v1.move( x1, mid_point.y() )
		edge.v2.move( x2, mid_point.y() )
		setup_observer( edge, relation = HorizontalEdgeVertexRelation() )
		return True


class FixedLengthConstraintEdgeAction( EdgeAction ):

	def __init__( self, length: int ):
		self.length = length

	def apply( self, edge: Edge ) -> bool:
		mid_point = line_middle_point( edge.v1.point, edge.v2.point )
		dx = self.length / sqrt( 1 + edge.a )
		dy = edge.a * dx
		x1, x2 = setup_x_symmetrically( edge, mid_x = mid_point.x(), dist = dx / 2 )
		y1, y2 = setup_y_symmetrically( edge, mid_y = mid_point.y(), dist = dy / 2 )
		edge.v1.move( x1, y1 )
		edge.v2.move( x2, y2 )
		setup_observer( edge, relation = FixedEdgeLengthVertexRelation( length = self.length ) )
		return True
