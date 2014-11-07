from time import sleep

from pineal.osc import Osc
from pineal.config import OSC_GUI, OSC_CORE

import sys
sys.argv = sys.argv[:1] + ['-ckivy:log_level:error']
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider as _Slider


class Slider(_Slider):
    def __init__(self, visual, variable, **kwargs):
        self.visual = visual
        self.variable = variable
        _Slider.__init__(self, **kwargs)


class Tab(TabbedPanelHeader):
    def __init__(self, **kwargs):
        TabbedPanelHeader.__init__(self, **kwargs)
        self.variables = []


class Gui(App):
    def build(self):
        self.tb= TabbedPanel()

        while self.tb.tab_list:
            self.tb.tab_list.pop(0)

        return self.tb

    def run(self):
        try:
            App.run(self)
        except KeyboardInterrupt:
            self.on_stop()

    def on_start(self):
        print 'starting pineal.gui'
        self.visuals = {}

        self.osc = Osc(OSC_GUI, OSC_CORE)
        self.osc.listen('add', self.cb_add)
        self.osc.start()

    def on_stop(self):
        self.osc.stop()

    def cb_add(self, path, tags, args, source):
        visual, var, value = args

        if visual not in self.visuals.keys():
            tab = Tab(text=visual)
            tab.content = BoxLayout(orientation='horizontal')
            self.tb.add_widget(tab)

            self.visuals[visual] = tab

        if var not in self.visuals[visual].variables:
            tab = self.visuals[visual]
            self.visuals[visual].variables.append(var)

            slider = Slider(
                visual, var,
                min=0, max=1, value=value,
                orientation='vertical', size_hint=(1, 0.9)
            )
            slider.bind(value=self.cb_slider)

            label = Label(text=var, size_hint=(1, 0.1))

            box = BoxLayout(orientation='vertical')
            box.add_widget(slider)
            box.add_widget(label)

            tab.content.add_widget(box)

    def cb_slider(self, slider, value):
        self.osc.send('/visual/'+slider.visual+'/'+slider.variable, float(value))
