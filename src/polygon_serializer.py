import pickle
from typing import List
from pathlib import Path

from src.polygon import Polygon


class PolygonSerializer:

	def __init__( self, polygon: Polygon ):
		self.vertices = polygon.vertices
		self.edges = polygon.edges


def serialize_polygons( polygons: List[Polygon], file_path: str ):
	if Path( file_path ).is_file():
		mode = 'w+b'
	else:
		mode = 'x+b'

	serializers = [PolygonSerializer( polygon ) for polygon in polygons]
	with open( file_path, mode ) as file:
		pickle.dump( obj = serializers, file = file )


def deserialize_polygons( file_path ) -> List[Polygon]:
	if not Path( file_path ).is_file():
		return []

	with open( file_path, mode = 'r+b' ) as file:
		serializer_list = pickle.load( file = file )

	polygons: List[Polygon] = []
	for serializer in serializer_list:
		polygon = Polygon( serializer.vertices )
		polygon.edges = serializer.edges
		polygons.append( polygon )
	return polygons
