import inspect, sys

import matplotlib
matplotlib.use('Qt4Agg')

from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

import traits.api as traits
import traitsui.api as traitsui
from collections import OrderedDict

from matplotlib.pyplot import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT

from traitsui.qt4.editor import Editor
from traitsui.qt4.basic_editor_factory import BasicEditorFactory

from PyQt4 import QtGui

import threading

class _MPLFigureEditor(Editor):

    scrollable  = True

    def init(self, parent):
        self.control = self._create_canvas(parent)
        self.set_tooltip()

    def update_editor(self):
        pass

    def _create_canvas(self, parent):
        """ Create the MPL canvas. """
        self._widget = QtGui.QWidget()
        self._mpl_control = FigureCanvas(self.value)
        self._toolbar = NavigationToolbar2QT(self._mpl_control, self._widget) 
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._toolbar)
        layout.addWidget(self._mpl_control)
        self._widget.setLayout(layout)

        return self._widget

class MPLFigureEditor(BasicEditorFactory):

    klass = _MPLFigureEditor


class FuncWorker(threading.Thread):
    def __init__(self, orig_func, finish_func, fig, *args, **kwargs):
        threading.Thread.__init__(self)
        self.func = orig_func
        self.fig = fig
        self.finish_func = finish_func
        self.args = args
        self.kwargs = kwargs
        
    def run(self):
        self.func(self.fig, *self.args, **self.kwargs)
        self.finish_func()


def interact(func):
    
    Options = build_options_type(func)

    class QuickvisGUI(traits.HasTraits):
        
        figure = traits.Instance(Figure, ())
        apply = traits.Button
        options = traits.Instance(Options, ())
        options_changed = traits.Bool(True)
        running = traits.Bool(False)
        
        view = traitsui.View(
                   traitsui.Tabbed(
                       traitsui.Group(
                            traitsui.Item(
                                'options',
                                style='custom',
                                show_label=False,
                                enabled_when='not running'),
                            traitsui.Group(
                                traitsui.Spring(),
                                traitsui.Item(
                                    'apply',
                                    show_label=False,
                                    enabled_when='options_changed'),
                                orientation='horizontal',
                                dock='tab'),
                           label='options',
                           dock='tab'),
                       traitsui.Item(
                           'figure', 
                            editor=MPLFigureEditor(),
                            show_label=False)),
                   dock='tab',
                   width=800,
                   height=600,
                   resizable=True)
        
        @traits.on_trait_change('options.+')
        def _on_options_changed(self):
            self.options_changed = True
        
        @traits.on_trait_change('apply')
        def redraw(self):
            if self.running:
                return 
            
            self.options_changed = False
            self.figure.clear()
            self.running = True
            
            def finish_func():
                self.running = False
                self.figure.canvas.draw()
                
            self.worker = FuncWorker(func, finish_func, self.figure, 
                                     **self.options.get())
            self.worker.start()
    
    class NewFunc(object):
        def __init__(self):
            self.func = func
            
        def __call__(self, *args, **kwargs):
            self.func(*args, **kwargs)
            
        def show_gui(self):
            window = QuickvisGUI()
            window.configure_traits()
            window.redraw()
    
    return NewFunc()


def build_options_type(func):
    args, varargs, keywords, defaults = inspect.getargspec(func)
    if varargs is not None or keywords is not None:
        raise ValueError("Illegal arguments")
    
    single_args = args[:len(args) - len(defaults)]
    default_args = args[len(args) - len(defaults):]
    
    arg_defaults = OrderedDict()
    
    for name, default in zip(default_args, defaults):
        if not isinstance(default, traits.TraitType):
            raise ValueError("Illegal arguments, not a Trait: " + name)
        arg_defaults[name] = default
    
    if len(single_args) != 1:
        raise ValueError("Illegal arguments")
    
    if 'view' in arg_defaults:
        raise ValueError()
    
    arg_defaults['view'] = traitsui.View(*arg_defaults.keys())
    
    return traits.MetaHasTraits("Form", (traits.HasTraits,), arg_defaults)


def beispiel():
    @interact
    def func(fig, num=traits.Enum("Faktor", "b"), num2=traits.Bool()):
        import numpy as np
        ax = fig.add_subplot(111)
        ax.plot(np.linspace(0, 1), a * np.linspace(0, 1)**2)
    
    func.show_gui()
    
if __name__ == '__main__':
    beispiel()
    