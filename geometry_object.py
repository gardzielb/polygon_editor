from abc import ABC, abstractmethod

from PyQt5.QtCore import QPoint

from geometry_drawer import GeometryDrawer
from geometry_visitor import GeometryObjectVisitor


class GeometryObject( ABC ):

	def __init__( self ):
		self.highlight = False

	@abstractmethod
	def draw( self, drawer: GeometryDrawer ):
		pass

	@abstractmethod
	def move( self, dest_point: QPoint ):
		pass

	@abstractmethod
	def is_hit( self, hit: QPoint ) -> bool:
		return False

	@abstractmethod
	def accept_visitor( self, visitor: GeometryObjectVisitor ) -> bool:
		return False
