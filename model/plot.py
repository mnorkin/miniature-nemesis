"""
The Plot
"""
import pyqtgraph as pg

class Plot():

  def __init__(self, title='Plot'):
    self.plot_widget = pg.plot(title=title)
    self.plot_widget.showGrid(x=True, y=True)

  def plot_dots(self, joined_data):
    x_data = [joined_data[i][0] for i in range(joined_data.__len__())]
    y_data = [joined_data[i][1] for i in range(joined_data.__len__())]

    self.plot_widget.plot(x_data, y_data, pen='r', symbol='o')

  def plot_continue(self, joined_data, color='m'):

    x_data = [joined_data[i][0] for i in range(joined_data.__len__())]
    y_data = [joined_data[i][1] for i in range(joined_data.__len__())]

    self.plot_widget.plot(x_data, y_data, pen=color)

  def plot_point(self, x_data, y_data, color='r'):

    self.plot_widget.plot([x_data], [y_data], pen=color, symbol='o')