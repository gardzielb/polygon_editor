from typing import Dict

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPaintEvent, QColor, QMouseEvent, QPainterPath, QBrush
from PyQt5.QtWidgets import QWidget

from constants import POINT_RADIUS
from line_drawers import *
from polygon import Polygon
from polygon_builder import PolygonBuilder


def build_polygon_path( polygon: Polygon ) -> QPainterPath:
	path = QPainterPath( polygon.points[0] )
	for i in range( 1, len( polygon.points ) - 1 ):
		path.lineTo( polygon.points[i] )
	return path


class PolygonSurface( QWidget ):
	STROKE_COLOR = QColor( 0, 0, 255 )
	FILL_BRUSH = QBrush( QColor( 200, 200, 200 ), Qt.SolidPattern )

	def __init__( self, *args ):
		super().__init__( *args )
		self.painter = QPainter()
		self.draw_line_chain = GentleIncreaseLineDrawer()
		self.draw_line_chain.set_next( SteepIncreaseLineDrawer() ).set_next( GentleDecreaseLineDrawer() ) \
			.set_next( SteepDecreaseLineDrawer() )

		self.polygon_map: Dict[Polygon, QPainterPath] = { }
		self.polygon_builder = PolygonBuilder()

		self.setMouseTracking( True )
		self.is_drawing = False

	def mouseReleaseEvent( self, event: QMouseEvent ) -> None:
		self.polygon_builder.add_point( event.pos() )
		if self.polygon_builder.is_finished:
			polygon = self.polygon_builder.build_polygon()
			self.polygon_map[polygon] = build_polygon_path( polygon )
		self.repaint()

	def mouseMoveEvent( self, event: QMouseEvent ) -> None:
		if not self.polygon_builder.is_finished:
			self.polygon_builder.move_last_point( event.pos() )
		self.repaint()

	def paintEvent( self, event: QPaintEvent ):
		self.painter.begin( self )
		self.painter.setPen( QColor( 0, 0, 255 ) )
		for polygon in self.polygon_map.keys():
			self.__draw_polygon__( polygon )
		self.__draw_unfinished_polygon__()
		self.painter.end()

	def __draw_unfinished_polygon__( self ):
		for i in range( self.polygon_builder.current_size() - 1 ):
			self.__draw_point__( self.polygon_builder.points[i] )
			self.__draw_line__( self.polygon_builder.points[i], self.polygon_builder.points[i + 1] )

	def __draw_polygon__( self, polygon: Polygon ):
		self.painter.fillPath( self.polygon_map[polygon], self.FILL_BRUSH )
		v_count = polygon.vertices()
		for i in range( v_count ):
			i2 = (i + 1) % v_count
			self.__draw_point__( polygon.points[i] )
			self.__draw_line__( polygon.points[i], polygon.points[i2] )

	def __draw_line__( self, p1: QPoint, p2: QPoint ):
		if p1.x() < p2.x():
			self.draw_line_chain.draw_line( p1, p2, self.painter )
		elif p1.x() == p2.x():
			pass  # TODO
		else:
			self.draw_line_chain.draw_line( p2, p1, self.painter )

	def __draw_point__( self, point: QPoint ):
		for i in range( -POINT_RADIUS, POINT_RADIUS ):
			for j in range( -POINT_RADIUS, POINT_RADIUS ):
				self.painter.drawPoint( point.x() + i, point.y() + j )
