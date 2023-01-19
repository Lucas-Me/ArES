# IMPORTS
import os, gc, time

# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from gui.widgets.station_list_item_qwidget import StationListItem

# IMPORT UI MODULES
from gui.ui_widgets.ui_py_station_list_view import UI_PyStationListView

class PyStationListView(QListWidget):

    def __init__(self, parent) -> None:
        super().__init__()

        # Properties
        self.parent = parent
        self.itemWidth = 390
        self.itemHeight = 60
        self.existing_items = 0
        self.deleted_items = []
        self.active_row = QSpinBox()
        
        # configuring widgets
        self.active_row.setRange(-1, 1000)
        self.active_row.setValue(-1)
        self.verticalScrollBar().setSingleStep(1)

        # animation properties
        self.delete_parallel_animation = QParallelAnimationGroup()
        self.reposition_parallel_animation = QParallelAnimationGroup()

        # Configuring UI
        self.ui = UI_PyStationListView()
        self.ui.setup_ui(self)

        # Signals and Slots
        self.delete_parallel_animation.finished.connect(self.reposition_animation)
        self.reposition_parallel_animation.finished.connect(self.delete_list_widget)
        self.verticalScrollBar().valueChanged.connect(self.scroll_bar_adjust)
        self.itemClicked.connect(self.toggle_animation)

    def toggle_animation(self, WidgetItem : QListWidgetItem):
        active_row = self.active_row.value()
        station_item = self.itemWidget(WidgetItem)
        item_row = self.row(WidgetItem)

        # Check if already selected
        if active_row != item_row:
            if active_row >= 0:
                self.itemWidget(self.item(active_row)).change_color('#ffffff')
        
            station_item.change_color('#ededff', highlight = True)
            self.active_row.setValue(item_row)

    def add_station_item(self, station_object):
        # Creating QListWidgetItem and adding it to List
        list_widget_item = QListWidgetItem(self)
        self.addItem(list_widget_item)

        # creating StationListItem 
        station_item = StationListItem(
            station_object = station_object,
            item_width = self.itemWidth,
            item_height = self.itemHeight
            )

        # Setting Size Hint to ListWidgetItem
        SizeHint = QSize(self.itemWidth, self.itemHeight)
        list_widget_item.setSizeHint(SizeHint)

        # Setting StationListItem to QListWidgetItem
        self.setItemWidget(list_widget_item, station_item)

        # SIGNALS AND SLOTS
        station_item.ui.close_button.clicked.connect(
            lambda x: self.remove_btn(list_widget_item)
            )
        
        # toggle add animation
        # station_item.insert_animation()

        # update private variable
        self.updateExistingItems(1)

    def updateExistingItems(self, value):
        self.existing_items = self.existing_items + value
        
    def resizeEvent(self, e: QResizeEvent) -> None:
        self.scroll_bar_adjust()
        return super().resizeEvent(e)

    def scroll_bar_adjust(self):
        sb = self.verticalScrollBar()
        h = self.height()
        hidden_n = 0
        for i in range(self.count()):
            hidden_n += self.item(i).isHidden()

        n = self.count() - hidden_n
        dh = self.itemHeight
        height = dh * n
        over = height - h
        if over > 0:
            sb.setMaximum(over + dh)
        else:
            sb.setMaximum(0)

    def remove_btn(self, ListWidgetItem : QListWidgetItem):
        if self.delete_parallel_animation.state() == QAbstractAnimation.State.Running: # If running
            self.delete_parallel_animation.pause() # Pause animations

        # getting Item Widget from ListWidgetItem
        station_item = self.itemWidget(ListWidgetItem)
        row = self.row(ListWidgetItem)
        if row == self.active_row.value():
            self.active_row.setValue(-1)
        
        # creating animation
        anim = QPropertyAnimation(station_item, b"geometry")

        # estimate initial position
        x0 = station_item.pos().x()
        y0 = station_item.pos().y()
        dx = station_item.width()
        dy = station_item.height()

        # estimate final position
        x = x0 + dx / 2
        y = y0 + dy / 2

        # setting animation properties
        anim.setStartValue(QRect(x0, y0, dx, dy))
        anim.setEndValue(QRect(x, y, 0, 0))
        anim.setDuration(300) # miliseconds
        anim.setEasingCurve(QEasingCurve.OutCirc)

        # insert animation into GroupAnimation
        self.delete_parallel_animation.addAnimation(anim) # Add other animation

        # resume animation
        if self.delete_parallel_animation.state() == QAbstractAnimation.State.Paused: # If paused
            self.delete_parallel_animation.resume() # Resume animations
        else:
            self.delete_parallel_animation.start()

        # Changing properties
        del self.parent.selected_parameters[station_item.station_object.metadata['signature']]
        del self.parent.archives[station_item.station_object.metadata['signature']]

        self.deleted_items.append(row)
        self.updateExistingItems(-1)

    def reposition_animation(self):
        while self.delete_parallel_animation.animationCount() > 0:
            self.delete_parallel_animation.takeAnimation(0)
        n  = len(self.deleted_items)

        # triggering reposition animation
        for i in range(max(self.deleted_items) + 1, self.existing_items + n):
            station_item = self.itemWidget(self.item(i))
            x = station_item.pos().x()
            y = station_item.pos().y()
            dx = station_item.width()
            dy = station_item.height()

            # Creating animation
            anim = QPropertyAnimation(station_item, b'geometry')
            anim.setStartValue(QRect(x, y, dx, dy))
            anim.setEndValue(QRect(x, y - (dy + 5), dx, dy))
            anim.setDuration(300) # em milisegundos
            anim.setEasingCurve(QEasingCurve.OutCirc)
            self.reposition_parallel_animation.addAnimation(anim)
        
        self.reposition_parallel_animation.start()
        
    def delete_list_widget(self):
        while self.reposition_parallel_animation.animationCount() > 0:
            self.reposition_parallel_animation.takeAnimation(0)

        # Removing ListWidgetItem from listWidget
        for row in self.deleted_items:
            ListWidgetItem = self.takeItem(row)
            self.removeItemWidget(ListWidgetItem)

            # Deleting ListWidgetItem
            del ListWidgetItem
        
        # cleaning
        self.deleted_items = []
        gc.collect() # Junk collector
        
