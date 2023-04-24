# IMPORT QT MODULES
from qt_core import *

class TagBar(QWidget):

    def __init__(self, *args, **kwargs):
        # PRIVATE VARIABLES
        self.nmax = kwargs.pop('max', 100)
        self.tags = []

        # super init
        super().__init__(*args, **kwargs)

        # UI
        self.h_layout = QHBoxLayout(self)
        self.h_layout.setContentsMargins(2,2,2,2)
        self.h_layout.setSpacing(4)

        # line edit
        self.line_edit = QLineEdit()
        self.line_edit.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # commands
        self.refresh()
        self.setup_ui()

    def setup_ui(self):
        self.line_edit.returnPressed.connect(self.create_tags)

    def create_tags(self):
        new_tags = self.line_edit.text().split(', ')
        self.line_edit.setText('')
        self.tags.extend(new_tags)
        print(self.tags)
        self.refresh()

    def refresh(self):
        for i in reversed(range(self.h_layout.count())):
            self.h_layout.itemAt(i).widget().setParent(None)

        for tag in self.tags:
            self.add_tag_to_bar(tag)
        
        # ADD TO WIDGET 
        self.h_layout.addWidget(self.line_edit)
        self.line_edit.setFocus()

    def add_tag_to_bar(self, text):

        # creating tag
        tag = TagButton(position = len(self.tags), text = text)
        
        # add to main layout
        self.h_layout.addWidget(tag)

        # signal
        tag.clicked.connect(lambda x: self.delete_tag(x))

    def delete_tag(self, index):
        del self.tags[index]
        self.refresh()


class TagButton(QFrame):
    
    clicked = Signal(int)
    def __init__(self, *args, **kwargs):
        super().__init__()
        
        # PRIVATE VARIABLES
        self.position = kwargs.pop('position')

        # UI AND ASSETS
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.setStyleSheet('border:1px solid rgb(192, 192, 192); border-radius: 4px;')
        self.setContentsMargins(2, 2, 2, 2)
        self.setFixedHeight(28)
        
        # tag layout
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(4, 4, 4, 4)
        hbox.setSpacing(10)

        # TAG TEXT
        label = QLabel(kwargs.pop('text', ''))
        label.setStyleSheet('border:0px')
        label.setFixedHeight(16)

        # button X
        x_button = QPushButton('x')
        x_button.setFixedSize(20, 20)
        x_button.setStyleSheet('border:0px; font-weight:bold')
        x_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        
        # add to tag layout
        hbox.addWidget(x_button)
        hbox.addWidget(label)

        # establishing signals
        x_button.clicked.connect(self.deleteTag)
    
    def deleteTag(self):
        self.clicked.emit(self.position)