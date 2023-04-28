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

        # insert line edit into layout
        self.h_layout.addWidget(self.line_edit)

        # signals and slots
        self.line_edit.returnPressed.connect(self.create_tags)

    def create_tags(self):
        # getting tag name
        new_tags = self.line_edit.text().split(', ')
        self.line_edit.setText('')
        
        # loop to create tags
        index = self.h_layout.count() - 1
        for i in range(len(new_tags)):
            
            # creating tag and appending into list
            tag = TagButton(text = new_tags[i])
            self.tags.append(tag)
            position = index + i

            # inserting into layout
            self.h_layout.insertWidget(position, tag)

            # delete when clicked
            tag.clicked.connect(lambda x: self.delete_tag(x))

            # check if maximum is reached
            if self.nmax == position + 1:
                self.line_edit.setHidden(True)
                break

    def delete_tag(self, tag_widget : QFrame):
        index = self.tags.index(tag_widget)

        # delete from layout
        self.h_layout.takeAt(index)

        # delete from list
        del self.tags[index]

        tag_widget.deleteLater()
        # show line edit if necessary
        self.line_edit.setHidden(False)

class TagButton(QFrame):
    
    clicked = Signal(object)
    def __init__(self, *args, **kwargs):
        super().__init__()

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
        self.clicked.emit(self)