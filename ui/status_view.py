import os
import dircache
import ntpath
from Status import Ui_MainWindow
from PyQt4.QtGui import QMainWindow, QHeaderView, QAbstractItemView, QTreeWidgetItem, QRadioButton, QButtonGroup, QFontMetrics, QBrush, QColor
from PyQt4.QtCore import Qt, QSettings, QPoint, QSize

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

class StatusView(QMainWindow):
    def __init__(self, file_dict, apply_callback):
        QMainWindow.__init__(self)

        self.apply_callback = apply_callback

        self.uncheckableColumns = 2

        self.settings = QSettings("Exile", "StatusView")
        self.settings.beginGroup("status_view")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        self.tree = self.ui.treeWidget

        # Last column should not be the one stretching on resize, first one should
        self.tree.header().setStretchLastSection(False)
        self.tree.header().setResizeMode(0, QHeaderView.Stretch)

        self.resize_headers_to_minimum()

        # highlighting is distracting and buggy with checkboxes
        self.tree.setSelectionMode(QAbstractItemView.NoSelection)

        self.ui.applyButton.clicked.connect(self.apply_clicked)
        self.ui.closeButton.clicked.connect(self.close_clicked)

        self.process_dict(file_dict, self.tree)

        self.tree.expandAll()

    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry());

    def resize_headers_to_minimum(self):
        maxWidth = 0
        header = self.tree.headerItem()
        for i in range(self.uncheckableColumns, self.tree.columnCount()+1):
            fm = QFontMetrics(header.font(i))
            width = fm.width(header.text(i))
            if width > maxWidth:
                maxWidth = width
        maxWidth = maxWidth + 20
        for i in range(self.uncheckableColumns, self.tree.columnCount()+1):
            self.tree.setColumnWidth(i, maxWidth)
    
    def tree_item_radio_clicked(self, button):
        self.uncheck_parents(button.treeItem)
        id = button.group().id(button)
        if id == 1 or id == 2: # ignore columns
            self.enable_children(button.treeItem, False)
        else:
            self.enable_children(button.treeItem, True)
            self.check_children(button.treeItem, id)

    def apply_clicked(self):
        new_file_dict = self.apply_callback(self.harvest_form())
        self.tree.clear()
        self.process_dict(new_file_dict, self.tree)
        self.tree.expandAll()
        return

    def close_clicked(self):
        self.close()
        return

    def attach_data(self, item, data):
        item.my_data = data

    def retrieve_data(self, item):
        try:
            return item.my_data
        except:
            return None

    def process_dict(self, file_dict, parent_item):
        if file_dict == None:
            return
        for k,v in sorted(file_dict.items()):
            if isinstance(v, dict):
                item = self.add_node(parent_item, k, "DIR")
                self.process_dict(v, item)
            elif isinstance(v, basestring):
                self.add_node(parent_item, k, v)

    def uncheck_parents(self, item):
        parent = item.parent()
        while parent != None:
            parentFirstButton = self.tree.itemWidget(parent, self.uncheckableColumns + 1)
            group = parentFirstButton.group()
            self.uncheck_group(group)
            parent = parent.parent()

    def check_children(self, item, id):
        child_count = item.childCount()
        for i in range(child_count):
            childItem = item.child(i)
            firstButton = self.tree.itemWidget(childItem, self.uncheckableColumns + 1)
            group = firstButton.group()
            buttonToCheck = group.button(id)
            if buttonToCheck != None:
                if buttonToCheck.isEnabled():
                    buttonToCheck.setChecked(True)
                else:
                    self.uncheck_group(group)
            self.check_children(childItem, id)

    def enable_children(self, item, enabled):
        child_count = item.childCount()
        for i in range(child_count):
            childItem = item.child(i)
            firstButton = self.tree.itemWidget(childItem, self.uncheckableColumns + 1)
            group = firstButton.group()
            if not enabled:
                self.uncheck_group(group)
            all_buttons = group.buttons()
            for button in all_buttons:
                button.setEnabled(enabled)
            self.enable_children(childItem, enabled)

    def uncheck_group(self, group):
        checkedButton = group.checkedButton()
        if checkedButton != None:
            group.setExclusive(False);
            group.checkedButton().setChecked(False);
            group.setExclusive(True);

    def add_node(self, parentItem, path, type):
        item = QTreeWidgetItem(parentItem)
        item.setText(0, path_leaf(path))
        buttonGroup = QButtonGroup()

        isNewFile = type is "UNTRACKED"
        isModifiedFile = type is "MODIFIED"
        isMissing = type is "MISSING"
        isDirectory = type is "DIR"

        if isNewFile:
            item.setText(1, type)
            item.setForeground(1, QBrush(QColor(0, 255, 0)))
        if isModifiedFile:
            item.setText(1, type)
            item.setForeground(1, QBrush(QColor(0, 0, 255)))
        if isMissing:
            item.setText(1, type)
            item.setForeground(1, QBrush(QColor(255, 0, 0)))
        if isDirectory:
            for i in range(self.tree.columnCount()):
                item.setBackground(i, QBrush(QColor(230, 230, 255)))

        # must keep reference to buttonGroup for its callback to work
        parent_data = self.retrieve_data(parentItem)
        if parent_data != None:
            path = os.path.join(parent_data[0], path)
        self.attach_data(item, (path, buttonGroup, type))

        for i in range(self.uncheckableColumns, self.tree.columnCount()):
            if i == self.tree.columnCount() - 7 and isMissing:
                continue # option to add not enabled for missing files
            if i == self.tree.columnCount() - 4 and isNewFile:
                continue # option to resolve not enabled for new files
            if i == self.tree.columnCount() - 3 and isNewFile:
                continue # option to stop tracking not enabled for untracked files
            if i == self.tree.columnCount() - 2 and isMissing:
                continue # option to delete not enabled for missing files
            if i == self.tree.columnCount() - 2 and isDirectory:
                continue # option to delete not enabled for directories, too dangerous
            button = QRadioButton()
            buttonGroup.addButton(button, i - self.uncheckableColumns) # id is the index
            button.treeItem = item
            self.tree.setItemWidget(item, i, button)

        buttonGroup.buttonClicked.connect(self.tree_item_radio_clicked)

        return item

    def harvest_form(self):
        result = {}

        result["add"] = []
        result["ignore_glob"] = []
        result["ignore_loc"] = []
        result["resolve"] = []
        result["stop_track"] = []
        result["delete"] = []

        result_map = [] # lookup of button index to value
        result_map.append("add")
        result_map.append("ignore_glob")
        result_map.append("ignore_loc")
        result_map.append("resolve")
        result_map.append("stop_track")
        result_map.append("delete")

        root = self.tree.invisibleRootItem()
        self.harvest_node(result, result_map, root)
        return result

    def harvest_node(self, result, result_map, item):
        child_count = item.childCount()
        for i in range(child_count):
            childItem = item.child(i)
            firstButton = self.tree.itemWidget(childItem, self.uncheckableColumns + 1)
            group = firstButton.group()
            checkedId = group.checkedId()
            if checkedId >= 0 and checkedId < len(result_map):
                path = self.retrieve_data(childItem)[0]
                type = self.retrieve_data(childItem)[2]
                result[result_map[checkedId]].append((path,type))
            self.harvest_node(result, result_map, childItem)