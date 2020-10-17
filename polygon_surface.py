from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPaintEvent, QMouseEvent
from PyQt5.QtWidgets import QWidget

from geometry_drawer import GeometryDrawer
from line_drawers import *
from polygon import Polygon
from polygon_action_manager import PolygonActionManager
from polygon_builder import PolygonBuilder


class PolygonSurface( QWidget ):

	def __init__( self, *args ):
		super().__init__( *args )
		self.drawer = GeometryDrawer()

		self.polygons: List[Polygon] = []
		self.polygon_builder = PolygonBuilder()
		self.polygon_action_manager = PolygonActionManager()

		self.setMouseTracking( True )

	def mousePressEvent( self, event: QMouseEvent ) -> None:
		if event.button() != Qt.LeftButton:
			return
		if self.polygon_action_manager.is_active:
			self.polygon_action_manager.is_moving = True

	def mouseReleaseEvent( self, event: QMouseEvent ) -> None:
		if event.button() == Qt.LeftButton:
			if self.polygon_action_manager.is_moving:
				self.polygon_action_manager.release_object()
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
		elif self.polygon_action_manager.is_moving:
			self.polygon_action_manager.move_object( dest_point = event.pos() )
		else:
			self.polygon_action_manager.release_object()
			for polygon in self.polygons:
				hit_object = polygon.search_for_hit( event.pos() )
				if hit_object:
					self.polygon_action_manager.set_polygon( polygon, active_object = hit_object )
					break
		self.repaint()

	def paintEvent( self, event: QPaintEvent ):
		self.drawer.begin( self )
		for polygon in self.polygons:
			polygon.draw( self.drawer )
		self.polygon_builder.draw( self.drawer )
		self.drawer.end()
