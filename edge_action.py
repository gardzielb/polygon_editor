from abc import ABC, abstractmethod

from edge import Edge
from geo_utils import line_middle_point
from polygon import Polygon
from vertex import Vertex, VerticalEdgeVertexRelation, HorizontalEdgeVertexRelation, FixedEdgeLengthVertexRelation, \
	VertexRelation


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


def try_set_relation( v1: Vertex, v2: Vertex, relation: VertexRelation ) -> bool:
	if relation.can_allow_move( sender = v1, dest_x = v1.x(), dest_y = v1.y(), initiator = v1 ):
		relation.correct( sender = v1 )
	elif relation.can_allow_move( sender = v2, dest_x = v2.x(), dest_y = v2.y(), initiator = v2 ):
		relation.correct( sender = v2 )
	else:
		return False

	v1.relations.append( relation )
	v2.relations.append( relation )
	return True


class VerticalConstraintEdgeAction( EdgeAction ):

	def apply( self, edge: Edge ) -> bool:
		return try_set_relation( edge.v1, edge.v2, VerticalEdgeVertexRelation( edge.v1, edge.v2 ) )


class HorizontalConstraintEdgeAction( EdgeAction ):

	def apply( self, edge: Edge ) -> bool:
		return try_set_relation( edge.v1, edge.v2, HorizontalEdgeVertexRelation( edge.v1, edge.v2 ) )


class FixedLengthConstraintEdgeAction( EdgeAction ):

	def __init__( self, length: int ):
		self.length = length

	def apply( self, edge: Edge ) -> bool:
		return try_set_relation( edge.v1, edge.v2, FixedEdgeLengthVertexRelation( edge.v1, edge.v2, self.length ) )
