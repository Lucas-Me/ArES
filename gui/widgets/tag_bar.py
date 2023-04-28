# IMPORT QT MODULES
from qt_core import *

# IMPORT MODULES
import numpy as np

# IMPORT CUSTOM WIDGETS
from gui.widgets.labels import ClickableLabel

class ColorTags(QWidget):

    def __init__(self, *args, **kwargs):
        # PRIVATE VARIABLES
        self.color_schema = {}
        self.tags = []
        self.tag_names = []

        # super init
        super().__init__(*args, **kwargs)

        # UI
        self.v_layout = QVBoxLayout(self)
        self.v_layout.setContentsMargins(2,2,2,2)
        self.v_layout.setSpacing(4)

    @Slot(object)
    def tagClicked(self, tag):
        print("clicado", tag)

    def updateTags(self, tag_names : list[str], colors):
        if tag_names == self.tag_names:
            return None
        
        self.clearTags()
        for i in range(len(tag_names)):
            # creating tag
            tag = TagButton(text = tag_names[i])

            # tag configs
            tag.hideButton()
            tag.text_clicked.connect(self.tagClicked)
            if not tag_names[i] in self.color_schema:
                self.color_schema[tag_names[i]] = next(colors)

            tag.setColor(self.color_schema[tag_names[i]])

            # storing widget
            self.tags.append(tag)
            self.v_layout.addWidget(tag)

    def clearTags(self):
        for index in reversed(range(self.v_layout.count())):
            # delete widget
            self.v_layout.itemAt(index).widget().deleteLater()
            
            # remove from layout
            self.v_layout.takeAt(index)
            
        self.tags.clear()
        self.tag_names.clear()
    

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
        self.line_edit.setPlaceholderText("Insira uma legenda...")

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
    text_clicked = Signal(object)
    def __init__(self, *args, **kwargs):
        super().__init__()

        # UI AND ASSETS
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.setContentsMargins(4, 4, 4, 4)
        self.setFixedHeight(30)
        
        # tag layout
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(4, 4, 4, 4)
        hbox.setSpacing(10)

        # TAG TEXT
        self.label = ClickableLabel(kwargs.pop('text', ''))
        self.label.setStyleSheet('border:0px')
        self.label.setFixedHeight(16)
        self.label.clicked.connect(lambda: self.text_clicked.emit(self))

        # button X
        self.x_button = QPushButton('x')
        self.x_button.setFixedSize(20, 20)
        self.x_button.setStyleSheet('border:0px; font-weight:bold')
        self.x_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        
        # add to tag layout
        hbox.addWidget(self.x_button)
        hbox.addWidget(self.label)

        # establishing signals
        self.x_button.clicked.connect(self.deleteTag)
    
    def deleteTag(self):
        self.clicked.emit(self)

    def hideButton(self):
        self.x_button.setHidden(True)

    def setColor(self, color):
        self.color = color

        # Calculate contrast between the selected color and (black, white)
        rgb = np.array(QColor(color).getRgb())[:-1]
        print(rgb)
        for i in range(3):
            rgb[i] = rgb[i] / 3294 if rgb[i] <= 10 else (rgb[i] / 269 + 0.0513) ** 2.4

        # Luminance
        L = np.sum(rgb * np.array([0.2126, 0.7152, 0.0722]))

        # CONTRAST RATIO BETWEEN THE COLOR AND WHITE
        contrast_ratio = (L + 0.05) / (1.05)
        minimum_contrast_ratio = 7
        text_color = "black" if contrast_ratio < minimum_contrast_ratio else 'white'

        # APPLYING STYLESHEET
        self.setStyleSheet(f'''
            background-color: {color};
            color: {text_color};
            font: bold 10pt 'Microsoft New Tai Lue';
            border-radius: 5px;
            border: 1px solid rgb(192, 192, 192);
            ''')

    def getColor(self):
        return self.color
    
    def getText(self):
        return self.label.text()
    
    def setText(self, text):
        self.label.setText(text)