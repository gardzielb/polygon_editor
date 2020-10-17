from typing import List, Union

from PyQt5.QtCore import QPoint

from geometry_drawer import GeometryDrawer
from polygon import Polygon, Vertex


class PolygonBuilder:

	def __init__( self ):
		self.vertices: List[Vertex] = []
		self.is_finished = False
		self.floating_vertex: Union[Vertex, None] = None

	def add_point( self, point: QPoint ):
		if self.is_finished and self.vertices:
			return
		if not self.vertices and not self.floating_vertex:
			self.is_finished = False

		if self.floating_vertex:
			new_vertex = self.floating_vertex
		else:
			new_vertex = Vertex( point )
		self.vertices.append( new_vertex )
		self.is_finished = self.__are_ends_met__()
		if not self.is_finished:
			self.floating_vertex = Vertex( QPoint( point.x(), point.y() ) )

	def build_polygon( self ) -> Polygon:
		polygon = Polygon( vertices = self.vertices[0: len( self.vertices ) - 1] )
		self.reset()
		return polygon

	def reset( self ):
		self.vertices.clear()
		self.floating_vertex = None
		self.is_finished = True

	def move_floating_vertex( self, point: QPoint ):
		if self.floating_vertex and not self.is_finished:
			self.floating_vertex.move( dest_point = point )

	def draw( self, drawer: GeometryDrawer ):
		if not self.vertices:
			return
		self.vertices[0].draw( drawer )
		for i in range( 1, len( self.vertices ) ):
			drawer.draw_line( self.vertices[i - 1].point, self.vertices[i].point )
			self.vertices[i].draw( drawer )
		if self.floating_vertex:
			drawer.draw_line( self.vertices[len( self.vertices ) - 1].point, self.floating_vertex.point )
			self.floating_vertex.draw( drawer )

	def __are_ends_met__( self ) -> bool:
		if not self.floating_vertex or len( self.vertices ) <= 1:
			return False
		return self.vertices[0].is_hit( hit = self.floating_vertex.point )
