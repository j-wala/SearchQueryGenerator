import sys
import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QApplication, QTableView, QCheckBox, QLineEdit, QVBoxLayout
from PyQt5.QtWidgets import QWidget

class MyModel(QAbstractTableModel):

    def __init__(self, dataframe):
        super().__init__()
        self.dataframe = dataframe

    def rowCount(self, parent=None):
        return self.dataframe.shape[0]

    def columnCount(self, parent=None):
        return self.dataframe.shape[1]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.dataframe.iloc[index.row(), index.column()]
        elif role == Qt.CheckStateRole:
            return Qt.Checked if self.dataframe.iloc[index.row(), index.column()] else Qt.Unchecked

    def setData(self, index, value, role):
        if role == Qt.CheckStateRole:
            self.dataframe.iloc[index.row(), index.column()] = value
            return True
        else:
            return False

def main():
    app = QApplication(sys.argv)
    dataframe = pd.DataFrame({"Name": ["John", "Jane", "Mary"], "Age": [30, 25, 40]})
    model = MyModel(dataframe)
    view = QTableView()
    view.setModel(model)

    checkboxes = []
    for i in range(model.rowCount()):
        checkbox = QCheckBox()
        checkbox.setCheckable(True)
        checkbox.setChecked(False)
        checkboxes.append(checkbox)
        # view.setCellWidget(i, 0, checkbox)

    query_field = QLineEdit()

    def update_query():
        query = ""
        for checkbox in checkboxes:
            if checkbox.isChecked():
                query += checkbox.text() + " "
        query_field.setText(query)

    def checkbox_state_changed(checkbox):
        update_query()

    for checkbox in checkboxes:
        checkbox.stateChanged.connect(checkbox_state_changed)

    layout = QVBoxLayout()
    layout.addWidget(view)
    layout.addWidget(query_field)

    window = QWidget()
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()