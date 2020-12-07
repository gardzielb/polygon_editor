from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter, QBrush, QColor, QPainterPath, QPaintDevice, QImage

from src.line_drawers import create_line_drawer_chain, draw_line_wu, draw_line_bresenham, draw_line_qt
from src.settings_dialog import LineSettings


class GeometryDrawer:

	def __init__( self ):
		self.painter = QPainter()
		self.bresenham_chain = create_line_drawer_chain( draw_line_bresenham )
		self.wu_chain = create_line_drawer_chain( draw_line_wu )
		self.qt_chain = create_line_drawer_chain( draw_line_qt )
		self.line_algorithm = LineSettings.BRESENHAM

	def draw_point( self, point: QPoint, radius: int ):
		for i in range( -radius, radius + 1 ):
			for j in range( -radius, radius + 1 ):
				self.painter.drawPoint( point.x() + i, point.y() + j )

	def draw_line( self, p1: QPoint, p2: QPoint ):
		point1 = p1
		point2 = p2
		if p1.x() > p2.x():
			point1 = p2
			point2 = p1

		if self.line_algorithm == LineSettings.QT_LIB:
			self.qt_chain.draw_line( point1, point2, self.painter )
		elif self.line_algorithm == LineSettings.WU:
			self.wu_chain.draw_line( point1, point2, self.painter )
		else:
			self.bresenham_chain.draw_line( point1, point2, self.painter )

	def draw_icon( self, icon_path: str, central_point: QPoint ):
		icon = QImage( icon_path )
		self.painter.drawImage( central_point.x() - icon.width() / 2, central_point.y() - icon.height() / 2, icon )

	def fill_polygon( self, polygon_path: QPainterPath ):
		self.painter.fillPath( polygon_path, self.painter.brush() )

	def begin( self, device: QPaintDevice ):
		self.painter.begin( device )

	def end( self ):
		self.painter.end()

	def pen( self ) -> QColor:
		return self.painter.pen()

	def brush( self ) -> QBrush:
		return self.painter.brush()

	def set_brush( self, color: QColor ):
		self.painter.setBrush( color )

	def set_pen( self, color: QColor ):
		self.painter.setPen( color )
