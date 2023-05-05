# QT MODULES
import PySide6.QtGui
from qt_core import *

# IMPORTING MODULES
import numpy as np

def calculateLuminance(rgb : np.array):
    # Calculate luminance of a color
    rgb = np.array(rgb)
    rgb2 = np.where(rgb <= 10, rgb / 3294, (rgb / 269 + 0.0513) ** 2.4)

    # Luminance
    L = np.sum(rgb2 * np.array([0.2126, 0.7152, 0.0722]))

    return L


class ColorMap(QWidget):
    
    def __init__(self, *args, **kwargs):
        # PRIVATE VARIABLES
        self.gradient_ = QLinearGradient()

        # SETTINGS
        self.gradient_.setStart(0, 0)
        self.gradient_.setFinalStop(1, 0)
        self.gradient_.setCoordinateMode(QGradient.ObjectBoundingMode)

        # INIT
        super().__init__(*args, **kwargs)

    def paintEvent(self, event: QPaintEvent) -> None:
        # super().paintEvent()

        # creating painter
        painter = QPainter()
        painter.begin(self)

        # painting box
        painter.fillRect(QRect(0, 0, self.width(), self.height()), self.gradient_)
        painter.end()

    def refreshColors(self, colors):
        self.gradient_ = QLinearGradient()
        self.gradient_.setStart(0, 0)
        self.gradient_.setFinalStop(1, 0)
        self.gradient_.setCoordinateMode(QGradient.ObjectBoundingMode)

        # adding colors
        n = len(colors)
        positions = np.linspace(0, 1, n)
        for i in range(n):
            self.gradient_.setColorAt(positions[i], colors[i])

        # update colormap
        self.update()
        

class ColormapWidget(QFrame):

    def __init__(self, *args, **kwargs):
        # PRIVATE VARIABLES
        self.colormap_ = ColorMap()
        self.sliders_ = ColormapMarkers()

        # INIT
        super().__init__(*args, **kwargs)

        # SETUP UI
        self.ui = ViewerUI()
        self.ui.setup_ui(self)

        # settings
        self.setFixedHeight(300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # SIGNALS AND SLOTS
        self.refreshWidgets()

    def refreshWidgets(self):
        # gradient colors
        self.colormap_.refreshColors(
            colors = self.sliders_.getColors(),
        )

        # markers
        self.sliders_.refreshItems()

    
class ViewerUI(object):

    def setup_ui(self, parent : ColormapWidget):

        if not parent.objectName():
            parent.setObjectName("colormap")

        # MAIN LAYOUT
        self.main_layout = QVBoxLayout(parent)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(0)

        # ADD TO MAIN LAYOUT
        self.main_layout.addWidget(parent.colormap_)
        self.main_layout.addWidget(parent.sliders_)

        parent.colormap_.setFixedHeight(60)
        parent.sliders_.setFixedHeight(30)

class ColormapMarkers(QWidget):

    def __init__(self, *args, **kwargs):
        # PRIVATE VARIABLES
        self.markers = [ColorMark('#000000'), ColorMark('#ffffff')]

        # INIT
        super().__init__()

        # LAYOUT
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def refreshItems(self):
        # removing children
        for i in range(self.main_layout.count()):
            self.main_layout.itemAt(i).widget().deleteLater()
            #
            self.main_layout.takeAt(i)

        # inserting children
        for i in range(len(self.markers)):
            if i > 0:
                self.main_layout.addItem(QSpacerItem(30, 30, QSizePolicy.MinimumExpanding))
            
            # add marker
            self.main_layout.addWidget(self.markers[i])

    def getColors(self):
        return [marker.getColor() for marker in self.markers]


class ColorMark(QWidget):

    def __init__(self, color : str):
        # INIT
        super().__init__()

        # SETTINGS
        self.setColor(color)
        self.setFixedWidth(20)

    def setColor(self, color : str):
        self.color = QColor(color)

        # COR DA BORDA
        # Calculate contrast between the selected color and (black, white)
        L1 = calculateLuminance(self.color.getRgb()[:-1])
        L2 = calculateLuminance(QColor('white').getRgb()[:-1])

        # CONTRAST RATIO BETWEEN THE COLOR AND WHITE
        contrast_ratio = (L1 + 0.05) / (L2 + 1.05)
        minimum_contrast_ratio = 0.5
        border_color = "#000000" if contrast_ratio > minimum_contrast_ratio else '#ffffff'
        self.border_color = border_color

        # APPLYING STYLESHEET
        self.setStyleSheet(f'''
            background-color: {color};
            border-radius: 5px;
            border: 2px solid {border_color};
            ''')

    def getColor(self):
        return self.color.name()
    
    def paintEvent(self, event: QPaintEvent) -> None:
        # super().paintEvent(event)

        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)