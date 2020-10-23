from PyQt5.QtWidgets import QMainWindow

from src.polygon_surface import PolygonSurface


class EditorWindow( QMainWindow ):
	def __init__( self ):
		super().__init__()
		self.setWindowTitle( 'Polygon Editor' )
		self.setCentralWidget( PolygonSurface() )
