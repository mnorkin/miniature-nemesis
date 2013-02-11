import pyqtgraph as pg

class Plot():

  def __init__(self, title='Plot'):
    self.plot_widget = pg.plot(title=title)
    self.plot_widget.showGrid(x=True, y=True)

  def plot_dots(self, joined_data):
    x_data = [joined_data[i][0] for i in range(joined_data.__len__())]
    y_data = [joined_data[i][1] for i in range(joined_data.__len__())]

    self.plot_widget.plot(x_data, y_data, pen=None, symbol='o')

  def plot_continue(self, joined_data, color='r'):

    x_data = [joined_data[i][0] for i in range(joined_data.__len__())]
    y_data = [joined_data[i][1] for i in range(joined_data.__len__())]

    self.plot_widget.plot(x_data, y_data, pen=color)
