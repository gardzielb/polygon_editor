from abc import ABC, abstractmethod
from typing import List

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from geo_utils import line_length
from geometry_drawer import GeometryDrawer
from geometry_object import GeometryObject
from geometry_visitor import GeometryObjectVisitor


class Vertex( GeometryObject ):
	RADIUS = 2
	HIGHLIGHT_PEN = QColor( 0, 200, 0 )

	def __init__( self, point: QPoint ):
		super().__init__()
		self.point = point
		self.last_move_vector = QPoint()
		self.move_observers: List[VertexObserver] = []

	def draw( self, drawer: GeometryDrawer ):
		radius = self.RADIUS
		prev_pen = drawer.pen()
		if self.highlight:
			drawer.set_pen( self.HIGHLIGHT_PEN )
			radius += 1
		drawer.draw_point( self.point, radius )
		drawer.set_pen( prev_pen )

	def move( self, dest_x: int, dest_y: int ):
		self.last_move_vector.setX( dest_x - self.point.x() )
		self.last_move_vector.setY( dest_y - self.point.y() )
		self.point.setX( dest_x )
		self.point.setY( dest_y )
		self.__notify_observers__()

	def is_hit( self, hit: QPoint ) -> bool:
		if abs( self.point.x() - hit.x() ) > self.RADIUS:
			return False
		return abs( self.point.y() - hit.y() ) <= self.RADIUS

	def accept_visitor( self, visitor: GeometryObjectVisitor ) -> bool:
		return visitor.visit_vertex( vertex = self )

	def __notify_observers__( self ):
		for observer in self.move_observers:
			observer.update( v_moved = self )

	def x( self ) -> int:
		return self.point.x()

	def y( self ) -> int:
		return self.point.y()

	def setX( self, x: int ):
		self.point.setX( x )

	def setY( self, y: int ):
		return self.point.setY( y )


class VertexRelation( ABC ):

	@abstractmethod
	def correct_on_move( self, v_moved: Vertex, v_to_move: Vertex ):
		pass

	@abstractmethod
	def is_satisfied( self, v1: Vertex, v2: Vertex ) -> bool:
		return True


class VerticalEdgeVertexRelation( VertexRelation ):
	def is_satisfied( self, v1: Vertex, v2: Vertex ) -> bool:
		return v1.x() == v2.x()

	def correct_on_move( self, v_moved: Vertex, v_to_move: Vertex ):
		v_to_move.move( v_moved.point.x(), v_to_move.point.y() )


class HorizontalEdgeVertexRelation( VertexRelation ):
	def is_satisfied( self, v1: Vertex, v2: Vertex ) -> bool:
		return v1.y() == v2.y()

	def correct_on_move( self, v_moved: Vertex, v_to_move: Vertex ):
		v_to_move.move( v_to_move.point.x(), v_moved.point.y() )


class FixedEdgeLengthVertexRelation( VertexRelation ):

	def __init__( self, length: int ):
		self.length = length

	def is_satisfied( self, v1: Vertex, v2: Vertex ) -> bool:
		return line_length( v1.point, v2.point ) == self.length

	def correct_on_move( self, v_moved: Vertex, v_to_move: Vertex ):
		dest_x = v_to_move.point.x() + v_moved.last_move_vector.x()
		dest_y = v_to_move.point.y() + v_moved.last_move_vector.y()
		v_to_move.move( dest_x, dest_y )


class VertexObserver:

	def __init__( self, v1, v2, relation: VertexRelation ):
		self.v1 = v1
		self.v2 = v2
		self.relation = relation

	def update( self, v_moved: Vertex ):
		if self.relation.is_satisfied( self.v1, self.v2 ):
			return

		if v_moved == self.v1:
			v_to_move = self.v2
		else:
			v_to_move = self.v1
		self.relation.correct_on_move( v_moved, v_to_move )
