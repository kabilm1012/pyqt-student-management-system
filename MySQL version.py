from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QWidget, QApplication, QGridLayout, \
    QPushButton, QLineEdit, QMainWindow, QTableWidget, QTableWidgetItem, \
    QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import mysql.connector

class DatabaseConnection:
    def __init__(self, host="localhost", user="root", password="Kabilm@1012", database="school"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        connection = mysql.connector.connect(host=self.host, user=self.user, 
                                             password=self.password, database=self.database)
        return connection
        


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Student Management System")
        self.setMinimumSize(600, 400)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)
        help_menu_item.addAction(about_action)

        search_student_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_student_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_student_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        self.load_data()

        # Create toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        # Add toolbar elements
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)

        # Create status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if not children:
            self.statusbar.addWidget(edit_button)
            self.statusbar.addWidget(delete_button)

    def load_data(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(list(result)):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()
    
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        search_dialog = SearchDialog()
        search_dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add Widgets
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_names = QComboBox()
        courses  = ["Biology", "Computer Science", "Accounts", "Arts"]
        self.course_names.addItems(courses)
        layout.addWidget(self.course_names)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add Submit Button
        register_button = QPushButton("Register")
        register_button.clicked.connect(self.add_student)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_names.currentText()
        mobile = self.mobile.text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (%s,%s,%s)", 
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add Widgets
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM STUDENTS WHERE name = %s", 
                                (name,))
        rows = cursor.fetchall()
        print(rows)
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()
        self.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Update Student Record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()
        course_name = main_window.table.item(index, 2).text()
        mobile = main_window.table.item(index, 3).text()
        self.student_id = main_window.table.item(index, 0).text()

        # Create widgets
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.courses_name = QComboBox()
        courses = ["Biology", "Computer Science", "Arts", "Accounts"]
        self.courses_name.addItems(courses)
        self.courses_name.setCurrentText(course_name)
        layout.addWidget(self.courses_name)

        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add button
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.edit)
        layout.addWidget(edit_button)

        self.setLayout(layout)

    def edit(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = %s, course = %s, mobile = %s WHERE id = %s",
                       (self.student_name.text(), self.courses_name.currentText(), 
                        self.mobile.text(), self.student_id))
        connection.commit()
        cursor.close()
        connection.close()

        # Refresh the table
        main_window.load_data()
        self.close()
        

class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Delete Student Record")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure want to delete?")
        yes_button = QPushButton("yes")
        yes_button.clicked.connect(self.yes)

        no_button = QPushButton("no")
        no_button.clicked.connect(self.no)

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0)
        layout.addWidget(no_button, 1, 1)

        self.setLayout(layout)

    def yes(self):
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = %s",
                       (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        
        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was successfully deleted!")
        confirmation_widget.exec()

    def no(self):
        self.close()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
This is a simple student management system app where we can edit, 
add and delete the student database. Feel free to modify and use!
"""
        self.setText(content)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
