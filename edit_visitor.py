from typing import List

from edge import Edge
from edge_dialog import EdgeDialog
from geometry_visitor import GeometryObjectVisitor
from polygon import Polygon
from vertex import Vertex


def __opposite_vertex__( edge: Edge, vertex: Vertex ) -> Vertex:
	if edge.v1 == vertex:
		return edge.v2
	else:
		return edge.v1


class EditGeometryObjectVisitor( GeometryObjectVisitor ):

	def __init__( self, polygon: Polygon, polygon_list: List[Polygon] ):
		self.polygon = polygon
		self.polygon_list = polygon_list

	def visit_vertex( self, vertex: Vertex ) -> bool:
		# i = self.polygon.vertices.index( vertex )
		# v2 = self.polygon.vertices[(i + 1) % len( self.polygon.vertices )]
		# observer = VertexObserver( vertex, v2, relation = VerticalEdgeVertexRelation() )
		# vertex.move_observers.append( observer )
		# v2.move_observers.append( observer )
		# return

		if len( self.polygon.vertices ) == 3:
			return False
		self.polygon.vertices.remove( vertex )

		del_edges = [e for e in self.polygon.edges if e.v1 == vertex or e.v2 == vertex]
		v1 = __opposite_vertex__( del_edges[0], vertex )
		v2 = __opposite_vertex__( del_edges[1], vertex )

		del_index = self.polygon.edges.index( del_edges[0] )
		for edge in del_edges:
			self.polygon.edges.remove( edge )

		self.polygon.edges.insert( del_index, Edge( v1, v2 ) )
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
