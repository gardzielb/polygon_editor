from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QMenuBar

from src.polygon_surface import PolygonSurface


class EditorWindow( QMainWindow ):
	def __init__( self ):
		super().__init__()

		menu = self.menuBar().addMenu( 'File' )
		save_action = menu.addAction( 'Save' )
		load_action = menu.addAction( 'Load' )

		self.setWindowTitle( 'Polygon Editor' )
		polygon_surface = PolygonSurface()
		self.setCentralWidget( polygon_surface )

		save_action.triggered.connect( polygon_surface.save_polygons )
		load_action.triggered.connect( polygon_surface.load_polygons )
