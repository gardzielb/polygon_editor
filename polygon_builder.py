from typing import List

from PyQt5.QtCore import QPoint

from polygon import Polygon, Vertex


class PolygonBuilder:

	def __init__( self ):
		self.vertices: List[Vertex] = []
		self.is_finished = False

	def add_point( self, point: QPoint ):
		if self.is_finished and self.vertices:
			return
		if not self.vertices:
			self.is_finished = False
		self.vertices.append( Vertex( point ) )
		self.is_finished = self.__are_ends_met__()
		if not self.is_finished:
			self.vertices.append( Vertex( QPoint( point.x(), point.y() ) ) )

	def build_polygon( self ) -> Polygon:
		polygon = Polygon( vertices = self.vertices[0:(len( self.vertices ) - 2)] )
		self.reset()
		return polygon

	def reset( self ):
		self.vertices.clear()
		self.is_finished = True

	def move_last_point( self, point: QPoint ):
		if self.vertices and not self.is_finished:
			self.vertices[len( self.vertices ) - 1].move( dest_point = point )

	def current_size( self ):
		return len( self.vertices )

	def __are_ends_met__( self ) -> bool:
		v_count = len( self.vertices )
		return v_count > 1 and self.vertices[0].is_hit( hit = self.vertices[v_count - 1].point )
