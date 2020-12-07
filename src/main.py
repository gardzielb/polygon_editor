from PyQt5.QtWidgets import QApplication

from pathlib import Path
import sys

path = Path().absolute()
sys.path.append( str( path ) )

from src.ui.editor_window import EditorWindow

if __name__ == '__main__':
	app = QApplication( [] )

	window = EditorWindow()
	window.show()

	app.exec_()
