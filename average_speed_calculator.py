from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QApplication, QLineEdit, \
     QPushButton, QComboBox
import sys


class AvgSpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Average Speed Calculator")
        grid = QGridLayout()

        # Create Widgets
        distance_label = QLabel("Distance:")
        self.distance_line_edit = QLineEdit()

        self.unit_combo = QComboBox()
        self.unit_combo.addItems(['metric(km)', 'imperial(miles)'])

        time_label = QLabel("Time(hours):")
        self.time_line_edit = QLineEdit()

        # Create Button
        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate_avg_speed)
        self.output_label = QLabel("")

        # Add widgets to grid
        grid.addWidget(distance_label, 1, 0)
        grid.addWidget(self.distance_line_edit, 1, 1)
        grid.addWidget(self.unit_combo, 1, 2)
        grid.addWidget(time_label, 2, 0)
        grid.addWidget(self.time_line_edit, 2, 1)
        grid.addWidget(calculate_button, 3, 0, 1, 3)
        grid.addWidget(self.output_label, 4, 0, 1, 3)

        self.setLayout(grid)

    def calculate_avg_speed(self):
        distance = float(self.distance_line_edit.text())
        time = float(self.time_line_edit.text())
        choosen_combo = self.unit_combo.currentText()

        avg_speed = distance / time

        if choosen_combo == "metric(km)":
            avg_speed = round(avg_speed, 2)
            unit = "km/hr"

        elif choosen_combo == "imperial(miles)":
            avg_speed = round(avg_speed * 0.621371, 2)
            unit = "mph"
            
        self.output_label.setText(f"Average Speed: {avg_speed} {unit}")


app = QApplication(sys.argv)
calculate_speed = AvgSpeedCalculator()
calculate_speed.show()
sys.exit(app.exec())




