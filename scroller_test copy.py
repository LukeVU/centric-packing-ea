import wx
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt

class MyFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Scrollable Plot', size=(800, 600))
        self.panel = wx.Panel(self)
        self.init_data()
        self.init_plot()
        self.canvas = FigureCanvasWxAgg(self.panel, -1, self.fig)

        self.scroll_range = self.canvas.GetSize()[0]
        self.canvas.SetScrollbar(wx.HORIZONTAL, 0, 400, self.scroll_range)

    def init_data(self):
        self.fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(20, 20))

        for i in range(3):
            for j in range(3):
                axs[i, j].plot(np.random.randn(100), label=f"subplot({i+1}, {j+1})")
                axs[i, j].legend()

        plt.tight_layout()

    def init_plot(self):
        self.fig = Figure(None)
        self.ax = self.fig.add_subplot(111)

    def draw_plot(self):
        self.ax.clear()
        self.ax.plot(self.data, "b")
        self.canvas.draw()

class MyApp(wx.App):
    def __init__(self):
        app = MyApp()
        app.MainLoop()

    def OnInit(self):
        frame = MyFrame(None, -1)
        frame.Show(True)
        frame.draw_plot()
        self.SetTopWindow(frame)
        return True