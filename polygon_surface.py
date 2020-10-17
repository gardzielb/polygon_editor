from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPaintEvent, QMouseEvent
from PyQt5.QtWidgets import QWidget

from geometry_drawer import GeometryDrawer
from line_drawers import *
from polygon import Polygon
from polygon_builder import PolygonBuilder


class PolygonSurface( QWidget ):

	def __init__( self, *args ):
		super().__init__( *args )
		self.drawer = GeometryDrawer()

		self.polygons: List[Polygon] = []
		self.polygon_builder = PolygonBuilder()
		self.active_polygon: Union[Polygon, None] = None
		self.is_object_grabbed = False

		self.setMouseTracking( True )

	def mousePressEvent( self, event: QMouseEvent ) -> None:
		if event.button() != Qt.LeftButton:
			return
		if self.active_polygon:
			self.is_object_grabbed = True

	def mouseReleaseEvent( self, event: QMouseEvent ) -> None:
		if event.button() == Qt.LeftButton:
			if self.is_object_grabbed:
				self.active_polygon.release()
				self.active_polygon = None
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
			self.polygon_builder.move_floating_vertex( event.pos() )
		elif self.is_object_grabbed:
			self.active_polygon.move( dest_point = event.pos() )
		else:
			self.active_polygon = None
			for polygon in self.polygons:
				if polygon.try_hit( event.pos() ):
					self.active_polygon = polygon
					break
		self.repaint()

	def paintEvent( self, event: QPaintEvent ):
		self.drawer.begin( self )
		for polygon in self.polygons:
			polygon.draw( self.drawer )
		self.polygon_builder.draw( self.drawer )
		self.drawer.end()
