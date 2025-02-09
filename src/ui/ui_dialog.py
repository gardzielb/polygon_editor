# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/ui_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(332, 240)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(150, 190, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 10, 291, 161))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontal_radio_button = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.horizontal_radio_button.setObjectName("horizontal_radio_button")
        self.radio_button_group = QtWidgets.QButtonGroup(Dialog)
        self.radio_button_group.setObjectName("radio_button_group")
        self.radio_button_group.addButton(self.horizontal_radio_button)
        self.gridLayout.addWidget(self.horizontal_radio_button, 2, 0, 1, 1)
        self.length_radio_button = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.length_radio_button.setObjectName("length_radio_button")
        self.radio_button_group.addButton(self.length_radio_button)
        self.gridLayout.addWidget(self.length_radio_button, 3, 0, 1, 1)
        self.mid_point_radio_button = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.mid_point_radio_button.setChecked(True)
        self.mid_point_radio_button.setObjectName("mid_point_radio_button")
        self.radio_button_group.addButton(self.mid_point_radio_button)
        self.gridLayout.addWidget(self.mid_point_radio_button, 0, 0, 1, 1)
        self.length_spin_box = QtWidgets.QSpinBox(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.length_spin_box.sizePolicy().hasHeightForWidth())
        self.length_spin_box.setSizePolicy(sizePolicy)
        self.length_spin_box.setWrapping(False)
        self.length_spin_box.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.length_spin_box.setMinimum(10)
        self.length_spin_box.setMaximum(1000)
        self.length_spin_box.setObjectName("length_spin_box")
        self.gridLayout.addWidget(self.length_spin_box, 3, 1, 1, 1)
        self.vertical_radio_button = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.vertical_radio_button.setChecked(False)
        self.vertical_radio_button.setObjectName("vertical_radio_button")
        self.radio_button_group.addButton(self.vertical_radio_button)
        self.gridLayout.addWidget(self.vertical_radio_button, 1, 0, 1, 1)
        self.remove_constraint_radio_button = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.remove_constraint_radio_button.setObjectName("remove_constraint_radio_button")
        self.radio_button_group.addButton(self.remove_constraint_radio_button)
        self.gridLayout.addWidget(self.remove_constraint_radio_button, 4, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Edit edge"))
        self.horizontal_radio_button.setText(_translate("Dialog", "Horizontal constraint"))
        self.length_radio_button.setText(_translate("Dialog", "Fixed length constraint"))
        self.mid_point_radio_button.setText(_translate("Dialog", "Add point in the middle"))
        self.vertical_radio_button.setText(_translate("Dialog", "Vertical constraint"))
        self.remove_constraint_radio_button.setText(_translate("Dialog", "Remove constraint"))
