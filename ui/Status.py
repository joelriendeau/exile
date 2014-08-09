# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\joel\Documents\GitHub\exile\ui\Status.ui'
#
# Created: Fri Aug 08 22:47:58 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1092, 806)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setMargin(5)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeWidget = QtGui.QTreeWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setColumnCount(7)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.header().setCascadingSectionResizes(True)
        self.treeWidget.header().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.treeWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.applyButton = QtGui.QPushButton(self.centralwidget)
        self.applyButton.setMinimumSize(QtCore.QSize(100, 0))
        self.applyButton.setObjectName(_fromUtf8("applyButton"))
        self.horizontalLayout.addWidget(self.applyButton)
        self.cancelButton = QtGui.QPushButton(self.centralwidget)
        self.cancelButton.setMinimumSize(QtCore.QSize(100, 0))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Exile Status", None))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Path", None))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "Status", None))
        self.treeWidget.headerItem().setText(2, _translate("MainWindow", "Add", None))
        self.treeWidget.headerItem().setToolTip(2, _translate("MainWindow", "Add/Update", None))
        self.treeWidget.headerItem().setText(3, _translate("MainWindow", "Ign. Glob", None))
        self.treeWidget.headerItem().setToolTip(3, _translate("MainWindow", "Ignore Globally for all users", None))
        self.treeWidget.headerItem().setText(4, _translate("MainWindow", "Ign. Loc", None))
        self.treeWidget.headerItem().setToolTip(4, _translate("MainWindow", "Ignore Locally only for you", None))
        self.treeWidget.headerItem().setText(5, _translate("MainWindow", "Resolve", None))
        self.treeWidget.headerItem().setText(6, _translate("MainWindow", "No Op", None))
        self.treeWidget.headerItem().setToolTip(6, _translate("MainWindow", "Do nothing", None))
        self.applyButton.setText(_translate("MainWindow", "Apply", None))
        self.cancelButton.setText(_translate("MainWindow", "Cancel", None))

