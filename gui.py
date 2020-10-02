"""

    Divide & Conquer
    WSU CPTS 451
    Spring 2020
    Milestone 2

"""

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qt_creator_file = "milestone2App.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)


class Milestone2(QMainWindow):
    def __init__(self):
        super(Milestone2, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_state_list()
        self.ui.stateList.currentTextChanged.connect(self.state_changed)
        self.ui.cityList.itemSelectionChanged.connect(self.city_changed)
        self.ui.zipList.itemSelectionChanged.connect(self.zip_changed)
        self.ui.zipList.itemSelectionChanged.connect(self.get_businesses)
        self.ui.zipList.itemSelectionChanged.connect(self.zipcode_stat)

    def execute_query(self, query):
        try:
            connection = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='cpts451'")
        except:
            print("Unable to connect to the database.")

        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        result = cur.fetchall()
        connection.close()
        return result

    def load_state_list(self):
        self.ui.stateList.clear()
        sql_command = "SELECT distinct state_name FROM business ORDER BY state_name;"
        print(sql_command)
        try:
            results = self.execute_query(sql_command)
            for row in results:
                self.ui.stateList.addItem(row[0])  # adding value to the combo box
        except:
            print("Query failed.")

        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def state_changed(self):
        self.ui.cityList.clear()
        state = self.ui.stateList.currentText()
        if self.ui.stateList.currentIndex() >= 0:
            sql_command = "SELECT distinct city FROM business WHERE state_name = '" + state + "' ORDER BY city;"
            print(sql_command)
            try:
                results = self.execute_query(sql_command)
                print(results)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query failed - state_changed().")

    def city_changed(self):
        self.ui.zipList.clear()
        state = self.ui.stateList.currentText()
        city = self.ui.cityList.selectedItems()[0].text()

        if  (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            sql_command = "SELECT distinct zip_code FROM business WHERE state_name = '"+state+"' AND city = '"+ city +"';"
            print(sql_command)
            try:
                results = self.execute_query(sql_command)
                print(results)
                for row in results:
                    item = str(row[0])
                    self.ui.zipList.addItem(item)
            except:
                print("Query failed - city_changed().")

    def zip_changed(self):
        self.ui.categoryList.clear()
        zipcode = self.ui.zipList.selectedItems()[0].text()

        if len(self.ui.zipList.selectedItems()) > 0:
            sql_command = "SELECT distinct category_type FROM hascategory, business " \
                          "WHERE zip_code = '" +zipcode+ "' AND hascategory.business_id = business.business_id;"
            print(sql_command)
            try:
                results = self.execute_query(sql_command)
                print(results)
                for row in results:
                    self.ui.categoryList.addItem(row[0])
            except:
                print("Query failed - zip_changed().")

    def zipcode_stat(self):
        self.ui.numBusinesses.clear()
        self.ui.topCategory.clear()
        zipcode = self.ui.zipList.selectedItems()[0].text()

        if len(self.ui.zipList.selectedItems()) > 0:
            sql_command1 = "SELECT count(*) FROM business WHERE zip_code = '" +zipcode+ "'"
            print(sql_command1)
            sql_command2 = "SELECT count(*) as num_business, category_type FROM hascategory, business " \
                           "WHERE zip_code = '" + zipcode + "' AND hascategory.business_id = business.business_id " \
                                                            "GROUP BY category_type ORDER BY num_business DESC;"
            print(sql_command2)
            try:
                results1 = self.execute_query(sql_command1)
                print(results1)
                self.ui.numBusinesses.addItem(str(results1[0][0]))
            except:
                print("Query failed - zipcode_stat1().")

            try:
                results2 = self.execute_query(sql_command2)
                print(results2)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.topCategory.horizontalHeader().setStyleSheet(style)
                self.ui.topCategory.setColumnCount(len(results2[0]))
                self.ui.topCategory.setRowCount(len(results2))
                self.ui.topCategory.setHorizontalHeaderLabels(["#of Business","Category"])
                self.ui.topCategory.resizeColumnsToContents()
                self.ui.topCategory.setColumnWidth(0, 150)
                self.ui.topCategory.setColumnWidth(1, 300)

                current_row_count = 0

                for row in results2:
                    for col_count in range(0, len(results2[0])):
                        self.ui.topCategory.setItem(current_row_count, col_count, QTableWidgetItem(str(row[col_count])))
                    current_row_count += 1
            except:
                print("Query failed - zipcode_stat2().")

    def get_businesses(self):
        if (self.ui.stateList.currentIndex() >=0) and (len(self.ui.cityList.selectedItems()) > 0) and (len(self.ui.zipList.selectedItems()) >0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.zipList.selectedItems()[0].text()

            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)

            sql_command = "SELECT business_name, city, business_avg_star, num_of_checkins, num_of_tips FROM business " \
                          "WHERE state_name = '" + state + "' AND city = '" + city + "' AND zip_code = " + zipcode + \
                          " ORDER BY business_name;"
            print(sql_command)
            try:
                results = self.execute_query(sql_command)
                print(results)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(["Business Name", "City", "Stars", "# of Checkins", "# of Tips"])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 350)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 30)
                self.ui.businessTable.setColumnWidth(3, 150)
                self.ui.businessTable.setColumnWidth(4, 150)

                current_row_count = 0

                for row in results:
                    for col_count in range(0, len(results[0])):
                        self.ui.businessTable.setItem(current_row_count, col_count, QTableWidgetItem(str(row[col_count])))
                    current_row_count += 1
            except:
                print("Query failed - get_businesses().")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Milestone2()
    window.show()
    sys.exit(app.exec_())
