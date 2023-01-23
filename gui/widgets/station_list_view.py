# IMPORTS
import os, gc, time

# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from gui.widgets.station_list_item import StationListItem

# IMPORT UI MODULES
from gui.ui_widgets.ui_py_station_list_view import UI_PyStationListView

class PyStationListView(QListWidget):

    def __init__(self, parent, width, scroll_width = 15, item_height = 50) -> None:
        super().__init__()

        # configuration
        self.setFixedWidth(width)

        # Properties
        self.parent = parent
        self.item_width = self.width() - scroll_width
        self.item_height = item_height
        self.scroll_width = scroll_width
        self.existing_items = 0
        self.deleted_items = []
        self.active_row = QSpinBox()
        
        # configuring widgets
        self.active_row.setRange(-1, 1000)
        self.active_row.setValue(-1)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.verticalScrollBar().setSingleStep(1)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setSelectionRectVisible(False)
        self.setItemAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setContentsMargins(0, 0, 0, 0)

        # Configuring UI
        self.ui = UI_PyStationListView()
        self.ui.setup_ui(self)

        # Signals and Slots
        self.itemClicked.connect(self.toggle_highlight)

    def toggle_highlight(self, WidgetItem : QListWidgetItem):
        active_row = self.active_row.value()
        station_item = self.itemWidget(WidgetItem)
        item_row = self.row(WidgetItem)

        # Check if already selected
        if active_row != item_row:
            if active_row >= 0:
                self.itemWidget(self.item(active_row)).change_color('#ffffff')
        
            station_item.change_color('#d0e6ea', highlight = True)
            self.active_row.setValue(item_row)

    def add_station_item(self, station_object):
        # Creating QListWidgetItem and adding it to List
        list_widget_item = QListWidgetItem(self)
        self.addItem(list_widget_item)

        # test
        is_xls = station_object.metadata['signature'][:3] == 'xls'

        # creating StationListItem 
        station_item = StationListItem(
            station_object = station_object,
            item_width = self.item_width,
            item_height = self.item_height
            )

        # Setting Size Hint to ListWidgetItem
        SizeHint = QSize(self.item_width, self.item_height)
        list_widget_item.setSizeHint(SizeHint)

        # Setting StationListItem to QListWidgetItem
        self.setItemWidget(list_widget_item, station_item)

        # SIGNALS AND SLOTS
        if is_xls:
            station_item.ui.delete_btn.clicked.connect(
                lambda x: self.remove_item(list_widget_item)
                )
        
        # update private variable
        self.updateExistingItems(1)

    def updateExistingItems(self, value):
        self.existing_items = self.existing_items + value
        
    # def resizeEvent(self, e: QResizeEvent) -> None:
    #     self.scroll_bar_adjust()
    #     return super().resizeEvent(e)

    # def scroll_bar_adjust(self):
    #     sb = self.verticalScrollBar()
    #     h = self.height()
    #     hidden_n = 0
    #     for i in range(self.count()):
    #         hidden_n += self.item(i).isHidden()

    #     n = self.count() - hidden_n
    #     dh = self.itemHeight
    #     height = dh * n
    #     over = height - h
    #     if over > 0:
    #         sb.setMaximum(over + dh)
    #     else:
    #         sb.setMaximum(0)

    def remove_item(self, ListWidgetItem : QListWidgetItem):
        # getting Item Widget from ListWidgetItem
        station_item = self.itemWidget(ListWidgetItem)
        row = self.row(ListWidgetItem)

        # reseting active row if needed
        if row == self.active_row.value():
            self.active_row.setValue(-1)
        
        # Changing properties
        del self.parent.selected_parameters[station_item._signature]
        del self.parent.archives[station_item._signature]

        self.deleted_items.append(row)
        self.updateExistingItems(-1)
        self.delete_list_widget()

    def delete_list_widget(self):
        # Removing ListWidgetItem from listWidget
        for row in self.deleted_items:
            ListWidgetItem = self.takeItem(row)
            self.removeItemWidget(ListWidgetItem)

            # Deleting ListWidgetItem
            del ListWidgetItem
        
        # cleaning
        self.deleted_items = []
        gc.collect() # Junk collector
        
