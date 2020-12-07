from __future__ import annotations

from abc import ABC, abstractmethod
from math import sqrt
from typing import List, Optional, Any

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from src.edge_constraints import EdgeConstraint
from src.geo_utils import line_length, get_line_equation, circle_intersections
from src.geometry_drawer import GeometryDrawer
from src.geometry_object import GeometryObject
from src.geometry_visitor import GeometryObjectVisitor


class Vertex( GeometryObject ):
	RADIUS = 2
	FOCUS_RADIUS = 6
	HIGHLIGHT_PEN = QColor( 0, 200, 0 )

	def __init__( self, point: QPoint ):
		super().__init__()
		self.point = point
		self.relations: List[VertexRelation] = []
		self.last_move_vector = QPoint( 0, 0 )

	def draw( self, drawer: GeometryDrawer ):
		radius = self.RADIUS
		prev_pen = drawer.pen()
		if self.highlight:
			drawer.set_pen( self.HIGHLIGHT_PEN )
			radius += 1
		drawer.draw_point( self.point, radius )
		drawer.set_pen( prev_pen )

	def move( self, dest_x: int, dest_y: int ):
		self.move_by_relation( dest_x, dest_y, sender = None )

	def is_hit( self, hit: QPoint ) -> bool:
		if abs( self.point.x() - hit.x() ) > self.FOCUS_RADIUS:
			return False
		return abs( self.point.y() - hit.y() ) <= self.FOCUS_RADIUS

	def accept_visitor( self, visitor: GeometryObjectVisitor ) -> bool:
		return visitor.visit_vertex( vertex = self )

	def can_move(
			self, dest_x: int, dest_y: int, initiator: Optional[Vertex] = None, sender: Optional[VertexRelation] = None
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
		self.last_move_vector.setX( dest_x - self.x() )
		self.last_move_vector.setY( dest_y - self.y() )
		self.point.setX( dest_x )
		self.point.setY( dest_y )

	def move_by_relation( self, dest_x: int, dest_y: int, sender: Optional[VertexRelation] ):
		self.move_carelessly( dest_x, dest_y )
		for relation in self.relations:
			if relation is not sender:
				relation.correct( sender = self )

	def x( self ) -> int:
		return self.point.x()

	def y( self ) -> int:
		return self.point.y()

	def setX( self, x: int ):
		self.point.setX( x )

	def setY( self, y: int ):
		return self.point.setY( y )


class VertexRelation( ABC ):

	def __init__( self, v1: Vertex, v2: Vertex, constraint: EdgeConstraint ):
		self.v1 = v1
		self.v2 = v2
		self.constraint = constraint

	@abstractmethod
	def can_allow_move( self, sender: Vertex, dest_x: int, dest_y: int, initiator: Vertex ) -> bool:
		return False

	@abstractmethod
	def correct( self, sender: Vertex ):
		pass


def find_the_other( sender: Vertex, o1, o2 ) -> Any:
	if o1 == sender:
		return o2
	return o1


class VerticalEdgeVertexRelation( VertexRelation ):

	def __init__( self, v1: Vertex, v2: Vertex ):
		super().__init__( v1, v2, EdgeConstraint.VERTICAL )

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
			receiver.move_by_relation( sender.x(), receiver.y(), sender = self )


class HorizontalEdgeVertexRelation( VertexRelation ):

	def __init__( self, v1: Vertex, v2: Vertex ):
		super().__init__( v1, v2, EdgeConstraint.HORIZONTAL )

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
			receiver.move_by_relation( receiver.x(), sender.y(), sender = self )


def resolve_length_length( p1: QPoint, p2: QPoint, p_moved: QPoint, l1: int, l2: int ) -> Optional[QPoint]:
	solution = circle_intersections( mid1 = p1, r1 = l1, mid2 = p2, r2 = l2 )
	if not solution:
		return None

	dist1 = line_length( p_moved, solution[0] )
	dist2 = line_length( p_moved, solution[1] )
	if dist1 <= dist2:
		return solution[0]
	return solution[1]


class FixedEdgeLengthVertexRelation( VertexRelation ):

	def __init__( self, v1: Vertex, v2: Vertex, length: int ):
		super().__init__( v1, v2, EdgeConstraint.FIXED_LENGTH )
		self.length = length
		self.dest: Optional[QPoint] = None

	def can_allow_move( self, sender: Vertex, dest_x: int, dest_y: int, initiator: Vertex ) -> bool:
		receiver = find_the_other( sender, self.v1, self.v2 )
		if abs( line_length( receiver.point, QPoint( dest_x, dest_y ) ) - self.length ) <= Vertex.RADIUS:
			return True
		if receiver == initiator:
			return False

		self.dest = self.__solve_conflict__( benchmark = QPoint( dest_x, dest_y ), p_moved = receiver )
		return bool( self.dest )

	def correct( self, sender: Vertex ):
		receiver = find_the_other( sender, self.v1, self.v2 )
		if abs( line_length( sender.point, receiver.point ) - self.length ) <= Vertex.RADIUS:
			return

		if self.dest:
			receiver.move( self.dest.x(), self.dest.y() )
			self.dest = None

		move_vector = sender.last_move_vector
		move_x = receiver.x() + move_vector.x()
		move_y = receiver.y() + move_vector.y()
		receiver.move_by_relation( move_x, move_y, sender = self )

	def __solve_conflict__( self, benchmark: QPoint, p_moved: Vertex ) -> Optional[QPoint]:
		if p_moved.relations:
			relation = p_moved.relations[0]
			other_benchmark = find_the_other( p_moved, relation.v1, relation.v2 )

			if relation.constraint == EdgeConstraint.FIXED_LENGTH:
				return resolve_length_length(
					p1 = benchmark, p2 = other_benchmark.point, p_moved = p_moved.point, l1 = self.length,
					l2 = int( line_length( other_benchmark.point, p_moved.point ) )
				)

		a, b = get_line_equation( benchmark, p_moved.point )
		if p_moved.x() >= benchmark.x():
			x = self.length / sqrt( 1 + a ** 2 ) + benchmark.x()
		else:
			x = benchmark.x() - self.length / sqrt( 1 + a ** 2 )
		return QPoint( x, a * x + b )
