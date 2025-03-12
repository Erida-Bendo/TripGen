import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.interpolate import interp1d
import numpy as np

class GraphWindow(QMainWindow):
    def __init__(self, graphData):
        super().__init__()
        self.graphData = graphData
        self.setWindowTitle('Hourly Graphs')
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        self.canvas = FigureCanvas(plt.Figure())
        self.setCentralWidget(self.canvas)
        self.plot_graph()

    def plot_graph(self):
        if len(self.graphData.columns) == 2:
            ax = self.canvas.figure.add_subplot(111)
            
            # Original data
            x = np.arange(len(self.graphData))
            y1 = self.graphData.iloc[:, 0]
            y2 = self.graphData.iloc[:, 1]
            
            # Interpolation
            x_new = np.linspace(x.min(), x.max(), 300)
            f1 = interp1d(x, y1, kind='cubic')
            f2 = interp1d(x, y2, kind='cubic')
            
            y1_smooth = f1(x_new)
            y2_smooth = f2(x_new)
            
            # Plot with enhancements
            ax.plot(x_new, y1_smooth, label='Quellverkehr', linestyle='--', color='red')
            ax.plot(x_new, y2_smooth, label='Zielverkehr', linestyle='--', color='grey')
            
            ax.legend(loc='best', fontsize=12)
            ax.set_title('Ganglinien', fontsize=16)
            ax.set_xlabel('Stunde', fontsize=14)
            ax.set_ylabel('Verkehr', fontsize=14)
            ax.grid(True)
            
            self.canvas.draw()
        else:
            ax = self.canvas.figure.add_subplot(111)
            # Extract data for all columns
            x = np.arange(len(self.graphData))

            # Categories for legend
            categories = ["Besucher", "Beschäftigte", "Wirtschaft"]
            colors = ['blue', 'green', 'orange']  # One color per category

            # Interpolation
            x_new = np.linspace(x.min(), x.max(), 300)

            # Plot each category (combining Quellverkehr and Zielverkehr)
            for i, category in enumerate(categories):
                # Get the column indices for this category
                quell_idx = i * 2    # 0, 2, 4
                ziel_idx = i * 2 + 1 # 1, 3, 5
                
                # Get data for both columns
                y_quell = self.graphData.iloc[:, quell_idx]
                y_ziel = self.graphData.iloc[:, ziel_idx]
                
                # Interpolate both columns
                f_quell = interp1d(x, y_quell, kind='cubic')
                f_ziel = interp1d(x, y_ziel, kind='cubic')
                
                y_quell_smooth = f_quell(x_new)
                y_ziel_smooth = f_ziel(x_new)
                
                # Plot both Quellverkehr and Zielverkehr with the same color
                # Use solid line for Quellverkehr
                ax.plot(x_new, y_quell_smooth, color=colors[i], linestyle='-')
                
                # Use dashed line for Zielverkehr
                ax.plot(x_new, y_ziel_smooth, color=colors[i], linestyle='-')
                
                # Add a single legend entry for this category
                # We're adding this as a separate line that won't be drawn
                ax.plot([], [], color=colors[i], label=category)

            # Enhance the plot
            ax.legend(loc='best', fontsize=12)
            ax.set_title('Ganglinien', fontsize=16)
            ax.set_xlabel('Stunde', fontsize=14)
            ax.set_ylabel('Verkehr', fontsize=14)
            ax.grid(True)

            self.canvas.draw()