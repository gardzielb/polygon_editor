from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from src.edge_constraints import EdgeConstraint
from src.geo_utils import line_length
from src.geometry_drawer import GeometryDrawer
from src.geometry_object import GeometryObject
from src.geometry_visitor import GeometryObjectVisitor


class Vertex( GeometryObject ):
	RADIUS = 2
	HIGHLIGHT_PEN = QColor( 0, 200, 0 )

	def __init__( self, point: QPoint ):
		super().__init__()
		self.point = point
		self.relations: List[VertexRelation] = []

	def draw( self, drawer: GeometryDrawer ):
		radius = self.RADIUS
		prev_pen = drawer.pen()
		if self.highlight:
			drawer.set_pen( self.HIGHLIGHT_PEN )
			radius += 1
		drawer.draw_point( self.point, radius )
		drawer.set_pen( prev_pen )

	def move( self, dest_x: int, dest_y: int ):
		self.move_carelessly( dest_x, dest_y )
		for relation in self.relations:
			relation.correct( sender = self )

	def is_hit( self, hit: QPoint ) -> bool:
		if abs( self.point.x() - hit.x() ) > self.RADIUS:
			return False
		return abs( self.point.y() - hit.y() ) <= self.RADIUS

	def accept_visitor( self, visitor: GeometryObjectVisitor ) -> bool:
		return visitor.visit_vertex( vertex = self )

	def can_move(
			self, dest_x, dest_y, initiator: Optional[Vertex] = None, sender: Optional[VertexRelation] = None
	) -> bool:
		if not initiator:
			initiator = self
		for relation in self.relations:
			if relation == sender:
				continue
			if not relation.can_allow_move( sender = self, dest_x = dest_x, dest_y = dest_y, initiator = initiator ):
				return False
		return True

	def move_carelessly( self, dest_x: int, dest_y: int ):
		self.point.setX( dest_x )
		self.point.setY( dest_y )

	def x( self ) -> int:
		return self.point.x()

	def y( self ) -> int:
		return self.point.y()

	def setX( self, x: int ):
		self.point.setX( x )

	def setY( self, y: int ):
		return self.point.setY( y )


class VertexRelation( ABC ):

	def __init__( self, constraint: EdgeConstraint ):
		self.constraint = constraint

	@abstractmethod
	def can_allow_move( self, sender: Vertex, dest_x: int, dest_y: int, initiator: Vertex ) -> bool:
		return False

	@abstractmethod
	def correct( self, sender: Vertex ):
		pass


def find_the_other( sender: Vertex, v1: Vertex, v2: Vertex ) -> Vertex:
	if v1 == sender:
		return v2
	return v1


class VerticalEdgeVertexRelation( VertexRelation ):

	def __init__( self, v1: Vertex, v2: Vertex ):
		super().__init__( EdgeConstraint.VERTICAL )
		self.v1 = v1
		self.v2 = v2

	def can_allow_move( self, sender: Vertex, dest_x: int, dest_y: int, initiator: Vertex ) -> bool:
		receiver = find_the_other( sender, self.v1, self.v2 )
		if receiver.x() == dest_x:
			return True
		if receiver == initiator:
			return False
		return receiver.can_move( dest_x, receiver.y(), initiator, sender = self )

	def correct( self, sender: Vertex ):
		receiver = find_the_other( sender, self.v1, self.v2 )
		if receiver.x() != sender.x():
			receiver.move( sender.x(), receiver.y() )


class HorizontalEdgeVertexRelation( VertexRelation ):

	def __init__( self, v1: Vertex, v2: Vertex ):
		super().__init__( EdgeConstraint.HORIZONTAL )
		self.v1 = v1
		self.v2 = v2

	def can_allow_move( self, sender: Vertex, dest_x: int, dest_y: int, initiator: Vertex ) -> bool:
		receiver = find_the_other( sender, self.v1, self.v2 )
		if receiver.y() == dest_y:
			return True
		if receiver == initiator:
			return False
		return receiver.can_move( receiver.x(), dest_y, initiator, sender = self )

	def correct( self, sender: Vertex ):
		receiver = find_the_other( sender, self.v1, self.v2 )
		if receiver.y() != sender.y():
			receiver.move( receiver.x(), sender.y() )


class FixedEdgeLengthVertexRelation( VertexRelation ):

	def __init__( self, v1: Vertex, v2: Vertex, length: int ):
		super().__init__( EdgeConstraint.FIXED_LENGTH )
		self.v1 = v1
		self.v2 = v2
		self.length = length
		self.dest_x: Optional[int] = None
		self.dest_y: Optional[int] = None

	def can_allow_move( self, sender: Vertex, dest_x: int, dest_y: int, initiator: Vertex ) -> bool:
		receiver = find_the_other( sender, self.v1, self.v2 )
		if abs( line_length( receiver.point, QPoint( dest_x, dest_y ) ) - self.length ) <= Vertex.RADIUS:
			return True
		if receiver == initiator:
			return False
		return self.__try_on_circle__(
			vertex = receiver, neighbor_x = dest_x, neighbor_y = dest_y, initiator = initiator
		)

	def correct( self, sender: Vertex ):
		receiver = find_the_other( sender, self.v1, self.v2 )
		if abs( line_length( sender.point, receiver.point ) - self.length ) <= Vertex.RADIUS:
			return
		if self.dest_x or self.__try_on_circle__( receiver, sender.x(), sender.y(), sender ):
			receiver.move( self.dest_x, self.dest_y )
		self.dest_x, self.dest_y = None, None

	def __try_on_circle__( self, vertex: Vertex, neighbor_x: int, neighbor_y: int, initiator: Vertex ) -> bool:
		delta_e = 3
		delta_se = 5 - 2 * self.length
		d = 1 - self.length
		x = 0
		y = self.length

		points: List[QPoint] = []
		point = self.__closest_on_circle__( vertex, x, y, neighbor_x, neighbor_y, initiator )
		if point:
			points.append( point )

		while y > x:
			if d < 0:
				d += delta_e
				delta_e += 2
				delta_se += 2
			else:
				d += delta_se
				delta_e += 2
				delta_se += 4
				y -= 1
			x += 1
			point = self.__closest_on_circle__( vertex, x, y, neighbor_x, neighbor_y, initiator )
			if point:
				points.append( point )

		if points:
			points.sort( key = lambda pt: line_length( pt, vertex.point ) )
			self.dest_x, self.dest_y = points[0].x(), points[0].y()
			return True
		return False

	def __closest_on_circle__(
			self, vertex: Vertex, x: int, y: int, offset_x: int, offset_y: int, initiator: Vertex
	) -> Optional[QPoint]:
		points = [
			QPoint( x + offset_x, y + offset_y ), QPoint( y + offset_x, x + offset_y ),
			QPoint( y + offset_x, -x + offset_y ), QPoint( x + offset_x, -y + offset_y ),
			QPoint( -x + offset_x, -y + offset_y ), QPoint( -y + offset_x, -x + offset_y ),
			QPoint( -y + offset_x, x + offset_y ), QPoint( -x + offset_x, y + offset_y )
		]

		points.sort( key = lambda pt: line_length( pt, vertex.point ) )
		for point in points:
			if vertex.can_move( point.x(), point.y(), initiator, sender = self ):
				return point
		return None
