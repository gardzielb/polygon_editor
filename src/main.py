from PyQt5.QtWidgets import QApplication

from src.ui.editor_window import EditorWindow

if __name__ == '__main__':
	app = QApplication( [] )

	window = EditorWindow()
	window.show()

	app.exec_()
