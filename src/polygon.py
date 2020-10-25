from typing import List, Optional

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainterPath, QColor

from src.edge import Edge
from src.geometry_drawer import GeometryDrawer
from src.geometry_object import GeometryObject
from src.geometry_visitor import GeometryObjectVisitor
from src.vertex import Vertex


class Polygon( GeometryObject ):
	DEFAULT_PEN = QColor( 0, 0, 255 )
	DEFAULT_BRUSH = QColor( 102, 178, 255, 80 )
	HIGHLIGHT_BRUSH = QColor( 255, 102, 178, 80 )

	def __init__( self, vertices: List[Vertex] ):
		super().__init__()

		self.vertices: List[Vertex] = vertices
		self.edges: List[Edge] = []
		self.painter_path = self.__update_painter_path__()
		self.is_moving = False
		self.move_origin: Optional[QPoint] = None

		for i in range( len( vertices ) ):
			i2 = (i + 1) % len( vertices )
			self.edges.append( Edge( vertices[i], vertices[i2] ) )

	def draw( self, drawer: GeometryDrawer, is_highlighted = False ):
		prev_pen = drawer.pen()
		prev_brush = drawer.brush()
		drawer.set_pen( self.DEFAULT_PEN )
		drawer.set_brush( self.DEFAULT_BRUSH )

		if not self.is_moving:
			if self.highlight:
				drawer.set_brush( self.HIGHLIGHT_BRUSH )
			drawer.fill_polygon( self.painter_path )

		for edge in self.edges:
			edge.draw( drawer )
		for vertex in self.vertices:
			vertex.draw( drawer )

		drawer.set_pen( prev_pen )
		drawer.set_brush( prev_brush )

	def move( self, dest_x: int, dest_y: int ):
		if self.move_origin:
			x_move = dest_x - self.move_origin.x()
			y_move = dest_y - self.move_origin.y()
			for vertex in self.vertices:
				vertex.move_carelessly( vertex.point.x() + x_move, vertex.point.y() + y_move )
		self.move_origin = QPoint( dest_x, dest_y )

	def is_hit( self, hit: QPoint ) -> bool:
		return self.painter_path.contains( hit )

	def accept_visitor( self, visitor: GeometryObjectVisitor ) -> bool:
		return visitor.visit_polygon( polygon = self )

	def post_move_update( self ):
		self.is_moving = False
		self.move_origin = None
		self.painter_path = self.__update_painter_path__()
		for edge in self.edges:
			edge.post_move_update()

	def search_for_hit( self, point: QPoint ) -> Optional[GeometryObject]:
		objects: List[GeometryObject] = self.vertices.copy()
		objects.extend( self.edges )
		objects.append( self )
		for obj in objects:
			if obj.is_hit( hit = point ):
				return obj
		return None

	def __update_painter_path__( self ) -> QPainterPath:
		path = QPainterPath( self.vertices[0].point )
		for i in range( 1, len( self.vertices ) ):
			path.lineTo( self.vertices[i].point )
		return path
