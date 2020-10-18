from abc import ABC, abstractmethod


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
