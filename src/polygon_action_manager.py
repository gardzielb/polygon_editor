from typing import List, Optional

from PyQt5.QtCore import QPoint

from src.geometry_object import GeometryObject
from src.polygon import Polygon
from src.edit_visitor import EditGeometryObjectVisitor


class PolygonActionManager:

	def __init__( self ):
		self.polygon: Optional[Polygon] = None
		self.active_object: Optional[GeometryObject] = None
		self.remove_visitor: Optional[EditGeometryObjectVisitor] = None
		self.is_moving = False
		self.is_active = False

	def set_polygon( self, polygon: Polygon, active_object: GeometryObject, polygon_list: List[Polygon] ):
		self.polygon = polygon
		self.active_object = active_object
		self.remove_visitor = EditGeometryObjectVisitor( polygon, polygon_list )
		self.active_object.highlight = True
		self.is_active = True

	def edit_remove_object( self ) -> bool:
		return self.active_object.accept_visitor( self.remove_visitor )

	def release_object( self ):
		if self.is_active:
			self.active_object.highlight = False
			self.polygon.post_move_update()
			self.is_moving = False
			self.is_active = False

	def move_object( self, dest_point: QPoint ):
		self.active_object.move( dest_point.x(), dest_point.y() )

	def set_moving( self, is_moving: bool ):
		self.is_moving = is_moving
		self.polygon.is_moving = is_moving
