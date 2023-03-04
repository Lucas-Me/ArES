import os
import matplotlib as mpl
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from matplotlib.backends.qt_compat import (
    QtWidgets, __version__,
    _enum,  _getSaveFileName
)

class NavigationToolbar(NavigationToolbar2QT):

    def __init__(self, canvas, parent):
        # only display the buttons we need
        NavigationToolbar2QT.toolitems = (
            ('Home', 'Reiniciar visão original', 'home', 'home'),
            ('Back', 'Voltar a operação anterior', 'back', 'back'),
            ('Forward', 'Avançar para a operação seguinte', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Navegue com o clique esquerdo, dê zoom com o direito.', 'move', 'pan'),
            ('Zoom', 'Dê zoom para o retangulo', 'zoom_to_rect', 'zoom'),
            # ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'), (None, None, None, None),
            ('Save', 'Salvar a figura', 'filesave', 'save_figure')
        )
        super().__init__(canvas, parent)

    # sobrescreve a função "save_figure"
    def save_figure(self, *args):
        filetypes = self.canvas.get_supported_filetypes_grouped()
        sorted_filetypes = sorted(filetypes.items())
        default_filetype = self.canvas.get_default_filetype()

        startpath = os.path.expanduser(mpl.rcParams['savefig.directory'])
        start = os.path.join(startpath, self.canvas.get_default_filename())
        filters = []
        selectedFilter = None
        for name, exts in sorted_filetypes:
            exts_list = " ".join(['*.%s' % ext for ext in exts])
            filter_ = '%s (%s)' % (name, exts_list)
            if default_filetype in exts:
                selectedFilter = filter_
            filters.append(filter_)
        filters = ';;'.join(filters)

        fname, filter_ = _getSaveFileName(
            self.canvas.parent(), "Choose a filename to save to", start,
            filters, selectedFilter)
        if fname:
            # Save dir for next time, unless empty str (i.e., use cwd).
            if startpath != "":
                mpl.rcParams['savefig.directory'] = os.path.dirname(fname)
            try:
                self.canvas.figure.savefig(fname, dpi = 300, bbox_inches="tight")
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self, "Erro ao salvar o arquivo", str(e),
                    _enum("QtWidgets.QMessageBox.StandardButton").Ok,
                    _enum("QtWidgets.QMessageBox.StandardButton").NoButton)
