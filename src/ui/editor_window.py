from PyQt5.QtWidgets import QMainWindow

from src.polygon_surface import PolygonSurface


class EditorWindow( QMainWindow ):
	def __init__( self ):
		super().__init__()

		menu = self.menuBar().addMenu( 'File' )
		save_action = menu.addAction( 'Save' )
		save_action.setShortcut( 'Ctrl+S' )
		load_action = menu.addAction( 'Load' )
		load_action.setShortcut( 'Ctrl+O' )
		settings_action = menu.addAction( 'Settings' )

		self.setWindowTitle( 'Polygon Editor' )
		polygon_surface = PolygonSurface()
		self.setCentralWidget( polygon_surface )

		save_action.triggered.connect( polygon_surface.save_polygons )
		load_action.triggered.connect( polygon_surface.load_polygons )
		settings_action.triggered.connect( polygon_surface.open_settings_dialog )
		settings_action.triggered.connect( polygon_surface.open_settings_dialog )
