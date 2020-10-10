from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPaintEvent, QPainter, QColor
from PyQt5.QtWidgets import QWidget

from polygon import Polygon
from line_drawers import *


class PolygonSurface( QWidget ):
	def __init__( self, *args ):
		super().__init__( *args )
		self.painter = QPainter()
		self.draw_line_chain = GentleIncreaseLineDrawer()
		self.draw_line_chain.set_next( SteepIncreaseLineDrawer() ).set_next( GentleDecreaseLineDrawer() ) \
			.set_next( SteepDecreaseLineDrawer() )
		self.polygons = [Polygon( [QPoint( 100, 100 ), QPoint( 50, 150 ), QPoint( 150, 150 )] )]

	def paintEvent( self, event: QPaintEvent ):
		self.painter.begin( self )
		self.painter.setPen( QColor( 0, 0, 255 ) )
		for polygon in self.polygons:
			self.__draw_polygon__( polygon )

		# self.__draw_line_bresenham__( QPoint( 0, 0 ), QPoint( 100, 100 ) )
		# self.__draw_line_bresenham__( QPoint( 100, 100 ), QPoint( 0, 0 ) )

		self.painter.end()

	def add_polygon( self, polygon: Polygon ):
		self.polygons.append( polygon )

	def __draw_polygon__( self, polygon: Polygon ):
		v_count = polygon.vertices()
		for i in range( v_count ):
			i2 = (i + 1) % v_count
			self.__draw_line__( polygon.points[i], polygon.points[i2] )

	def __draw_line__( self, p1: QPoint, p2: QPoint ):
		if p1.x() < p2.x():
			self.draw_line_chain.draw_line( p1, p2, self.painter )
		elif p1.x() == p2.x():
			pass  # TODO
		else:
			self.draw_line_chain.draw_line( p2, p1, self.painter )
