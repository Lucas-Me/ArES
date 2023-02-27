from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt

class CustomLineCollection(LineCollection):
    
	def __init__(self, *args, **kwargs):
		self.ax = kwargs.pop("ax", plt.gca())
		super().__init__(*args, **kwargs)
		self.fig = self.ax.get_figure()
		self.lw_data = kwargs.pop("linewidths", 1)
		self.lw = 1
		self.trans = self.ax.transData.transform

		self._resize()
		self.cid = self.fig.canvas.mpl_connect('draw_event', self._resize)
		self.fig.canvas.draw()
	
	def _resize(self, event=None):
		self.ppd = 72./self.fig.dpi
		lw =  ((self.trans((self.lw_data, 1)) - self.trans((0, 0))) * self.ppd)[0]
		if lw != self.lw:
			self.set_linewidth(lw)
			self.lw = lw
			self._redraw_later()

	def _redraw_later(self):
		self.timer = self.fig.canvas.new_timer(interval=10)
		self.timer.single_shot = True
		self.timer.add_callback(lambda : self.fig.canvas.draw_idle())
		self.timer.start()