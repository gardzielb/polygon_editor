from typing import List

from PyQt5.QtCore import QPoint

from constants import POINT_RADIUS
from polygon import Polygon


class PolygonBuilder:

	def __init__( self ):
		self.points: List[QPoint] = []
		self.is_finished = False

	def add_point( self, point: QPoint ):
		if self.is_finished:
			return
		self.points.append( point )
		self.is_finished = self.are_ends_met()
		if not self.is_finished:
			self.points.append( point )

	def build_polygon( self ) -> Polygon:
		self.is_finished = False
		polygon = Polygon( points = self.points[0:(len( self.points ) - 2)] )
		self.points.clear()
		return polygon

	def move_last_point( self, point: QPoint ):
		if self.points and not self.is_finished:
			self.points[len( self.points ) - 1] = point

	def current_size( self ):
		return len( self.points )

	def are_ends_met( self ) -> bool:
		v_count = len( self.points )
		if v_count <= 1:
			return False
		if abs( self.points[0].x() - self.points[v_count - 1].x() ) > POINT_RADIUS:
			return False
		return abs( self.points[0].y() - self.points[v_count - 1].y() ) <= POINT_RADIUS
