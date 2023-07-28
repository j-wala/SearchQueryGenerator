import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QHeaderView, QLineEdit, QLabel, QPushButton
from PyQt5.QtCore import Qt, QAbstractTableModel

class DataFrameModel(QAbstractTableModel):
    def __init__(self, dataframe):
        super().__init__()
        self._dataframe = dataframe

    def rowCount(self, parent=None):
        return self._dataframe.shape[0]

    def columnCount(self, parent=None):
        return self._dataframe.shape[1]

    def data(self, index, role):
        if role == Qt.CheckStateRole and index.column() == 0:
            return Qt.Checked if self._dataframe.iloc[index.row(), 0] else Qt.Unchecked
        elif role == Qt.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])
            if orientation == Qt.Vertical:
                return str(self._dataframe.index[section])
        return None

    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        return Qt.ItemIsEnabled

    def setData(self, index, value, role):
        if role == Qt.CheckStateRole and index.column() == 0:
            self._dataframe.iloc[index.row(), 0] = value == Qt.Checked
            return True
        return False

class DataFrameViewer(QMainWindow):
    def __init__(self, dataframe):
        super().__init__()
        self.df_model = DataFrameModel(dataframe)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.table_view = QTableView(self)
        self.table_view.setModel(self.df_model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        layout.addWidget(self.table_view)

        self.search_label = QLabel("Search Query:", self)
        layout.addWidget(self.search_label)

        self.search_textfield = QLineEdit(self)
        self.search_textfield.setPlaceholderText("Enter search query based on selected rows")
        layout.addWidget(self.search_textfield)

        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self.update_search_textfield)
        layout.addWidget(self.search_button)

    def update_search_textfield(self):
        selected_rows = [index for index in range(len(self.df_model._dataframe)) if self.df_model._dataframe.iloc[index, 0]]
        selected_data = self.df_model._dataframe.iloc[selected_rows]
        search_query = " OR ".join(selected_data['Query'])  # Replace 'Column_Name' with the actual column name from your DataFrame
        self.search_textfield.setText(search_query)

if __name__ == "__main__":
    # Replace 'data' with your actual DataFrame
    # data = {
    #     'Checkbox_Column': [False, False, False, False],
    #     'Column_Name': ['Data 1', 'Data 2', 'Data 3', 'Data 4']
    # }
    # df = pd.DataFrame(data)
    df = pd.read_csv('data/data.csv', delimiter=";")
    app = QApplication(sys.argv)
    window = DataFrameViewer(df)
    window.show()
    sys.exit(app.exec_())