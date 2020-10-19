from typing import List

from PyQt5.QtCore import QPoint

from edge_dialog import EdgeDialog
from geometry_visitor import GeometryObjectVisitor
from polygon import Polygon
from polygon_objects import Vertex, Edge


def __opposite_point__( edge: Edge, vertex: Vertex ) -> QPoint:
	if edge.p1 == vertex.point:
		return edge.p2
	else:
		return edge.p1


class EditGeometryObjectVisitor( GeometryObjectVisitor ):

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
		dialog = EdgeDialog()
		if not dialog.exec_():
			return True
		action = dialog.get_action( self.polygon )
		return action.apply( edge )

	def visit_polygon( self, polygon: Polygon ) -> bool:
		self.polygon_list.remove( polygon )
		return True
