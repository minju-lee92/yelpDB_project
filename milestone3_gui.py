"""

    Divide & Conquer
    WSU CPTS 451
    Spring 2020
    Milestone 3

"""

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qt_creator_file = "milestone3.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)


class Milestone2(QMainWindow):
    def __init__(self):
        super(Milestone2, self).__init__()
        self.ui = Ui_MainWindow()

        # GUI Elements - Businesses Page
        self.ui.setupUi(self)
        self.load_state_list()
        self.ui.stateList.currentTextChanged.connect(self.state_changed)
        self.ui.cityList.itemSelectionChanged.connect(self.city_changed)
        self.ui.zipList.itemSelectionChanged.connect(self.zip_changed)
        self.ui.zipList.itemSelectionChanged.connect(self.zipcode_stat)
        self.ui.searchButton.clicked.connect(self.search_button_pressed)
        self.ui.clearButton.clicked.connect(self.clear_button_pressed)
        self.ui.refreshButton.clicked.connect(self.refresh_button_pressed)

        # GUI Elements - Users Page
        self.ui.loginUserName.textChanged.connect(self.user_login_updated)
        self.ui.loginUserIDs.itemSelectionChanged.connect(self.user_id_selected)

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
        print("")

        try:
            results = self.execute_query(sql_command)
            print(results)
            print("")

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
            print("")

            try:
                results = self.execute_query(sql_command)
                print(results)
                print("")

                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query failed - state_changed().")

    def city_changed(self):
        self.ui.zipList.clear()
        state = self.ui.stateList.currentText()
        city = self.ui.cityList.selectedItems()[0].text()

        if  (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            sql_command = "SELECT distinct zip_code FROM business WHERE state_name = '" + state + "' AND city = '" + city + "' ORDER BY zip_code;"
            print(sql_command)
            print("")

            try:
                results = self.execute_query(sql_command)
                print(results)
                print("")

                for row in results:
                    item = str(row[0])
                    self.ui.zipList.addItem(item)
            except:
                print("Query failed - city_changed().")

    def zip_changed(self):
        self.ui.categoryList.clear()
        self.ui.businessTable.clear()
        zipcode = self.ui.zipList.selectedItems()[0].text()

        if len(self.ui.zipList.selectedItems()) > 0:
            sql_command = "SELECT distinct category_type FROM hascategory, business WHERE zip_code = '" + zipcode + "' AND hascategory.business_id = business.business_id ORDER BY category_type;"
            print(sql_command)
            print("")

            try:
                results = self.execute_query(sql_command)
                print(results)
                print("")

                for row in results:
                    self.ui.categoryList.addItem(row[0])
            except:
                print("Query failed - zip_changed().")

            sql_command2 = "SELECT business_name, address, city, business_avg_star, num_of_checkins, num_of_tips FROM business WHERE zip_code = '" + zipcode + "' ORDER BY business_name;"
            print(sql_command2)
            print("")

            try:
                results2 = self.execute_query(sql_command2)
                print(results2)
                print("")

                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results2[0]))
                self.ui.businessTable.setRowCount(len(results2))
                self.ui.businessTable.setHorizontalHeaderLabels(
                    ["Business Name", "Address", "City", "Stars", "# of Checkins", "# of Tips"])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 275)
                self.ui.businessTable.setColumnWidth(1, 250)
                self.ui.businessTable.setColumnWidth(2, 120)
                self.ui.businessTable.setColumnWidth(3, 60)
                self.ui.businessTable.setColumnWidth(4, 90)
                self.ui.businessTable.setColumnWidth(5, 75)

                current_row_count = 0

                for row in results2:
                    for col_count in range(0, len(results2[0])):
                        self.ui.businessTable.setItem(current_row_count, col_count,
                                                      QTableWidgetItem(str(row[col_count])))

                    current_row_count += 1
            except:
                print("Query failed - business_table_display.")

    def zipcode_stat(self):
        self.ui.numBusinesses.clear()
        self.ui.topCategory.clear()
        zipcode = self.ui.zipList.selectedItems()[0].text()

        if len(self.ui.zipList.selectedItems()) > 0:
            sql_command1 = "SELECT count(*) FROM business WHERE zip_code = '" + zipcode + "'"
            print(sql_command1)
            print("")

            sql_command2 = "SELECT count(*) as num_business, category_type FROM hascategory, business WHERE zip_code = '" + zipcode + "' AND hascategory.business_id = business.business_id GROUP BY category_type ORDER BY num_business DESC;"
            print(sql_command2)
            print("")

            try:
                results1 = self.execute_query(sql_command1)
                print(results1)
                print("")

                self.ui.numBusinesses.addItem(str(results1[0][0]))

            except:
                print("Query failed - zipcode_stat1().")

            try:
                results2 = self.execute_query(sql_command2)
                print(results2)
                print("")

                style = "::section {""background-color: #f3f3f3; }"
                self.ui.topCategory.horizontalHeader().setStyleSheet(style)
                self.ui.topCategory.setColumnCount(len(results2[0]))
                self.ui.topCategory.setRowCount(len(results2))
                self.ui.topCategory.setHorizontalHeaderLabels(["# of Businesses", "Category"])
                self.ui.topCategory.resizeColumnsToContents()
                self.ui.topCategory.setColumnWidth(0, 150)
                self.ui.topCategory.setColumnWidth(1, 400)

                current_row_count = 0

                for row in results2:
                    for col_count in range(0, len(results2[0])):
                        self.ui.topCategory.setItem(current_row_count, col_count, QTableWidgetItem(str(row[col_count])))
                    current_row_count += 1
            except:
                print("Query failed - zipcode_stat2().")

    def search_button_pressed(self):
        category = self.ui.categoryList.selectedItems()[0].text()

        if len(self.ui.categoryList.selectedItems()) > 0:
            zipcode = self.ui.zipList.selectedItems()[0].text()

            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)

            sql_command = "SELECT business_name, address, city, business_avg_star, num_of_checkins, num_of_tips FROM hascategory, business WHERE category_type = '" + category + "' AND zip_code = '" + zipcode + "' AND hascategory.business_id = business.business_id ORDER BY business_name;"
            print(sql_command)
            print("")

            try:
                results = self.execute_query(sql_command)
                print(results)
                print("")

                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(
                    ["Business Name", "Address", "City", "Stars", "# of Checkins", "# of Tips"])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 350)
                self.ui.businessTable.setColumnWidth(1, 250)
                self.ui.businessTable.setColumnWidth(2, 70)
                self.ui.businessTable.setColumnWidth(3, 30)
                self.ui.businessTable.setColumnWidth(4, 100)
                self.ui.businessTable.setColumnWidth(5, 70)

                current_row_count = 0

                for row in results:
                    for col_count in range(0, len(results[0])):
                        self.ui.businessTable.setItem(current_row_count, col_count,
                                                      QTableWidgetItem(str(row[col_count])))

                    current_row_count += 1
            except:
                print("Query failed - search_button_pressed().")

    def clear_button_pressed(self):
        self.ui.businessTable.clear()
        self.ui.businessTable.setColumnCount(0)

    def refresh_button_pressed(self):
        self.ui.popularBusinessesTable.clear()
        category = self.ui.categoryList.selectedItems()[0].text()

        self.ui.popularBusinessesTable.setColumnCount(0)

        if len(self.ui.categoryList.selectedItems()) > 0:
            zipcode = self.ui.zipList.selectedItems()[0].text()

            sql_command = "SELECT businesspopularity.business_name, businesspopularity.num_of_checkins, businesspopularity.num_of_tips, businesspopularity.business_avg_star, popularity_rating FROM businesspopularity, business WHERE category_type = '" + category + "' AND zip_code = '" + zipcode + "' AND businesspopularity.business_id = business.business_id" + " ORDER BY popularity_rating DESC;"
            print(sql_command)
            print("")

            try:
                results = self.execute_query(sql_command)
                print(results)
                print("")

                style = "::section {""background-color: #f3f3f3; }"
                self.ui.popularBusinessesTable.horizontalHeader().setStyleSheet(style)
                self.ui.popularBusinessesTable.setColumnCount(len(results[0]))
                self.ui.popularBusinessesTable.setRowCount(len(results))
                self.ui.popularBusinessesTable.setHorizontalHeaderLabels(
                    ["Business Name", "# of Check-ins", "# of Tips", "Avg_rating", "Popularity Score"])
                self.ui.popularBusinessesTable.resizeColumnsToContents()
                self.ui.popularBusinessesTable.setColumnWidth(0, 400)
                self.ui.popularBusinessesTable.setColumnWidth(1, 150)
                self.ui.popularBusinessesTable.setColumnWidth(2, 150)
                self.ui.popularBusinessesTable.setColumnWidth(3, 150)
                self.ui.popularBusinessesTable.setColumnWidth(4, 200)

                current_row_count = 0

                for row in results:
                    for col_count in range(0, len(results[0])):
                        self.ui.popularBusinessesTable.setItem(current_row_count, col_count, QTableWidgetItem(str(row[col_count])))

                    current_row_count += 1
            except:
                print("Query failed - get_popular_business().")

    def user_login_updated(self):
        self.ui.loginUserIDs.clear()
        user_name = self.ui.loginUserName.toPlainText()

        if len(user_name) > 0:
            sql_statement = "SELECT u.user_id, u.user_name FROM users AS u WHERE user_name LIKE '" + user_name + "%'"
            print(sql_statement)
            print("")

            try:
                results = self.execute_query(sql_statement)

                for row in results:
                    self.ui.loginUserIDs.addItem(row[0])
            except:
                print("Query Failed - user_login_updated().")

    def user_id_selected(self):
        self.ui.infoName.clear()
        self.ui.infoStars.clear()
        self.ui.infoFans.clear()
        self.ui.infoYelpingSince.clear()
        self.ui.infoFunny.clear()
        self.ui.infoCool.clear()
        self.ui.infoUseful.clear()
        self.ui.latestTipsOfMyFriendsTable.clear()
        self.ui.myFriendsTable.clear()
        self.ui.friendSuggestionsTable.clear()

        selected_id = self.ui.loginUserIDs.selectedItems()[0].text()

        name_sql = "SELECT u.user_name FROM users AS U WHERE u.user_id = '" + selected_id + "'"
        stars_sql = "SELECT u.user_avg_stars FROM users AS U WHERE u.user_id = '" + selected_id + "'"
        fans_sql = "SELECT u.num_of_fans FROM users AS U WHERE u.user_id = '" + selected_id + "'"
        yelping_since_sql = "SELECT u.yelping_since FROM users AS U WHERE u.user_id = '" + selected_id + "'"
        funny_sql = "SELECT u.funny FROM users AS U WHERE u.user_id = '" + selected_id + "'"
        cool_sql = "SELECT u.cool FROM users AS U WHERE u.user_id = '" + selected_id + "'"
        useful_sql = "SELECT u.useful FROM users AS U WHERE u.user_id = '" + selected_id + "'"
        friends_table_sql = "SELECT u2.user_name, u2.user_avg_stars, u2.num_of_fans, u2.tip_count, u2.yelping_since FROM users AS u1 JOIN friends AS f ON u1.user_id = f.user_id JOIN users as u2 ON u2.user_id = f.friend_id WHERE u1.user_id = '" + selected_id + "' ORDER BY u2.user_name"
        latest_tips_table_sql = "SELECT ar.user_name, ar.business_name, ar.city, ar.tip_date, ar.tip_text FROM (SELECT u.user_name, b.business_name, b.city, yt.tip_date, yt.tip_text FROM friends AS f JOIN yelptip as yt on f.friend_id = yt.user_id JOIN users as u on f.friend_id = u.user_id JOIN business as b on b.business_id = yt.business_id WHERE f.user_id = '" + selected_id + "') AS ar JOIN (SELECT yt.user_id, MAX(yt.tip_date) as test FROM yelptip AS yt GROUP BY yt.user_id) AS al ON ar.tip_date = al.test ORDER BY user_name"
        suggested_friends_sql = "SELECT DISTINCT e.user_name, e.user_avg_stars, e.num_of_fans, e.tip_count, e.yelping_since FROM yelptip AS t JOIN (SELECT u.user_id, u.user_name, u.user_avg_stars, u.num_of_fans, u.tip_count, u.yelping_since FROM users AS u EXCEPT SELECT u2.user_id, u2.user_name, u2.user_avg_stars, u2.num_of_fans, u2.tip_count, u2.yelping_since FROM users AS u1 JOIN friends AS f ON u1.user_id = f.user_id JOIN users AS u2 ON u2.user_id = f.friend_id WHERE u1.user_id = '" + selected_id + "') AS e ON t.user_id = e.user_id WHERE t.business_id IN (SELECT business_id FROM yelptip WHERE user_id = '" + selected_id + "') UNION SELECT u3.user_name, u3.user_avg_stars, u3.num_of_fans, u3.tip_count, u3.yelping_since FROM users AS u3 JOIN (SELECT DISTINCT ff.friend_id FROM friends AS ff WHERE ff.user_id IN (SELECT f.friend_id FROM friends AS f WHERE f.user_id = '" + selected_id + "')) AS fofid on u3.user_id = fofid.friend_id ORDER BY 1"

        print(name_sql + "\n",
              stars_sql + "\n",
              fans_sql + "\n",
              yelping_since_sql + "\n",
              funny_sql + "\n",
              cool_sql + "\n",
              useful_sql + "\n",
              friends_table_sql + "\n",
              latest_tips_table_sql + "\n",
              suggested_friends_sql)
        print("")

        try:
            name_result = self.execute_query(name_sql)
            stars_result = self.execute_query(stars_sql)
            fans_result = self.execute_query(fans_sql)
            yelping_since_result = self.execute_query(yelping_since_sql)
            funny_result = self.execute_query(funny_sql)
            cool_result = self.execute_query(cool_sql)
            useful_sql = self.execute_query(useful_sql)
            friends_table_results = self.execute_query(friends_table_sql)
            latest_tips_table_results = self.execute_query(latest_tips_table_sql)
            suggested_friends_table_results = self.execute_query(suggested_friends_sql)

            self.ui.infoName.addItem(str(name_result[0][0]))
            self.ui.infoStars.addItem(str(stars_result[0][0]))
            self.ui.infoFans.addItem(str(fans_result[0][0]))
            self.ui.infoYelpingSince.addItem(str(yelping_since_result[0][0]))
            self.ui.infoFunny.addItem(str(funny_result[0][0]))
            self.ui.infoCool.addItem(str(cool_result[0][0]))
            self.ui.infoUseful.addItem(str(useful_sql[0][0]))

            style = "::section {""background-color: #f3f3f3; }"
            self.ui.myFriendsTable.horizontalHeader().setStyleSheet(style)
            self.ui.myFriendsTable.setColumnCount(len(friends_table_results[0]))
            self.ui.myFriendsTable.setRowCount(len(friends_table_results))
            self.ui.myFriendsTable.setHorizontalHeaderLabels(
                ["Friend Name", "Avg Stars", "Fans", "Tip Count", "Yelping Since"])
            self.ui.myFriendsTable.resizeColumnsToContents()
            self.ui.myFriendsTable.setColumnWidth(0, 110)
            self.ui.myFriendsTable.setColumnWidth(1, 70)
            self.ui.myFriendsTable.setColumnWidth(2, 30)
            self.ui.myFriendsTable.setColumnWidth(3, 70)
            self.ui.myFriendsTable.setColumnWidth(4, 200)
            current_row_count = 0
            for row in friends_table_results:
                for col_count in range(0, len(friends_table_results[0])):
                    self.ui.myFriendsTable.setItem(current_row_count, col_count, QTableWidgetItem(str(row[col_count])))
                current_row_count += 1

            if len(latest_tips_table_results) > 0:
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.latestTipsOfMyFriendsTable.horizontalHeader().setStyleSheet(style)
                self.ui.latestTipsOfMyFriendsTable.setColumnCount(len(latest_tips_table_results[0]))
                self.ui.latestTipsOfMyFriendsTable.setRowCount(len(latest_tips_table_results))
                self.ui.latestTipsOfMyFriendsTable.setHorizontalHeaderLabels(
                    ["Friend Name", "Business", "City", "Date", "Review"])
                self.ui.latestTipsOfMyFriendsTable.resizeColumnsToContents()
                self.ui.latestTipsOfMyFriendsTable.setColumnWidth(0, 110)
                self.ui.latestTipsOfMyFriendsTable.setColumnWidth(1, 150)
                self.ui.latestTipsOfMyFriendsTable.setColumnWidth(2, 75)
                self.ui.latestTipsOfMyFriendsTable.setColumnWidth(3, 110)
                self.ui.latestTipsOfMyFriendsTable.setColumnWidth(4, 125)
                current_row_count = 0
                for row in latest_tips_table_results:
                    for col_count in range(0, len(latest_tips_table_results[0])):
                        self.ui.latestTipsOfMyFriendsTable.setItem(current_row_count, col_count,
                                                                   QTableWidgetItem(str(row[col_count])))
                    current_row_count += 1
            else:
                self.ui.latestTipsOfMyFriendsTable.clear()
                self.ui.latestTipsOfMyFriendsTable.setColumnCount(0)
                self.ui.latestTipsOfMyFriendsTable.setRowCount(0)

            if len(suggested_friends_table_results) > 0:
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.friendSuggestionsTable.horizontalHeader().setStyleSheet(style)
                self.ui.friendSuggestionsTable.setColumnCount(len(suggested_friends_table_results[0]))
                self.ui.friendSuggestionsTable.setRowCount(len(suggested_friends_table_results))
                self.ui.friendSuggestionsTable.setHorizontalHeaderLabels(
                    ["Friend Name", "Avg Stars", "Fans", "Tip Count", "Yelping Since"])
                self.ui.friendSuggestionsTable.resizeColumnsToContents()
                self.ui.friendSuggestionsTable.setColumnWidth(0, 110)
                self.ui.friendSuggestionsTable.setColumnWidth(1, 70)
                self.ui.friendSuggestionsTable.setColumnWidth(2, 30)
                self.ui.friendSuggestionsTable.setColumnWidth(3, 70)
                self.ui.friendSuggestionsTable.setColumnWidth(4, 180)
                current_row_count = 0
                for row in suggested_friends_table_results:
                    for col_count in range(0, len(suggested_friends_table_results[0])):
                        self.ui.friendSuggestionsTable.setItem(current_row_count, col_count,
                                                               QTableWidgetItem(str(row[col_count])))
                    current_row_count += 1
            else:
                self.ui.friendSuggestionsTable.clear()
                self.ui.friendSuggestionsTable.setColumnCount(0)
                self.ui.friendSuggestionsTable.setRowCount(0)

        except:
            print("Query Failed - user_login_updated().")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Milestone2()
    window.show()
    sys.exit(app.exec_())
