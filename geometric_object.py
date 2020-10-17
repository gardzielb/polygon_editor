from abc import ABC, abstractmethod
from typing import Union

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from geometry_drawer import GeometryDrawer


class GeometricObject( ABC ):
	NORMAL_STROKE_COLOR = QColor( 0, 0, 255 )
	NORMAL_FILL_COLOR = QColor( 200, 200, 200 )
	HIGHLIGHT_STROKE_COLOR = QColor( 0, 255, 0 )
	HIGHLIGHT_FILL_COLOR = QColor( 250, 250, 250 )

	def __init__( self ):
		self.move_origin: Union[QPoint, None] = None
		self.highlight = False

	@abstractmethod
	def draw_stroke( self, drawer: GeometryDrawer ):
		pass

	@abstractmethod
	def fill( self, drawer: GeometryDrawer ):
		pass

	@abstractmethod
	def move( self, dest_point: QPoint ):
		pass

	def draw( self, drawer: GeometryDrawer ):
		prev_pen = drawer.pen()
		prev_brush = drawer.brush()
		if self.highlight:
			print( "drawing highlighted object" )
			drawer.set_brush( self.HIGHLIGHT_FILL_COLOR )
			self.fill( drawer )
			drawer.set_pen( self.HIGHLIGHT_STROKE_COLOR )
			self.draw_stroke( drawer )
		else:
			drawer.set_brush( self.NORMAL_FILL_COLOR )
			self.fill( drawer )
			drawer.set_pen( self.NORMAL_STROKE_COLOR )
			self.draw_stroke( drawer )
		drawer.set_pen( prev_pen )
		drawer.set_brush( prev_brush )

	def start_moving( self, point: QPoint ):
		self.move_origin = point

	def end_moving( self ):
		self.move_origin = None
