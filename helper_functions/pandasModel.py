from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt5.QtGui import QBrush, QColor, QFont
import pandas as pd
import numpy as np

class PandasModel(QAbstractTableModel):
    """Model to display pandas DataFrame in QTableView with sum row"""
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._update_sums()

    def _update_sums(self):
        # Calculate and store sums for each column
        self.sums = {}
        for col_idx, col_name in enumerate(self._data.columns):
            # Try to calculate sum for each column, regardless of pandas' detected type
            try:
                # Force numeric conversion of the column before summing
                numeric_col = pd.to_numeric(self._data[col_name], errors='coerce')
                self.sums[col_idx] = numeric_col.sum()
            except:
                # If column can't be summed, store None
                self.sums[col_idx] = None

    def rowCount(self, parent=QModelIndex()):
        # Add one extra row for sums
        return len(self._data) + 1

    def columnCount(self, parent=QModelIndex()):
        return len(self._data.columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
            
        # Check if this is the sum row
        if index.row() == len(self._data):
            if role == Qt.DisplayRole or role == Qt.EditRole:
                col_idx = index.column()
                
                # Show sum value if available
                if col_idx in self.sums and self.sums[col_idx] is not None:
                    sum_value = self.sums[col_idx]
                    # Format with proper precision
                    return f"{sum_value:.4f}"
                return "Sum"  # Fallback if sum calculation failed
            elif role == Qt.BackgroundRole:
                return QBrush(QColor(230, 230, 250))  # Light lavender
            elif role == Qt.FontRole:
                font = QFont()
                font.setBold(True)
                return font
        else:
            # Regular row
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                if pd.isna(value):
                    return ""
                # Format numerical values consistently
                if isinstance(value, (int, float)):
                    col_name = self._data.columns[index.column()]
                    # Check if values in column have decimal places
                    if '.' in str(value) or any('.' in str(val) for val in self._data[col_name] if not pd.isna(val)):
                        return f"{value:.4f}"
                    return f"{int(value)}"
                return str(value)
            elif role == Qt.TextAlignmentRole:
                # Align numbers to right
                value = self._data.iloc[index.row(), index.column()]
                if isinstance(value, (int, float)):
                    return Qt.AlignRight | Qt.AlignVCenter
                
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                # For the sum row, show "Sum" in the vertical header
                if section == len(self._data):
                    return "Sum"
                return str(self._data.index[section])
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            if index.row() >= len(self._data):
                # Don't allow editing of the sum row
                return False
                
            try:
                # Try to convert to numeric if possible
                numeric_value = pd.to_numeric(value)
                self._data.iloc[index.row(), index.column()] = numeric_value
            except ValueError:
                # If not numeric, keep as string
                self._data.iloc[index.row(), index.column()] = value
                
            # Update sums
            self._update_sums()
            
            # Emit signal for the changed cell
            self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
            
            # Emit signal for the sum row cell
            sum_row_index = self.index(len(self._data), index.column())
            self.dataChanged.emit(sum_row_index, sum_row_index, [Qt.DisplayRole])
            
            return True
        return False

    def flags(self, index):
        # Make sum row non-editable
        if index.row() == len(self._data):
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable