# IMPORTS
import os

# IMPORT QT CORE
from qt_core import *

class PyPushButton(QPushButton):

    def __init__(
        self,
        text = "",
        height = 40, 
        width = 70,
        text_padding = 60,
        text_color = '#ffffff',
        icon_path = "",
        icon_color = '#ffffff',
        btn_color = '#2874bf',
        btn_hover = '#1e588f',
        is_active = False,
        icon_width = 70,
        setup = True,
        ) -> None:
        super().__init__()

        # Set default parameters
        self.setText(text)
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        self.setMinimumWidth(width)
        self.setMaximumWidth(width)
        self.setCursor(Qt.PointingHandCursor)

        # Custom Paramters
        self.text_padding = text_padding
        self.text_color = text_color
        self.icon_path = icon_path
        self.icon_color = icon_color
        self.icon_width = icon_width
        self.btn_color = btn_color
        self.btn_hover = btn_hover
        self.is_active = is_active

        # Set style
        if setup:
            self.set_style(
                text_padding = self.text_padding,
                text_color = self.text_color,
                btn_color = self.btn_color,
                btn_hover = self.btn_hover,
                is_active = self.is_active
            )

    def set_style(
        self,
        text_padding = 55,
        text_color = '#000000',
        btn_color = '#000000',
        btn_hover = '#1e588f',
        is_active = False
    ):
        style = f"""
        QPushButton {{
            color : {text_color};
            background-color: {btn_color};
            padding-left: {text_padding}px;
            font: 700 12pt 'Microsoft New Tai Lue';
            text-align: left;
            vertical-align: middle;
            border: none;
            border-radius: 10px;
            margin-left: 10px
        }}
        QPushButton:hover {{
            color: {btn_hover};
        }}
        """

        self.setStyleSheet(style)
        self.update_style(text_color, btn_color, is_active)

    def set_active(self, status : bool):
        self.is_active = status
        self.update_style(
            text_color = self.text_color,
            btn_color = self.btn_color,
            is_active = self.is_active,
            )

    def update_style(self,
        text_color = '#000000',
        btn_color = '#000000',
        is_active = False
    ):
        style = self.styleSheet()
        options = [text_color, btn_color]
        self.icon_color = options[is_active]


        active_style = f"""
            QPushButton {{
                background-color: {options[not is_active]};
                color: {options[is_active]};
            }}
        """

        self.setStyleSheet(style + active_style)

    def paintEvent(self, event) -> None:
        # Return default style
        QPushButton.paintEvent(self, event)

        # Painter
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        qp.setPen(Qt.NoPen)

        rect = QRect(0, 0, self.icon_width, self.height())
        
        self.draw_icon(qp, self.icon_path, rect, self.icon_color)
        
        qp.end()

    def enterEvent(self, event:QEnterEvent) -> None:
        '''
        Se o mouse estiver sobre o botao, pinta o icone de amarelo.
        '''
        self.icon_color = '#ffb703'
        self.update()
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        '''
        Se o mouse deixar o botao, pinta o icon da cor original.
        '''
        self.update_style(self.text_color, self.btn_color, self.is_active)
        self.update()
        
        return super().leaveEvent(event)

    def draw_icon(self, qp, image, rect, color):
        # format Path
        app_path = os.path.abspath(os.getcwd())
        folder = "gui/images/icons"
        path = os.path.join(app_path, folder)
        icon_path = os.path.normpath(os.path.join(path, image))

        # Draw icon
        icon = QPixmap(icon_path)

        # scale icon ot dimensions
        icon = icon.scaled(icon.width(), icon.height(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)

        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), color)
        qp.drawPixmap(
            (rect.width() - icon.width()) / 2,
            (rect.height() - icon.height()) / 2,
            icon
        )
        painter.end()


class ClassicButton(QPushButton):

    def __init__(
        self,
        text = "",
        height = 40, 
        width = 70,
        icon_path = "",
        icon_width = 70,
        icon_allign = "left",
        icon_color = "#000000",
        paint_icon = True,
        hover_color = None
        ) -> None:
        super().__init__()

        # Set default parameters
        self.setText(text)
        self.setFixedSize(QSize(width, height))
        self.setCursor(Qt.PointingHandCursor)

        # Custom Paramters
        self.icon_path = icon_path
        self.icon_width = icon_width
        self.icon_allign = icon_allign
        self.color = icon_color
        self.icon_color = icon_color
        self.hover_color = icon_color if hover_color is None else hover_color
        self.allign_left = icon_allign == 'left'
        self.paint_icon = paint_icon

    def paintEvent(self, event) -> None:
        # Return default style
        QPushButton.paintEvent(self, event)

        # Painter
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        qp.setPen(Qt.NoPen)

        rect = QRect(0, 0, self.width(), self.height())
        
        self.draw_icon(qp, self.icon_path, rect, self.icon_color)
        
        qp.end()

    def draw_icon(self, qp, image, rect, color):
        # format Path
        app_path = os.path.abspath(os.getcwd())
        folder = "gui/images/icons"
        path = os.path.join(app_path, folder)
        icon_path = os.path.normpath(os.path.join(path, image))

        # icon dimensions
        margin = 10
        icon = QPixmap(icon_path)
        icon_dx, icon_dy = icon.width(), icon.height()
        dx = self.icon_width
        dy = dx * icon_dy // icon_dx
        x =  margin if self.allign_left else rect.width() - dx - margin
        y = (rect.height() - dy) // 2 # margins

        # scale icon ot dimensions
        icon = icon.scaled(dx, dy, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
                
        # draw icon
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        if self.paint_icon:
            painter.fillRect(icon.rect(), color)
        qp.drawPixmap(x, y, dx, dy, icon)
        painter.end()

    def enterEvent(self, event:QEnterEvent) -> None:
        '''
        Se o mouse estiver sobre o botao, pinta o icone de amarelo.
        '''
        self.icon_color = self.hover_color
        self.update()

        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        '''
        Se o mouse deixar o botao, pinta o icon da cor original.
        '''
        self.icon_color = self.color
        self.update()
        
        return super().leaveEvent(event)