from enum import Enum

from PyQt5.QtWidgets import QDialog

from src.ui.ui_settings import Ui_SettingsDialog


class LineSettings( Enum ):
	QT_LIB = 0
	BRESENHAM = 1
	WU = 2


class SettingsDialog( QDialog ):

	def __init__( self, line_algorithm ):
		super().__init__()

		self.ui = Ui_SettingsDialog()
		self.ui.setupUi( self )

		self.line_algorithm = line_algorithm
		if self.line_algorithm == LineSettings.QT_LIB:
			self.ui.qt_radio_button.setChecked( True )
		elif self.line_algorithm == LineSettings.WU:
			self.ui.wu_radio_button.setChecked( True )
		else:
			self.ui.bresenham_radio_button.setChecked( True )

	def get_chosen_value( self ) -> LineSettings:
		if self.ui.qt_radio_button.isChecked():
			return LineSettings.QT_LIB
		elif self.ui.bresenham_radio_button.isChecked():
			return LineSettings.BRESENHAM
		return LineSettings.WU
