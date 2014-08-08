import os
import dircache
import ntpath
from Status import Ui_MainWindow
from PyQt4.QtGui import QMainWindow, QHeaderView, QAbstractItemView, QTreeWidgetItem, QRadioButton, QButtonGroup, QFontMetrics
from PyQt4.QtCore import Qt, QSettings

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

class StatusView(QMainWindow):
    def __init__(self, paths):
        QMainWindow.__init__(self)

        self.settings = QSettings("Exile", "StatusView");

        #self.restoreGeometry(self.settings.value("myWidget/geometry").toByteArray())
        #saveGeometry()
        
        ui = Ui_MainWindow()
        ui.setupUi(self)

        self.tree = ui.treeWidget

        # Last column should not be the one stretching on resize, first one should
        self.tree.header().setStretchLastSection(False)
        self.tree.header().setResizeMode(0, QHeaderView.Stretch)

        self.resize_headers_to_minimum()

        # highlighting is distracting and buggy with checkboxes
        self.tree.setSelectionMode(QAbstractItemView.NoSelection)

        for p in paths:
            self.process_path(p)

        self.tree.expandAll()

    def resize_headers_to_minimum(self):
        maxWidth = 0
        header = self.tree.headerItem()
        for i in range(1, self.tree.columnCount()+1):
            fm = QFontMetrics(header.font(i))
            width = fm.width(header.text(i))
            if width > maxWidth:
                maxWidth = width
        maxWidth = maxWidth + 20
        for i in range(1, self.tree.columnCount()+1):
            self.tree.setColumnWidth(i, maxWidth)
    
    def tree_item_radio_clicked(self, button):
        self.uncheck_parents(button.treeItem)
        id = button.group().id(button)
        self.check_children(button.treeItem, id)

    def attach_data(self, item, data):
        item.my_data = data

    def retrieve_data(self, item):
        return item.my_data

    def process_path(self, path):
        item = self.add_node(self.tree, path)
        self.extend_tree(item)

    def uncheck_parents(self, item):
        parent = item.parent()
        while parent != None:
            parentFirstButton = self.tree.itemWidget(parent, 1)
            group = parentFirstButton.group()
            self.uncheck_group(group)
            parent = parent.parent()

    def check_children(self, item, id):
        child_count = item.childCount()
        for i in range(child_count):
            childItem = item.child(i)
            firstButton = self.tree.itemWidget(childItem, 1)
            group = firstButton.group()
            buttonToCheck = group.button(id)
            buttonToCheck.setChecked(True)
            self.check_children(childItem, id)

    def uncheck_group(self, group):
        checkedButton = group.checkedButton()
        if checkedButton != None:
            group.setExclusive(False);
            group.checkedButton().setChecked(False);
            group.setExclusive(True);
        
    def extend_tree(self, parentItem):
        parentDir = self.retrieve_data(parentItem)[0]
  
        subdirs = dircache.listdir(parentDir)
        subdirs.sort()
        for childDir in subdirs:
            child_path = os.path.join(parentDir, childDir)
            if os.path.isdir(child_path) and not os.path.islink(childDir):
                childItem = self.add_node(parentItem, child_path)
                self.extend_tree(childItem)

    def add_node(self, parentItem, path):
        item = QTreeWidgetItem(parentItem)
        item.setText(0, path_leaf(path))
        buttonGroup = QButtonGroup()

        # must keep reference to buttonGroup for its callback to work
        self.attach_data(item, (path, buttonGroup))

        for i in range(self.tree.columnCount() - 1):
            button = QRadioButton()
            buttonGroup.addButton(button, i) # id is the index
            button.treeItem = item
            self.tree.setItemWidget(item, i + 1, button)

        buttonGroup.buttonClicked.connect(self.tree_item_radio_clicked)

        return item