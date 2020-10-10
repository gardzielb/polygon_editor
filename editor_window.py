from PyQt5.QtWidgets import QMainWindow
from ui_form import Ui_UiForm


class EditorWindow( QMainWindow ):
	def __init__( self ):
		super().__init__()

		self.ui = Ui_UiForm()
		self.ui.setupUi( self )
