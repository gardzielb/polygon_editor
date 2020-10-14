from PyQt5.QtGui import QPaintEvent, QColor, QMouseEvent
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
		self.polygons = []
		self.setMouseTracking( True )
		self.is_drawing = False

	def mouseReleaseEvent( self, event: QMouseEvent ) -> None:
		self.add_polygon(
			Polygon( [
				QPoint( event.x(), event.y() - 20 ), QPoint( event.x() + 17, event.y() + 10 ),
				QPoint( event.x() - 17, event.y() + 10 )
			] )
		)
		self.repaint()

	# def mouseMoveEvent( self, event: QMouseEvent ) -> None:
	# 	for polygon in self.polygons:
	# 		polygon.find_edge( event.pos() )

	def paintEvent( self, event: QPaintEvent ):
		self.painter.begin( self )
		self.painter.setPen( QColor( 0, 0, 255 ) )
		for polygon in self.polygons:
			self.__draw_polygon__( polygon )
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
