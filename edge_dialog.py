from PyQt5.QtWidgets import QDialog

from edge_action import EdgeAction, VerticalConstraintEdgeAction, HorizontalConstraintEdgeAction, \
	FixedLengthConstraintEdgeAction, AddMiddlePointEdgeAction
from polygon import Polygon
from ui_dialog import Ui_Dialog


class EdgeDialog( QDialog ):
	def __init__( self ):
		super().__init__()

		self.ui = Ui_Dialog()
		self.ui.setupUi( Dialog = self )

	def get_action( self, polygon: Polygon ) -> EdgeAction:
		checked_button = self.ui.radio_button_group.checkedButton()
		if checked_button == self.ui.horizontal_radio_button:
			return HorizontalConstraintEdgeAction()
		elif checked_button == self.ui.vertical_radio_button:
			return VerticalConstraintEdgeAction()
		elif checked_button == self.ui.length_radio_button:
			return FixedLengthConstraintEdgeAction( length = self.ui.length_spin_box.value() )
		else:
			return AddMiddlePointEdgeAction( polygon )
