import inspect, sys
import guidata
import guidata.dataset.dataitems as di
import guidata.dataset.datatypes as dt
from guidata.dataset.qtwidgets import DataSetEditGroupBox
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.pyplot import Figure
from PyQt4 import QtGui, QtCore

class Interact(QtCore.QObject):
    def __init__(self, func):
        QtCore.QObject.__init__(self)
        self._func = func
        
        class Form(dt.DataSet):
            pass
        
        self._form = Form
        self._process_args()
        self._figure = Figure()
        self._widget = None
        
        self._app = guidata.qapplication()
    
    def _process_args(self):
        args, varargs, keywords, defaults = inspect.getargspec(self._func)
        if varargs is not None or keywords is not None:
            raise ValueError("Illegal arguments")
        
        single_args = args[:len(args) - len(defaults)]
        default_args = args[len(args) - len(defaults):]
        
        for i, name_default in enumerate(zip(default_args, defaults)):
            name, default = name_default
            if not isinstance(default, di.DataItem):
                raise ValueError("Illegal arguments, not a DataItem: " + name)
            self._form._items.append(default)
            self._form._items[-1].set_name(name)
            self._form._items[-1]._order = i + 1
        
        if len(single_args) > 1:
            raise ValueError("Illegal arguments")
    
    def edit_data(self):
        self._form.edit()
        return self._form
    
    def _get_qtwidget(self, parent=None):
        self._widget = DataSetEditGroupBox(None, self._form)
        self._widget.setParent(parent)
        return self._widget
    
    def show_gui(self):
        main_window = ApplicationWindow(self)
        main_window.show()
        self._app.exec_()
        
    def _apply_func(self):
        assert self._widget is not None
        args = {}
        for widget in self._widget.edit.widgets:
            args[widget.item.item._name] = widget.item.get()
        try:
            self._func(self._figure, **args)
            self.emit(QtCore.SIGNAL("figure_changed()"))
        except Exception as e:
            import traceback
            traceback.print_exc()
            QtGui.QMessageBox.warning(None, type(e).__name__, e.message)
            
        
        
    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)


class MplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, figure=None):

        FigureCanvas.__init__(self, figure)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self, interact):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")
        
        data_widget = interact._get_qtwidget(parent=self)
        mpl_widget = MplCanvas(parent=self, figure=interact._figure)
        
        l = QtGui.QVBoxLayout()
        l.addWidget(data_widget)
        l.addStretch()
        
        data_widget_top = QtGui.QWidget()
        data_widget_top.setLayout(l)
        
        data_widget_dock = QtGui.QDockWidget()
        data_widget_dock.setWidget(data_widget_top)
        
        toolbar = NavigationToolbar(mpl_widget, self)
        
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, data_widget_dock)
        self.addToolBar(QtCore.Qt.TopToolBarArea, toolbar)
        
        self.connect(data_widget, QtCore.SIGNAL("apply_button_clicked()"),
                     interact._apply_func)
        self.connect(interact, QtCore.SIGNAL("figure_changed()"),
                     mpl_widget.draw)

        self.setCentralWidget(mpl_widget)


    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

def beispiel():
    @Interact
    def func(fig, a=di.ChoiceItem("Faktor", ["a", "b"])):
        import numpy as np
        ax = fig.add_subplot(111)
        ax.plot(np.linspace(0, 1), a * np.linspace(0, 1)**2)
    
    func.show_gui()
    