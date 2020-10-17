from typing import Union

from PyQt5.QtCore import QPoint

from geometric_object import GeometricObject
from polygon import Polygon


class PolygonActionManager:

	def __init__( self ):
		self.polygon: Union[Polygon, None] = None
		self.active_object: Union[GeometricObject, None] = None
		self.is_moving = False
		self.is_active = False

	def set_polygon( self, polygon: Polygon, active_object: GeometricObject ):
		self.polygon = polygon
		self.active_object = active_object
		self.active_object.highlight = True
		self.is_active = True

	def release_object( self ):
		if self.is_active:
			self.active_object.highlight = False
			self.polygon.post_move_update()
			self.is_moving = False
			self.is_active = False

	def move_object( self, dest_point: QPoint ):
		self.active_object.move( dest_point )
