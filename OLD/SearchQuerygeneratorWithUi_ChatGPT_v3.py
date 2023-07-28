import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QCheckBox, QTextEdit, QSizePolicy, QHeaderView, QPushButton, QHBoxLayout
from PyQt5.QtGui import QClipboard


class SearchInterface(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data[["Query"]]
        self.selected_items = set()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Search Query Generator")
        self.resize(800, 600)  # Set the initial size of the window (width, height)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)  # Two columns: Checkbox and Query

        for i, row in self.data.iterrows():
            self.table_widget.insertRow(i)

            # Checkbox column
            checkbox = QCheckBox()
            checkbox.setChecked(False)
            checkbox.stateChanged.connect(self.update_query)
            self.table_widget.setCellWidget(i, 0, checkbox)

            # Query column
            query_item = QTableWidgetItem(str(row["Query"]))
            self.table_widget.setItem(i, 1, query_item)

        # Set header labels and resize mode
        self.table_widget.setHorizontalHeaderLabels(["", "Query"])
        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        layout.addWidget(self.table_widget)

        # Create a QHBoxLayout for the button and the QTextEdit
        button_text_layout = QHBoxLayout()

        # Add the QTextEdit
        self.query_result_text_edit = QTextEdit()
        # Set maximum height for the QTextEdit widget
        self.query_result_text_edit.setMaximumHeight(50)
        button_text_layout.addWidget(self.query_result_text_edit)

        # Add the copy button
        copy_button = QPushButton("Copy")
        copy_button.clicked.connect(self.copy_to_clipboard)
        button_text_layout.addWidget(copy_button)

        layout.addLayout(button_text_layout)

        self.central_widget.setLayout(layout)

        self.show()

    def update_query(self):
        self.selected_items = set()
        for i in range(self.table_widget.rowCount()):
            checkbox = self.table_widget.cellWidget(i, 0)
            if checkbox.isChecked():
                query_item = self.table_widget.item(i, 1).text()
                self.selected_items.add(query_item)

        query = " AND ".join(self.selected_items)
        self.query_result_text_edit.setText(query)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.query_result_text_edit.toPlainText())


if __name__ == "__main__":
    import pandas as pd

    # Sample data, replace this with your DataFrame
    data = pd.read_excel("data/Literaturrecherche.xlsx", sheet_name="data")

    app = QApplication(sys.argv)
    window = SearchInterface(data)
    sys.exit(app.exec_())
