# IMPORTS
import gc


# IMPORT QT CORE
from qt_core import *

# IMPORT CUSTOM MODULES
from gui.widgets.station_list_item import StationListItem, EnterpriseHeaderItem

# IMPORT UI MODULES
from gui.ui_widgets.ui_py_station_list_view import UI_PyStationListView

class PyStationListView(QListWidget):
    itemPressed = Signal()

    def __init__(self, parent, width, scroll_width = 15, item_height = 50) -> None:
        super().__init__()

        # configuration
        self.setMinimumWidth(width)

        # Properties
        self.parent = parent
        self.item_height = item_height
        self.scroll_width = scroll_width
        self.enterprise_category = {} # key =  enterprise name, value = corresponding widget
        self.activeWidget = None
        
        # configuring widgets
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.verticalScrollBar().setSingleStep(1)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setItemAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setSortingEnabled(False)
        
        # Configuring UI
        self.ui = UI_PyStationListView()
        self.ui.setup_ui(self)

        # Signals and Slots
        self.itemClicked.connect(self.toggle_highlight)

    def organize_items(self):
        '''
        Essa funcao deve ser chamada toda vez que um objeto for adicionado ou removido
        da lista.
        '''
        pass

    def toggle_highlight(self, WidgetItem : QListWidgetItem):
        # getting item QFrame from ListWidgetItem
        item = self.itemWidget(WidgetItem)

        # Checking if it is a header
        if self.itemWidget(WidgetItem).objectName() == 'item_header':
            return None

        # Check if already selected
        if self.activeWidget != WidgetItem:
            if not self.activeWidget is None:
                self.itemWidget(self.activeWidget).change_color('#ffffff')
        
            item.change_color('#d0e6ea', highlight = True)
            self.update_active_widget(WidgetItem)

    def update_active_widget(self, widget):
        self.activeWidget = widget
        if self.activeWidget is None:
            self.parent.ui.check_box.setCheckable(False)
            self.parent.ui.check_box.setCheckState(Qt.CheckState.Unchecked)

        self.itemPressed.emit()

    def clear_selections(self):
        # clear selection count on every widget
        for i in range(self.count()):
            item = self.item(i)
            item_widget = self.itemWidget(item)
            if item_widget.objectName() == 'item_header':
                continue

            item_widget.marked.updateCount(0)

    def add_header(self, name):
        # CREATING HEADER OBJECT
        height = 30
        header = EnterpriseHeaderItem(
            label = name,
            total = 0, 
            width = self.width() - self.scroll_width,
            height= height
        )

        # CREATING LISTWIDGETITEM AND ITS PROPERTIES
        list_widget_header = QListWidgetItem()
        list_widget_header.setSizeHint(
            QSize(self.width() - self.scroll_width, height)
        )

        # SIGNALS AND SLOTS
        header.emptyHeader.connect(
            lambda: self.remove_header(list_widget_header)
            )

        # adding into list
        self.addItem(list_widget_header)
        self.setItemWidget(list_widget_header, header)
        self.enterprise_category[name] = list_widget_header

    def add_station_item(self, station_object):
        # checking if theres already an existing header
        enterprise = station_object.metadata['enterprise']
        if enterprise not in self.enterprise_category:
            self.add_header(enterprise)

        # getting the row number to insert
        header = self.enterprise_category[enterprise]
        header_item = self.itemWidget(header)
        n = header_item.count()
        row_to_insert = self.row(header) + n + 1

        # creating StationListItem 
        station_item = StationListItem(
            station_object = station_object,
            item_width = self.width() - self.scroll_width,
            item_height = self.item_height,
            )

         # Creating QListWidgetItem
        list_widget_item = QListWidgetItem()

        # Setting Size Hint to ListWidgetItem
        list_widget_item.setSizeHint(
            QSize(self.width() - self.scroll_width, self.item_height)
        )

        # ADDING ITEM TO LISTWIDGET
        self.insertItem(row_to_insert, list_widget_item)
        self.setItemWidget(list_widget_item, station_item)

        # SIGNALS AND SLOTS
        is_xls = station_item._signature[:3] == 'xls'
        if is_xls:
            station_item.ui.delete_btn.clicked.connect(
                lambda x: self.remove_item(list_widget_item)
                )
        
        # updating header count
        header_item.setCount(n + 1)

    def remove_item(self, ListWidgetItem : QListWidgetItem):
        # getting Item Widget from ListWidgetItem
        station_item = self.itemWidget(ListWidgetItem)

        # reseting active row if needed
        if ListWidgetItem == self.activeWidget:
            self.update_active_widget(None)
        
        # Changing properties
        del self.parent.selected_parameters[station_item._signature]
        del self.parent.archives[station_item._signature]

        #  header properties
        header = self.enterprise_category[station_item._enterprise]
        header_item = self.itemWidget(header)
        header_item.setCount(header_item.count() - 1)

        # removing from list
        self.removeItemWidget(ListWidgetItem)
        self.takeItem(self.row(ListWidgetItem))

        # Deleting ListWidgetItem
        del ListWidgetItem

        gc.collect() # Junk collector


    def remove_header(self, header : QListWidgetItem):
        item = self.itemWidget(header)

        # changing properties
        del self.enterprise_category[item.label]

        # removing from list
        self.removeItemWidget(header)
        self.takeItem(self.row(header))
        
        # deleting QLIstWidgetItem
        del header

    def clean_objects(self):
        '''
        This function cleans all the objects/items in the Station List View (QListWidget)
        '''
        self.clear()
        
        # resetting properties
        self.activeWidget = None
        self.enterprise_category.clear()

        # junk collector
        gc.collect()