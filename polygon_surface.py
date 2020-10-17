from typing import Dict, List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPaintEvent, QColor, QMouseEvent, QPainterPath, QBrush
from PyQt5.QtWidgets import QWidget

from geometry_drawer import GeometryDrawer
from geometric_object import GeometricObject
from line_drawers import *
from polygon import Polygon, Vertex
from polygon_builder import PolygonBuilder


class PolygonSurface( QWidget ):

	def __init__( self, *args ):
		super().__init__( *args )
		self.drawer = GeometryDrawer()

		self.polygons: List[Polygon] = []
		self.polygon_builder = PolygonBuilder()
		self.active_object: Union[GeometricObject, None] = None
		self.is_object_grabbed = False

		self.setMouseTracking( True )

	def mousePressEvent( self, event: QMouseEvent ) -> None:
		if event.button() != Qt.LeftButton:
			return
		if self.active_object:
			self.active_object.start_moving( event.pos() )
			self.is_object_grabbed = True

	def mouseReleaseEvent( self, event: QMouseEvent ) -> None:
		if event.button() == Qt.LeftButton:
			if self.is_object_grabbed:
				self.active_object.end_moving()
				self.active_object.highlight = False
				self.active_object = None
				self.is_object_grabbed = False
			else:
				self.polygon_builder.add_point( event.pos() )
				if self.polygon_builder.is_finished:
					self.polygons.append( self.polygon_builder.build_polygon() )
		else:
			self.polygon_builder.reset()

		self.repaint()

	def mouseMoveEvent( self, event: QMouseEvent ) -> None:
		if not self.polygon_builder.is_finished:
			self.polygon_builder.move_last_point( event.pos() )
		elif self.is_object_grabbed:
			self.active_object.move( dest_point = event.pos() )
		else:
			self.active_object = None
			for polygon in self.polygons:
				vertex = polygon.search_for_vertex( event.pos() )
				if vertex:
					self.active_object = vertex
					self.active_object.highlight = True
					# print( self.active_object.highlight )
					break
		self.repaint()

	def paintEvent( self, event: QPaintEvent ):
		self.drawer.begin( self )
		for polygon in self.polygons:
			polygon.draw( self.drawer )
		self.__draw_unfinished_polygon__()
		self.drawer.end()

	def __draw_unfinished_polygon__( self ):
		for i in range( self.polygon_builder.current_size() - 1 ):
			self.polygon_builder.vertices[i].draw( self.drawer )
			self.drawer.draw_line( self.polygon_builder.vertices[i].point, self.polygon_builder.vertices[i + 1].point )
