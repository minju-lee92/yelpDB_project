"""

    Divide & Conquer
    WSU CPTS 451
    Spring 2020
    Milestone 1-3

"""


import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qt_creator_file = "milestone1-3.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)


class Milestone1(QMainWindow):
    def __init__(self):
        super(Milestone1, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_state_list()
        self.ui.state_list.currentTextChanged.connect(self.state_changed)
        self.ui.city_list.itemSelectionChanged.connect(self.city_changed)
        self.ui.b_name.textChanged.connect(self.get_business_names)
        self.ui.businesses.itemSelectionChanged.connect(self.display_business_city)

    def execute_query(self, query):
        try:
            connection = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='cpts451'")
        except:
            print("Unable to connect to the database.")

        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        result = cur.fetchall()
        connection.close()
        return result

    def load_state_list(self):
        self.ui.state_list.clear()
        sql_command = "SELECT distinct state FROM business ORDER BY state;"

        try:
            results = self.execute_query(sql_command)
            for row in results:
                self.ui.state_list.addItem(row[0])
        except:
            print("Query failed.")

        self.ui.state_list.setCurrentIndex(-1)
        self.ui.state_list.clearEditText()

    def state_changed(self):
        self.ui.city_list.clear()
        state = self.ui.state_list.currentText()

        if self.ui.state_list.currentIndex() >= 0:
            sql_command = "SELECT distinct city FROM business WHERE state = '" + state + "' ORDER BY city;"
            try:
                results = self.execute_query(sql_command)
                for row in results:
                    self.ui.city_list.addItem(row[0])
            except:
                print("Query failed - state_changed().")

            for i in reversed(range(self.ui.business_table.rowCount())):
                self.ui.business_table.removeRow(i)

            sql_command = "SELECT name, city, state FROM business WHERE state = '" + state + "' ORDER BY name"
            try:
                results = self.execute_query(sql_command)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.business_table.horizontalHeader().setStyleSheet(style)
                self.ui.business_table.setColumnCount(len(results[0]))
                self.ui.business_table.setRowCount(len(results))
                self.ui.business_table.setHorizontalHeaderLabels(["Business Name", "City", "State"])
                self.ui.business_table.resizeColumnsToContents()
                self.ui.business_table.setColumnWidth(0, 300)
                self.ui.business_table.setColumnWidth(1, 100)
                self.ui.business_table.setColumnWidth(2, 50)
                current_row_count = 0

                for row in results:
                    for col_count in range(0, len(results[0])):
                        self.ui.business_table.setItem(current_row_count, col_count, QTableWidgetItem(row[col_count]))
                    current_row_count += 1
            except:
                print("Query failed - state_changed().")

    def city_changed(self):
        if self.ui.state_list.currentIndex() >= 0 and len(self.ui.city_list.selectedItems()) > 0:
            state = self.ui.state_list.currentText()
            city = self.ui.city_list.selectedItems()[0].text()
            sql_command = "SELECT name, city, state FROM business WHERE state = '" + state + "' AND city = '" + city + "' ORDER BY name;"
            results = self.execute_query(sql_command)
            try:
                results = self.execute_query(sql_command)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.business_table.horizontalHeader().setStyleSheet(style)
                self.ui.business_table.setColumnCount(len(results[0]))
                self.ui.business_table.setRowCount(len(results))
                self.ui.business_table.setHorizontalHeaderLabels(["Business Name", "City", "State"])
                self.ui.business_table.resizeColumnsToContents()
                self.ui.business_table.setColumnWidth(0, 300)
                self.ui.business_table.setColumnWidth(1, 100)
                self.ui.business_table.setColumnWidth(2, 50)
                current_row_count = 0
                for row in results:
                    for col_count in range(0, len(results[0])):
                        self.ui.business_table.setItem(current_row_count, col_count, QTableWidgetItem(row[col_count]))
                    current_row_count += 1
            except:
                print("Query failed - city_changed().")

    def get_business_names(self):
        self.ui.businesses.clear()
        business_name = self.ui.b_name.text()
        sql_command = "SELECT name FROM business WHERE name LIKE '%" + business_name + "%' ORDER BY name"
        try:
            results = self.execute_query(sql_command)
            for row in results:
                self.ui.businesses.addItem(row[0])
        except:
            print("Query failed - get_business_names().")

    def display_business_city(self):
        business_name = self.ui.businesses.selectedItems()[0].text()
        sql_command = "SELECT city FROM business WHERE name = '" + business_name + "';"
        try:
            results = self.execute_query(sql_command)
            self.ui.b_city.setText(results[0][0])
        except:
            print("Query failed - display_business_city().")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Milestone1()
    window.show()
    sys.exit(app.exec_())
