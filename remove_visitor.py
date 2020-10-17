from PyQt5.QtCore import QPoint

from geometry_visitor import GeometryObjectVisitor
from polygon import Polygon
from polygon_objects import Vertex, Edge


def __opposite_point__( edge: Edge, vertex: Vertex ) -> QPoint:
	if edge.p1 == vertex.point:
		return edge.p2
	else:
		return edge.p1


class RemoveGeometryObjectVisitor( GeometryObjectVisitor ):

	def __init__( self, polygon: Polygon ):
		self.polygon = polygon

	def visit_vertex( self, vertex: Vertex ) -> bool:
		if len( self.polygon.vertices ) == 3:
			return False
		self.polygon.vertices.remove( vertex )

		del_edges = [e for e in self.polygon.edges if e.p1 == vertex.point or e.p2 == vertex.point]
		p1 = __opposite_point__( del_edges[0], vertex )
		p2 = __opposite_point__( del_edges[1], vertex )

		for edge in del_edges:
			self.polygon.edges.remove( edge )

		self.polygon.edges.append( Edge( p1, p2 ) )
		return True

	def visit_edge( self, edge: Edge ) -> bool:
		self.polygon.edges.remove( edge )

		del_vertices = [v.point for v in self.polygon.vertices if v.point == edge.p1 or v.point == edge.p2]
		self.polygon.vertices.remove( del_vertices[0] )
		self.polygon.vertices.remove( del_vertices[1] )

		new_x = (edge.p1.x() + edge.p2.x()) / 2
		new_y = (edge.p1.y() + edge.p2.y()) / 2
		new_point = QPoint( new_x, new_y )

		self.polygon.vertices.append( Vertex( new_point ) )
		self.polygon.edges.append( Edge( edge.p1, new_point ) )
		self.polygon.edges.append( Edge( edge.p2, new_point ) )

		return True

	def visit_polygon( self, polygon: Polygon ) -> bool:
		pass
