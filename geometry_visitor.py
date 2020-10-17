from abc import ABC, abstractmethod

from PyQt5.QtCore import QPoint


# from polygon import Polygon
# from polygon_objects import Vertex, Edge
# import polygon as polygon_module
# import polygon_objects


class GeometryObjectVisitor( ABC ):

	@abstractmethod
	def visit_vertex( self, vertex ) -> bool:
		return False

	@abstractmethod
	def visit_edge( self, edge ) -> bool:
		return False

	@abstractmethod
	def visit_polygon( self, polygon ) -> bool:
		return False
