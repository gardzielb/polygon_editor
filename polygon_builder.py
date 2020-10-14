from typing import List

from PyQt5.QtCore import QPoint

from polygon import Polygon


class PolygonBuilder:

	def __init__( self ):
		self.points: List[QPoint] = []
		self.is_finished = False

	def add_point( self, point: QPoint ):
		self.is_finished = self.points[0] == self.points[len( self.points ) - 1]
		if self.is_finished:
			self.points.append( point )

	def build_polygon( self ) -> Polygon:
		self.is_finished = False
		return Polygon( points = self.points )
