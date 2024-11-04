import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QCheckBox, QTextEdit, QHeaderView, QPushButton, QHBoxLayout, QComboBox, QFileDialog
from PyQt6.QtGui import QColor, QBrush, QFont
import pandas as pd

HIGHLIGHT_COLOR = QColor(255, 255, 0)
NORMAL_TEXT_COLOR = QColor(0, 0, 0)
NORMAL_BG_COLOR = QColor(255, 255, 255)

class SearchInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = None  # DataFrame to store the loaded Excel data
        self.selected_items = set()
        self.logic = "AND"  # Default logic
        self.init_ui()
        self.load_excel_file()

    def load_excel_file(self):
        try:
            if self.data is None:  # Check if data is not already loaded
                self.data = pd.read_excel("data/Literaturrecherche.xlsx", sheet_name="data") # Change this to your excel file or load it via the button
                self.init_table()
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            self.data = None

    def init_ui(self):
        self.setWindowTitle("Search Query Generator")
        self.resize(800, 600)  # Set the initial size of the window (width, height)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)  # Two columns: Checkbox and Query

        layout.addWidget(self.table_widget)

        # Create a QHBoxLayout for the buttons and logic selection
        button_layout = QHBoxLayout()

        # Add the Load Excel button
        load_excel_button = QPushButton("Load Excel")
        load_excel_button.clicked.connect(self.open_file_dialog)
        button_layout.addWidget(load_excel_button)

        # Add the Copy button
        copy_button = QPushButton("Copy")
        copy_button.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(copy_button)

        # Add the Clear All button
        clear_all_button = QPushButton("Clear All")
        clear_all_button.clicked.connect(self.clear_all_checkboxes)
        button_layout.addWidget(clear_all_button)

        # Add the Randomize button
        randomize_button = QPushButton("Randomize")
        randomize_button.clicked.connect(self.randomize_checkboxes)
        button_layout.addWidget(randomize_button)

        # Add the logic selection ComboBox
        self.logic_combobox = QComboBox()
        self.logic_combobox.addItems(["AND", "OR"])
        self.logic_combobox.currentIndexChanged.connect(self.update_query)
        button_layout.addWidget(self.logic_combobox)

        layout.addLayout(button_layout)

        # Add the QTextEdit
        self.query_result_text_edit = QTextEdit()
        # Set maximum height for the QTextEdit widget
        self.query_result_text_edit.setMaximumHeight(50)
        layout.addWidget(self.query_result_text_edit)

        self.central_widget.setLayout(layout)

        self.show()

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_name:
            try:
                self.data = pd.read_excel(file_name, sheet_name="data")
                self.init_table()
            except Exception as e:
                print(f"Error loading Excel file: {e}")
                self.data = None

    def init_table(self):
        if self.data is not None:
            # Clear any existing data in the table
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)

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
            self.table_widget.setHorizontalHeaderLabels(["Query?", "Query"])
            self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

    def update_query(self):
        self.logic = self.logic_combobox.currentText()
        self.selected_items = set()
        for i in range(self.table_widget.rowCount()):
            checkbox = self.table_widget.cellWidget(i, 0)
            query_item = self.table_widget.item(i, 1)
            if checkbox.isChecked():
                self.selected_items.add(query_item.text())
                query_item.setBackground(HIGHLIGHT_COLOR)
                query_item.setForeground(QBrush(NORMAL_TEXT_COLOR))  # Set text color to black for better contrast
                font = QFont()
                font.setBold(True)
                query_item.setFont(font)
            else:
                query_item.setBackground(NORMAL_BG_COLOR)  # Reset background color
                query_item.setForeground(QBrush(NORMAL_TEXT_COLOR))  # Reset text color
                font = QFont()
                font.setBold(False)
                query_item.setFont(font)

        if self.logic == "AND":
            query = " AND ".join(self.selected_items)
        else:
            query = " OR ".join(self.selected_items)
        self.query_result_text_edit.setText(query)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.query_result_text_edit.toPlainText())

    def clear_all_checkboxes(self):
        for i in range(self.table_widget.rowCount()):
            checkbox = self.table_widget.cellWidget(i, 0)
            checkbox.setChecked(False)
            query_item = self.table_widget.item(i, 1)
            query_item.setBackground(NORMAL_BG_COLOR)  # Reset background color
            query_item.setForeground(QBrush(NORMAL_TEXT_COLOR))  # Reset text color
            font = QFont()
            font.setBold(False)
            query_item.setFont(font)

    def randomize_checkboxes(self):
        num_to_tick = random.randint(1, 4)
        rows = random.sample(range(self.table_widget.rowCount()), num_to_tick)
        for i in range(self.table_widget.rowCount()):
            checkbox = self.table_widget.cellWidget(i, 0)
            checkbox.setChecked(i in rows)
            query_item = self.table_widget.item(i, 1)
            if i in rows:
                query_item.setBackground(HIGHLIGHT_COLOR)
                query_item.setForeground(QBrush(NORMAL_TEXT_COLOR))  # Set text color to black for better contrast
                font = QFont()
                font.setBold(True)
                query_item.setFont(font)
            else:
                query_item.setBackground(NORMAL_BG_COLOR)  # Reset background color
                query_item.setForeground(QBrush(NORMAL_TEXT_COLOR))  # Reset text color
                font = QFont()
                font.setBold(False)
                query_item.setFont(font)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = SearchInterface()
    sys.exit(app.exec_())
