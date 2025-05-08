from PyQt6.QtWidgets import *
from gui import *
import csv

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        """
        Sets up GUI, connects UI elements to their respective methods, and initially hides the score inputs
        """
        super().__init__()
        self.setupUi(self)

        self.__score_labels = [self.score1, self.score2, self.score3, self.score4]
        self.__score_inputs = [self.score1_entry, self.score2_entry, self.score3_entry, self.score4_entry]
        self.__score_errors = [self.score1_error, self.score2_error, self.score3_error, self.score4_error]

        self.submit_button.clicked.connect(lambda : self.submit())

        self.attempts.textChanged.connect(lambda : self.show_score_input())
        self.hide_score_input()

    def submit(self) -> None:
        """
        Stores a students grade information in data.csv
        """
        self.main_error.clear()
        name = self.check_name()
        scores = self.check_scores()

        if self.attempts.text() == '':
            self.error_number.setStyleSheet('color: red;')
            self.error_number.setText(f'Please enter valid number')

        if name is not None and scores is not None:
            score1, score2, score3, score4 = scores
            top_score = max(scores)
            data = [name, score1, score2, score3, score4, top_score]
            found = False
            with open('data.csv', 'r', newline='') as csvfile:
                content = csv.reader(csvfile)
                for row in content:
                    if row[0] == name:
                        found = True
                        break
            if found:
                self.main_error.setStyleSheet('color: red;')
                self.main_error.setText(f'Student already has grades entered')
            else:
                with open('data.csv', 'a', newline='') as csvfile:
                    content = csv.writer(csvfile)
                    content.writerow(data)
                    self.main_error.setStyleSheet('Color: green;')
                    self.main_error.setText('Submitted')

    def check_name(self) -> str or None:
        """
        Checks the name input to ensure it's valid
        :return: student name
        """
        name = self.name.text()
        try:
            if name is None:
                raise ValueError
            elif name.replace(' ', '').isalpha():
                self.error_name.clear()
                return name
            else:
                raise ValueError
        except ValueError:
            self.error_name.setStyleSheet('color: red;')
            self.error_name.setText(f'Please enter valid name')
            return None

    def hide_score_input(self) -> None:
        """
        Hides all the score inputs
        """
        for label in self.__score_labels:
            label.hide()

        for entry in self.__score_inputs:
            entry.hide()

    def show_score_input(self) -> None:
        """
        Method to show the number of score inputs based on the number of scores input
        """
        score_input = self.attempts.text()
        if score_input == '':
            self.error_number.clear()
        else:
            try:
                number_of_scores = int(score_input)
                if 1 <= number_of_scores <= 4:
                    self.error_number.setText(f'')
                    for score in range(len(self.__score_labels)):
                        self.__score_labels[score].hide()
                        self.__score_inputs[score].hide()
                        self.__score_errors[score].setText('')

                    for score in range(number_of_scores):
                        self.__score_labels[score].show()
                        self.__score_inputs[score].show()


                else:
                    raise ValueError
            except ValueError:
                self.error_number.setStyleSheet('color: red;')
                self.error_number.setText(f'Please enter valid number')

    def check_scores(self) -> list or None:
        """
        Method to validate scores
        :return: score
        """
        all_valid = True

        try:
            number_of_scores = int(self.attempts.text())
        except ValueError:
            return None

        scores = [0, 0, 0, 0]
        for score in range(number_of_scores):
            try:
                if 0 <= int(self.__score_inputs[score].text()) <= 100:
                    self.__score_errors[score].clear()
                    scores[score] = int(self.__score_inputs[score].text())
                else:
                    raise ValueError
            except ValueError:
                self.__score_errors[score].setStyleSheet('color: red;')
                self.__score_errors[score].setText(f'Please enter valid score')
                all_valid = False
        if all_valid:
            return scores
        else:
            return None


