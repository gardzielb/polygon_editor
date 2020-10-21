from typing import List, Union

from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPainterPath, QColor

from geometry_object import GeometryObject
from geometry_drawer import GeometryDrawer
from edge import Edge
from vertex import Vertex
from geometry_visitor import GeometryObjectVisitor


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
		self.move_origin: Union[QPoint, None] = None

		for i in range( len( vertices ) ):
			i2 = (i + 1) % len( vertices )
			self.edges.append( Edge( vertices[i].point, vertices[i2].point ) )

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

	def move( self, dest_point: QPoint ):
		if self.move_origin:
			x_move = dest_point.x() - self.move_origin.x()
			y_move = dest_point.y() - self.move_origin.y()
			for vertex in self.vertices:
				vertex.move( dest_point = QPoint( vertex.point.x() + x_move, vertex.point.y() + y_move ) )
		self.move_origin = dest_point

	def is_hit( self, hit: QPoint ) -> bool:
		return self.painter_path.contains( hit )

	def accept_visitor( self, visitor: GeometryObjectVisitor ) -> bool:
		return visitor.visit_polygon( polygon = self )

	def post_move_update( self ):
		self.is_moving = False
		self.painter_path = self.__update_painter_path__()
		for edge in self.edges:
			edge.post_move_update()

	def search_for_hit( self, point: QPoint ) -> Union[GeometryObject, None]:
		objects: List[GeometryObject] = self.vertices.copy()
		objects.extend( self.edges )
		objects.append( self )
		for obj in objects:
			if obj.is_hit( hit = point ):
				return obj
		return None

	def get_bounding_box( self ) -> QRect:
		x_min = min( [v.point.x() for v in self.vertices] )
		x_max = max( [v.point.x() for v in self.vertices] )
		y_min = min( [v.point.y() for v in self.vertices] )
		y_max = max( [v.point.y() for v in self.vertices] )
		return QRect( x_min, y_min, x_max - x_min, y_max - y_min )

	def __update_painter_path__( self ) -> QPainterPath:
		path = QPainterPath( self.vertices[0].point )
		for i in range( 1, len( self.vertices ) ):
			path.lineTo( self.vertices[i].point )
		return path
