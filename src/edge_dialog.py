from PyQt5.QtWidgets import QDialog

from src.edge_action import EdgeAction, VerticalConstraintEdgeAction, HorizontalConstraintEdgeAction, \
	FixedLengthConstraintEdgeAction, AddMiddlePointEdgeAction, RemoveConstraintEdgeAction
from src.polygon import Polygon
from src.ui.ui_dialog import Ui_Dialog


class EdgeDialog( QDialog ):
	def __init__( self, edge_length: int ):
		super().__init__()

		self.ui = Ui_Dialog()
		self.ui.setupUi( Dialog = self )

		self.ui.length_spin_box.setValue( edge_length )
		self.ui.length_spin_box.setEnabled( False )
		for button in self.ui.radio_button_group.buttons():
			button.clicked.connect( self.__toggle_length_enabled__ )

	def get_action( self, polygon: Polygon ) -> EdgeAction:
		checked_button = self.ui.radio_button_group.checkedButton()
		if checked_button == self.ui.horizontal_radio_button:
			return HorizontalConstraintEdgeAction()
		elif checked_button == self.ui.vertical_radio_button:
			return VerticalConstraintEdgeAction()
		elif checked_button == self.ui.length_radio_button:
			return FixedLengthConstraintEdgeAction( length = self.ui.length_spin_box.value() )
		elif checked_button == self.ui.remove_constraint_radio_button:
			return RemoveConstraintEdgeAction()
		else:
			return AddMiddlePointEdgeAction( polygon )

	def __toggle_length_enabled__( self ):
		self.ui.length_spin_box.setEnabled( self.ui.length_radio_button.isChecked() )
