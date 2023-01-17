# IMPORTS
import os

# IMPORT QT CORE
from qt_core import *

class StaticButton(QPushButton):

    def __init__(
        self,
        text = "",
        text_padding = 0,
        btn_height = 20, 
        btn_width = 20,
        icon_path = "",
        icon_color = '#d40055',
        btn_color = "#ffffff",
        btn_hover = "#ffffff",
        btn_pressed = "#ffffff",
        icon_x = 0,
        icon_y = 0,
        icon_width = 20,
        icon_height = 20,
        ) -> None:
        super().__init__()

        # Set default parameters
        self.setText(text)
        self.setMinimumHeight(btn_height)
        self.setMaximumHeight(btn_height)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumWidth(btn_width)
        self.setMaximumWidth(btn_width)

        # Custom Paramters
        self.left_padding = text_padding
        self.btn_height = btn_height
        self.btn_width = btn_width
        self.icon_path = icon_path
        self.icon_color = icon_color
        self.btn_color = btn_color
        self.btn_hover = btn_hover
        self.btn_pressed = btn_pressed
        self.icon_x = icon_x
        self.icon_y = icon_y
        self.icon_width = icon_width
        self.icon_height = icon_height 
        self.use_icon = True if len(icon_path) > 0 else False

        # Set style
        self.set_style(
            btn_color = self.btn_color,
            btn_hover = self.btn_hover,
            btn_pressed = self.btn_pressed,
            text_padding = self.left_padding
        )

    def set_style(
        self,
        btn_color = '#000000',
        btn_hover = '#1e588f',
        btn_pressed = '#88b9e7',
        text_padding = 0
    ):
        style = f"""
        QPushButton {{
            background-color: {btn_color};
            text-align: left;
            padding-left : {text_padding}px;
            border: none;
        }}
        QPushButton:hover {{
            background-color: {btn_hover};
        }}
        QPushButton:pressed {{
            background-color: {btn_pressed};
        }}
        """

        self.setStyleSheet(style)

    def update_dimensions(self, w, h):
        self.setMinimumWidth(w)
        self.setMaximumWidth(w)
        self.setMinimumHeight(h)
        self.setMaximumHeight(h)

    def paintEvent(self, event) -> None:
        # Return default style
        QPushButton.paintEvent(self, event)

        if self.use_icon:
            # Painter
            qp = QPainter()
            qp.begin(self)
            qp.setRenderHint(QPainter.Antialiasing)
            qp.setPen(Qt.NoPen)

            rect = QRect(self.icon_x, self.icon_y, self.icon_width, self.icon_height)
            self.draw_icon(qp, self.icon_path, rect)
            
            qp.end()
    
    def draw_icon(self, qp, image, rect):
        # format Path
        app_path = os.path.abspath(os.getcwd())
        folder = "gui/images/icons"
        path = os.path.join(app_path, folder)
        icon_path = os.path.normpath(os.path.join(path, image))

        # Draw icon
        icon = QPixmap(icon_path)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        qp.drawPixmap(
            (rect.width() - icon.width()) / 2,
            (rect.height() - icon.height()) / 2,
            icon
        )
        painter.end()