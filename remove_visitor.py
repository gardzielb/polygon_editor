from typing import List

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QMenu

from edge_constraint import VerticalEdgeConstraint, HorizontalEdgeConstraint, LengthEdgeConstraint
from geo_utils import line_middle_point
from geometry_visitor import GeometryObjectVisitor
from polygon import Polygon
from polygon_objects import Vertex, Edge


def __opposite_point__( edge: Edge, vertex: Vertex ) -> QPoint:
	if edge.p1 == vertex.point:
		return edge.p2
	else:
		return edge.p1


class RemoveGeometryObjectVisitor( GeometryObjectVisitor ):

	def __init__( self, polygon: Polygon, polygon_list: List[Polygon] ):
		self.polygon = polygon
		self.polygon_list = polygon_list

	def visit_vertex( self, vertex: Vertex ) -> bool:
		if len( self.polygon.vertices ) == 3:
			return False
		self.polygon.vertices.remove( vertex )

		del_edges = [e for e in self.polygon.edges if e.p1 == vertex.point or e.p2 == vertex.point]
		p1 = __opposite_point__( del_edges[0], vertex )
		p2 = __opposite_point__( del_edges[1], vertex )

		del_index = self.polygon.edges.index( del_edges[0] )
		for edge in del_edges:
			self.polygon.edges.remove( edge )

		self.polygon.edges.insert( del_index, Edge( p1, p2 ) )
		return True

	def visit_edge( self, edge: Edge ) -> bool:
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

	def visit_polygon( self, polygon: Polygon ) -> bool:
		self.polygon_list.remove( polygon )
		return True
