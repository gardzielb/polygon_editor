from typing import List

from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtGui import QPaintEvent, QMouseEvent
from PyQt5.QtWidgets import QWidget, QMessageBox

from src.geometry_drawer import GeometryDrawer
from src.polygon import Polygon
from src.polygon_action_manager import PolygonActionManager
from src.polygon_builder import PolygonBuilder
from src.vertex import Vertex


def show_message( icon: QMessageBox.Icon, title: str, text: str ):
	msg_box = QMessageBox()
	msg_box.setIcon( icon )
	msg_box.setWindowTitle( title )
	msg_box.setText( text )
	msg_box.setStandardButtons( QMessageBox.Ok )
	msg_box.exec_()


class PolygonSurface( QWidget ):

	def __init__( self, *args ):
		super().__init__( *args )
		self.setMinimumSize( QSize( 1200, 800 ) )

		self.drawer = GeometryDrawer()
		self.polygons: List[Polygon] = []
		self.polygon_builder = PolygonBuilder()
		self.polygon_action_manager = PolygonActionManager()

		self.setMouseTracking( True )

	def mousePressEvent( self, event: QMouseEvent ) -> None:
		if event.button() != Qt.LeftButton:
			return
		if self.polygon_action_manager.is_active:
			self.polygon_action_manager.set_moving( True )

	def mouseReleaseEvent( self, event: QMouseEvent ) -> None:
		if event.button() == Qt.LeftButton:
			if self.polygon_action_manager.is_moving:
				self.polygon_action_manager.release_object()
			else:
				self.polygon_builder.add_point( event.pos() )
				if self.polygon_builder.is_finished:
					self.polygons.append( self.polygon_builder.build_polygon() )
		else:
			if self.polygon_action_manager.is_active:
				if not self.polygon_action_manager.edit_remove_object():
					show_message(
						icon = QMessageBox.Critical, title = 'Action failed', text = 'Cannot perform required action.'
					)
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
					self.polygon_action_manager.set_polygon(
						polygon, active_object = hit_object, polygon_list = self.polygons
					)
					break
		self.repaint()

	def paintEvent( self, event: QPaintEvent ):
		self.drawer.begin( self )

		# delta_e = 3
		# delta_se = 5 - 2 * 200
		# d = 1 - 200
		# x = 0
		# y = 200
		#
		# self.drawer.painter.drawPoint( x + 500, y + 500 )
		# self.drawer.painter.drawPoint( y + 500, x + 500 )
		# self.drawer.painter.drawPoint( -y + 500, x + 500 )
		# self.drawer.painter.drawPoint( -x + 500, y + 500 )
		# self.drawer.painter.drawPoint( y + 500, -x + 500 )
		# self.drawer.painter.drawPoint( x + 500, -y + 500 )
		# self.drawer.painter.drawPoint( -x + 500, -y + 500 )
		# self.drawer.painter.drawPoint( -y + 500, -x + 500 )
		#
		# while y > x:
		# 	if d < 0:
		# 		d += delta_e
		# 		delta_e += 2
		# 		delta_se += 2
		# 	else:
		# 		d += delta_se
		# 		delta_e += 2
		# 		delta_se += 4
		# 		y -= 1
		# 	x += 1
		# 	self.drawer.painter.drawPoint( x + 500, y + 500 )
		# 	self.drawer.painter.drawPoint( y + 500, x + 500 )
		# 	self.drawer.painter.drawPoint( -y + 500, x + 500 )
		# 	self.drawer.painter.drawPoint( -x + 500, y + 500 )
		# 	self.drawer.painter.drawPoint( y + 500, -x + 500 )
		# 	self.drawer.painter.drawPoint( x + 500, -y + 500 )
		# 	self.drawer.painter.drawPoint( -x + 500, -y + 500 )
		# 	self.drawer.painter.drawPoint( -y + 500, -x + 500 )

		for polygon in self.polygons:
			polygon.draw( self.drawer )
		self.polygon_builder.draw( self.drawer )
		self.drawer.end()
