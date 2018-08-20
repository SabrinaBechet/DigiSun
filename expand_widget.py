import sys
from PyQt4 import QtGui

class SectionExpandButton(QtGui.QPushButton):
    """a QPushbutton that can expand or collapse its section
    """
    def __init__(self, item, text = "", parent = None):
        super(SectionExpandButton, self).__init__(text, parent)
        self.section = item
        self.clicked.connect(self.on_clicked)

    def on_clicked(self):
        """toggle expand/collapse of section by clicking
        """
        if self.section.isExpanded():
            self.section.setExpanded(False)
        else:
            self.section.setExpanded(True)


class CollapsibleDialog(QtGui.QDialog):
    """a dialog to which collapsible sections can be added;
    subclass and reimplement define_sections() to define sections and
        add them as (title, widget) tuples to self.sections
    """
    def __init__(self):
        super(CollapsibleDialog, self).__init__()
        self.tree = QtGui.QTreeWidget()
        self.tree.setHeaderHidden(True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.tree)
        self.setLayout(layout)
        self.tree.setIndentation(0)

        self.sections = []
        self.define_sections("group 1 ")
        self.define_sections("group 2 ")
        print(self.sections)
        self.add_sections()

    def add_sections(self):
        """adds a collapsible sections for every 
        (title, widget) tuple in self.sections
        """
        for (title, widget) in self.sections:
            button1 = self.add_button(title)
            section1 = self.add_widget(button1, widget)
            button1.addChild(section1)

    def define_sections(self, title):
        """reimplement this to define all your sections
        and add them as (title, widget) tuples to self.sections
        """
        widget = QtGui.QFrame(self.tree)
        layout = QtGui.QFormLayout(widget)
        drawing_operator = QtGui.QLineEdit()
        #layout.addWidget(drawing_operator)
        layout.addRow("test", drawing_operator)
        #title = "Group 1"
        self.sections.append((title, widget))

    def add_button(self, title):
        """creates a QTreeWidgetItem containing a button 
        to expand or collapse its section
        """
        item = QtGui.QTreeWidgetItem()
        self.tree.addTopLevelItem(item)
        self.tree.setItemWidget(item, 0, SectionExpandButton(item, text = title))
        return item

    def add_widget(self, button, widget):
        """creates a QWidgetItem containing the widget,
        as child of the button-QWidgetItem
        """
        section = QtGui.QTreeWidgetItem(button)
        section.setDisabled(True)
        self.tree.setItemWidget(section, 0, widget)
        return section


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = CollapsibleDialog()
    window.show()
    sys.exit(app.exec_())
