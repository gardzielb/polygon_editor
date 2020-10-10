from PyQt5.QtCore import QPoint, QLine
from typing import List


class Polygon:
	def __init__( self, points: List[QPoint] ):
		self.points = points

	def vertices( self ) -> int:
		return len( self.points )

	def find_edge( self, point: QPoint ):
		for i in range( len( self.points ) ):
			p1 = self.points[i]
			p2 = self.points[(i + 1) % len( self.points )]
			a = (p1.y() - p2.y()) / (p1.x() - p2.x())
			b = p1.y() - a * p1.x()
			if point.y() == a * point.x() + b:
				print( "hover on edge detected" )
