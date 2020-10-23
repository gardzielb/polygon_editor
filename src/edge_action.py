from abc import ABC, abstractmethod

from src.edge import Edge
from src.edge_constraints import EdgeConstraint
from src.geo_utils import line_middle_point
from src.polygon import Polygon
from src.vertex import Vertex, VerticalEdgeVertexRelation, HorizontalEdgeVertexRelation, FixedEdgeLengthVertexRelation, \
	VertexRelation


class EdgeAction( ABC ):

	@abstractmethod
	def apply( self, edge: Edge ) -> bool:
		pass


class AddMiddlePointEdgeAction( EdgeAction ):

	def __init__( self, polygon: Polygon ):
		self.polygon = polygon

	def apply( self, edge: Edge ) -> bool:
		RemoveConstraintEdgeAction().apply( edge )

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


def try_set_relation( edge: Edge, relation: VertexRelation ) -> bool:
	if edge.constraint:
		return False

	v1 = edge.v1
	v2 = edge.v2
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
		if try_set_relation( edge, VerticalEdgeVertexRelation( edge.v1, edge.v2 ) ):
			edge.constraint = EdgeConstraint.VERTICAL
			return True
		return False


class HorizontalConstraintEdgeAction( EdgeAction ):

	def apply( self, edge: Edge ) -> bool:
		if try_set_relation( edge, HorizontalEdgeVertexRelation( edge.v1, edge.v2 ) ):
			edge.constraint = EdgeConstraint.HORIZONTAL
			return True
		return False


class FixedLengthConstraintEdgeAction( EdgeAction ):

	def __init__( self, length: int ):
		self.length = length

	def apply( self, edge: Edge ) -> bool:
		if try_set_relation( edge, FixedEdgeLengthVertexRelation( edge.v1, edge.v2, self.length ) ):
			edge.constraint = EdgeConstraint.FIXED_LENGTH
			return True
		return False


class RemoveConstraintEdgeAction( EdgeAction ):

	def apply( self, edge: Edge ) -> bool:
		if not edge.constraint:
			return True

		matching_relations = [rel for rel in edge.v1.relations if rel.constraint == edge.constraint]
		removed = [rel for rel in edge.v2.relations if rel in matching_relations]
		if len( removed ) != 1:
			return False

		edge.v1.relations.remove( removed[0] )
		edge.v2.relations.remove( removed[0] )

		edge.constraint = None
		return True
