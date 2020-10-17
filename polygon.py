from typing import List, Union

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainterPath, QBrush

from geometric_object import GeometricObject
from geometry_drawer import GeometryDrawer


class Vertex( GeometricObject ):
	RADIUS = 2

	def __init__( self, point: QPoint ):
		super().__init__()
		self.point = point

	def draw_stroke( self, drawer: GeometryDrawer ):
		drawer.draw_point( self.point, self.RADIUS )

	def move( self, dest_point: QPoint ):
		self.point.setX( dest_point.x() )
		self.point.setY( dest_point.y() )

	def fill( self, drawer: GeometryDrawer ):
		pass

	def is_hit( self, hit: QPoint ) -> bool:
		if abs( self.point.x() - hit.x() ) > self.RADIUS:
			return False
		return abs( self.point.y() - hit.y() ) <= self.RADIUS


class Edge( GeometricObject ):

	def __init__( self, p1: QPoint, p2: QPoint ):
		super().__init__()
		self.p1 = p1
		self.p2 = p2

	def draw_stroke( self, drawer: GeometryDrawer ):
		drawer.draw_line( self.p1, self.p2 )

	def fill( self, drawer: GeometryDrawer ):
		pass

	def move( self, dest_point: QPoint ):
		if not self.move_origin:
			return
		move_x = dest_point.x() - self.move_origin.x()
		move_y = dest_point.y() - self.move_origin.y()
		self.p1.setX( self.p1.x() + move_x )
		self.p1.setY( self.p1.y() + move_y )
		self.p2.setX( self.p1.x() + move_x )
		self.p2.setY( self.p1.y() + move_y )


class Polygon( GeometricObject ):

	def __init__( self, vertices: List[Vertex] ):
		super().__init__()

		self.vertices: List[Vertex] = vertices
		self.edges: List[Edge] = []
		self.painter_path = QPainterPath( vertices[0].point )
		self.fill_brush = QBrush()

		for i in range( len( vertices ) ):
			i2 = (i + 1) % len( vertices )
			self.edges.append( Edge( vertices[i].point, vertices[i2].point ) )
			self.painter_path.lineTo( vertices[i].point )

	def draw_stroke( self, drawer: GeometryDrawer ):
		for edge in self.edges:
			edge.draw_stroke( drawer )
		for vertex in self.vertices:
			vertex.draw_stroke( drawer )

	def fill( self, drawer: GeometryDrawer ):
		drawer.fill_polygon( self.painter_path )

	def move( self, dest_point: QPoint ):
		if not self.move_origin:
			return
		move_x = dest_point.x() - self.move_origin.x()
		move_y = dest_point.y() - self.move_origin.y()
		for vertex in self.vertices:
			vertex.point.setX( vertex.point.x() + move_x )
			vertex.point.setY( vertex.point.y() + move_y )

	def vertices_count( self ) -> int:
		return len( self.vertices )

	def search_for_vertex( self, vertex: QPoint ) -> Union[Vertex, None]:
		for v in self.vertices:
			if v.is_hit( hit = vertex ):
				return v
		return None

# def find_edge( self, point: QPoint ):
# 	for i in range( len( self.points ) ):
# 		p1 = self.points[i]
# 		p2 = self.points[(i + 1) % len( self.points )]
# 		a = (p1.y() - p2.y()) / (p1.x() - p2.x())
# 		b = p1.y() - a * p1.x()
# 		if point.y() == a * point.x() + b:
# 			print( "hover on edge detected" )
#
# def is_point_inside( self, point: QPoint ) -> bool:
# 	return False  # TODO
