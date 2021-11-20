from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont
from form.tictactoe_form import Ui_TICTACTOE
import sys
import time
from math import inf as infinity
import random


class TICTACTOE(QtWidgets.QMainWindow):
    def __init__(self):
        super(TICTACTOE, self).__init__()
        self.ui = Ui_TICTACTOE()
        self.ui.setupUi(self)

        self.time_ = 0
        self.turn = 0

        self.qmsgBox = QMessageBox()
        self.pushed = []
        self.push_list = []

        # creating 2d list
        for _ in range(7):
                temp = []
                for _ in range(7):
                        temp.append((QPushButton(self)))
                # adding 7 push button in single row
                self.push_list.append(temp)

        # x and y co-ordinate
        x = 90
        y = 90

        # traversing through push button list
        for i in range(7):
            for j in range(7):
                # setting geometry to the button
                self.push_list[i][j].setGeometry(x * i + 20,
                                                 y * j + 20,
                                                 80, 80)
                # setting font to the button
                self.push_list[i][j].setFont(QFont(QFont('Times', 20)))
                self.push_list[i][j].setStyleSheet("background-color: white")
                self.push_list[i][j].clicked.connect(self.action_called)

        # for i in range(7):
        #     for j in range(7):
        #         if self.push_list[i][j].text() == "":
        #             self.push_list[i][j].setText("X")



        self.ui.reset.clicked.connect(self.reset_game_action)
        self.ui.label.setText("X Player 1 to move")


    # method called by reset button
    def reset_game_action(self):

        # resetting values
        self.turn = 0
        self.times = 0

        # making label text empty:


        # traversing push list
        for buttons in self.push_list:
            for button in buttons:
                # making all the button enabled
                button.setEnabled(True)
                # removing text of all the buttons
                button.setText("")
                button.setStyleSheet("background-color: white")
                self.ui.label.setText("X Player 1 to move")

    def empty_cells(self):
        board = [
            [0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],
            [0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],
            [0,2],[1,2],[2,2],[3,2],[4,2],[5,2],[6,2],
            [0,3],[1,3],[2,3],[3,3],[4,3],[5,3],[6,3],
            [0,4],[1,4],[2,4],[3,4],[4,4],[5,4],[6,4],
            [0,5],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5],
            [0,6],[1,6],[2,6],[3,6],[4,6],[5,6],[6,6]
        ]
        for i in range(7):
            for j in range(7):
                try:
                    if self.push_list[i][j].text() == "X" or self.push_list[i][j].text() == "O":
                        board.remove([i,j])
                        self.pushed.append([i,j])
                except:
                    pass

        return board

    def minimax(self, isMaximazing):
        if self.who_wins_for_sanal() == "-1":
            return -1

        elif self.who_wins_for_sanal() == "1":
            return 1

        elif self.who_wins_for_sanal() == "0":
            return 0

        if isMaximazing == 1:
            # Aİ CHOOİCE
            bestscore = -1000
            for i in range(7):
                for j in range(7):
                    if self.push_list[i][j].text() == "":
                        self.push_list[i][j].setText("O")
                        self.push_list[i][j].setEnabled(False)
                        score = self.minimax(isMaximazing=0)
                        self.push_list[i][j].setText("")
                        self.push_list[i][j].setEnabled(True)
                        if score > bestscore:
                            bestscore = score
            return bestscore

        if isMaximazing == 0:
            bestscore = 1000

            for i in range(7):
                for j in range(7):
                    if self.push_list[i][j].text() == "":
                        self.push_list[i][j].setText("X")
                        self.push_list[i][j].setEnabled(False)
                        score = self.minimax(isMaximazing=1)
                        self.push_list[i][j].setText("")
                        self.push_list[i][j].setEnabled(True)
                        if score < bestscore:
                            bestscore = score
            return bestscore

    def ai_turn(self):
        # Aİ CHOOİCE
        bestscore = -1000
        a = 0
        b = 0
        for i in range(7):
            for j in range(7):
                if self.push_list[i][j].text() == "":
                    self.push_list[i][j].setText("O")
                    self.push_list[i][j].setEnabled(False)
                    score = self.minimax(self.turn)
                    self.push_list[i][j].setText("")
                    self.push_list[i][j].setEnabled(True)
                    if score > bestscore:
                        bestscore = score
                        a = i
                        b = j
        self.push_list[a][b].click()
        return

    def action_called(self):
        self.time_ += 1

        # getting button which called the action

        button = self.sender()
        print(self.pushed)

        x,y = random.choice(self.empty_cells())

        # making button disabled
        button.setEnabled(False)

        # checking the turn
        if self.turn == 0:
            button.setText("X")
            self.ui.label.setText("O Player 1 to move")
            self.winner()
            self.turn = 1
            if self.push_list[x][y].text() == "":
                self.push_list[x][y].click()
            else:
                if [x, y] in self.pushed:
                    x, y = random.choice(self.empty_cells())

        elif self.turn == 1:
            button.setText("O")
            self.ui.label.setText("X Player 1 to move")
            self.winner()
            self.turn = 0


    def winner(self):
        win = self.who_wins()
        if win == True:
            if self.turn == 1:
                self.ui.label.setText("")
                # O has won
                QMessageBox.information(self.qmsgBox, "WİNNER", "WİNNER O")
                self.reset_game_action()
                self.text = "O Won"

            # X has won
            else:
                self.ui.label.setText("")
                QMessageBox.information(self.qmsgBox, "WİNNER", "WİNNER X")
                self.reset_game_action()
                self.text = "X Won"

        if win == "0":
            self.ui.label.setText("")
            QMessageBox.information(self.qmsgBox, "DRAW", "NO ONE HAS WON -- DRAW ")
            self.reset_game_action()
            self.text = "DRAW"

    # method to check who wins
    def who_wins_for_sanal(self):

        # checking if any row crossed
        for i in range(7):
            if self.push_list[0][i].text() == self.push_list[1][i].text() \
                    and self.push_list[0][i].text() == self.push_list[2][i].text() \
                    and self.push_list[0][i].text() == self.push_list[3][i].text() \
                    and self.push_list[0][i].text() != "":
                if self.push_list[0][i].text() == "X":
                    return "-1"
                if self.push_list[0][i].text() == "O":
                    return "1"

            if self.push_list[1][i].text() == self.push_list[2][i].text() \
                    and self.push_list[1][i].text() == self.push_list[3][i].text() \
                    and self.push_list[1][i].text() == self.push_list[4][i].text() \
                    and self.push_list[1][i].text() != "":
                if self.push_list[1][i].text() == "X":
                    return "-1"
                if self.push_list[1][i].text() == "O":
                    return "1"

            if self.push_list[2][i].text() == self.push_list[3][i].text() \
                    and self.push_list[2][i].text() == self.push_list[4][i].text() \
                    and self.push_list[2][i].text() == self.push_list[5][i].text() \
                    and self.push_list[2][i].text() != "":
                if self.push_list[2][i].text() == "X":
                    return "-1"
                if self.push_list[2][i].text() == "O":
                    return "1"

            if self.push_list[3][i].text() == self.push_list[4][i].text() \
                    and self.push_list[3][i].text() == self.push_list[5][i].text() \
                    and self.push_list[3][i].text() == self.push_list[6][i].text() \
                    and self.push_list[3][i].text() != "":
                if self.push_list[3][i].text() == "X":
                    return "-1"
                if self.push_list[3][i].text() == "O":
                    return "1"


        # checking if any column crossed
        for i in range(7):
            if self.push_list[i][0].text() == self.push_list[i][1].text() \
                    and self.push_list[i][0].text() == self.push_list[i][2].text() \
                    and self.push_list[i][0].text() == self.push_list[i][3].text() \
                    and self.push_list[i][0].text() != "":
                if self.push_list[i][0].text() == "X":
                    return "-1"
                if self.push_list[i][0].text() == "O":
                    return "1"

            if self.push_list[i][1].text() == self.push_list[i][2].text() \
                    and self.push_list[i][1].text() == self.push_list[i][3].text() \
                    and self.push_list[i][1].text() == self.push_list[i][4].text() \
                    and self.push_list[i][1].text() != "":
                if self.push_list[i][1].text() == "X":
                    return "-1"
                if self.push_list[i][1].text() == "O":
                    return "1"

            if self.push_list[i][2].text() == self.push_list[i][3].text() \
                    and self.push_list[i][2].text() == self.push_list[i][4].text() \
                    and self.push_list[i][2].text() == self.push_list[i][5].text() \
                    and self.push_list[i][2].text() != "":
                if self.push_list[i][2].text() == "X":
                    return "-1"
                if self.push_list[i][2].text() == "O":
                    return "1"

            if self.push_list[i][3].text() == self.push_list[i][4].text() \
                    and self.push_list[i][3].text() == self.push_list[i][5].text() \
                    and self.push_list[i][3].text() == self.push_list[i][6].text() \
                    and self.push_list[i][3].text() != "":
                if self.push_list[i][3].text() == "X":
                    return "-1"
                if self.push_list[i][3].text() == "O":
                    return "1"


        # checking if diagonal crossed
        if self.push_list[0][0].text() == self.push_list[1][1].text() \
                and self.push_list[0][0].text() == self.push_list[2][2].text() \
                and self.push_list[0][0].text() == self.push_list[3][3].text() \
                and self.push_list[0][0].text() != "":
            if self.push_list[0][0].text() == "X":
                return "-1"
            if self.push_list[0][0].text() == "O":
                return "1"

        # checking if diagonal crossed
        if self.push_list[1][1].text() == self.push_list[2][2].text() \
                and self.push_list[1][1].text() == self.push_list[3][3].text() \
                and self.push_list[1][1].text() == self.push_list[4][4].text() \
                and self.push_list[1][1].text() != "":
            if self.push_list[1][1].text() == "X":
                return "-1"
            if self.push_list[1][1].text() == "O":
                return "1"

        # checking if diagonal crossed
        if self.push_list[2][2].text() == self.push_list[3][3].text() \
                and self.push_list[2][2].text() == self.push_list[4][4].text() \
                and self.push_list[2][2].text() == self.push_list[5][5].text() \
                and self.push_list[2][2].text() != "":
            if self.push_list[2][2].text() == "X":
                return "-1"
            if self.push_list[2][2].text() == "O":
                return "1"

        # checking if diagonal crossed
        if self.push_list[3][3].text() == self.push_list[4][4].text() \
                and self.push_list[3][3].text() == self.push_list[5][5].text() \
                and self.push_list[3][3].text() == self.push_list[6][6].text() \
                and self.push_list[3][3].text() != "":
            if self.push_list[3][3].text() == "X":
                return "-1"
            if self.push_list[3][3].text() == "O":
                return "1"

        if self.push_list[0][1].text() == self.push_list[1][2].text() \
                and self.push_list[0][1].text() == self.push_list[2][3].text() \
                and self.push_list[0][1].text() == self.push_list[3][4].text() \
                and self.push_list[0][1].text() != "":
            if self.push_list[0][1].text() == "X":
                return "-1"
            if self.push_list[0][1].text() == "O":
                return "1"

        if self.push_list[1][2].text() == self.push_list[2][3].text() \
                and self.push_list[1][2].text() == self.push_list[3][4].text() \
                and self.push_list[1][2].text() == self.push_list[4][5].text() \
                and self.push_list[1][2].text() != "":
            if self.push_list[1][2].text() == "X":
                return "-1"
            if self.push_list[1][2].text() == "O":
                return "1"

        if self.push_list[2][3].text() == self.push_list[3][4].text() \
                and self.push_list[2][3].text() == self.push_list[4][5].text() \
                and self.push_list[2][3].text() == self.push_list[5][6].text() \
                and self.push_list[2][3].text() != "":
            if self.push_list[2][3].text() == "X":
                return "-1"
            if self.push_list[2][3].text() == "O":
                return "1"

        if self.push_list[0][2].text() == self.push_list[2][4].text() \
                and self.push_list[0][2].text() == self.push_list[2][4].text() \
                and self.push_list[0][2].text() == self.push_list[3][5].text() \
                and self.push_list[0][2].text() != "":
            if self.push_list[0][2].text() == "X":
                return "-1"
            if self.push_list[0][2].text() == "O":
                return "1"

        if self.push_list[1][3].text() == self.push_list[2][4].text() \
                and self.push_list[1][3].text() == self.push_list[3][5].text() \
                and self.push_list[1][3].text() == self.push_list[4][6].text() \
                and self.push_list[1][3].text() != "":
            if self.push_list[1][3].text() == "X":
                return "-1"
            if self.push_list[1][3].text() == "O":
                return "1"

        if self.push_list[0][3].text() == self.push_list[1][4].text() \
                and self.push_list[0][3].text() == self.push_list[2][5].text() \
                and self.push_list[0][3].text() == self.push_list[3][6].text() \
                and self.push_list[0][3].text() != "":
            if self.push_list[0][3].text() == "X":
                return "-1"
            if self.push_list[0][3].text() == "O":
                return "1"

        if self.push_list[0][3].text() == self.push_list[1][2].text() \
                and self.push_list[0][3].text() == self.push_list[2][1].text() \
                and self.push_list[0][3].text() == self.push_list[3][0].text() \
                and self.push_list[0][3].text() != "":
            if self.push_list[0][3].text() == "X":
                return "-1"
            if self.push_list[0][3].text() == "O":
                return "1"

        if self.push_list[0][4].text() == self.push_list[1][3].text() \
                and self.push_list[0][4].text() == self.push_list[2][2].text() \
                and self.push_list[0][4].text() == self.push_list[3][1].text() \
                and self.push_list[0][4].text() != "":
            if self.push_list[0][4].text() == "X":
                return "-1"
            if self.push_list[0][4].text() == "O":
                return "1"

        if self.push_list[1][3].text() == self.push_list[2][2].text() \
                and self.push_list[1][3].text() == self.push_list[3][1].text() \
                and self.push_list[1][3].text() == self.push_list[4][0].text() \
                and self.push_list[1][3].text() != "":
            if self.push_list[1][3].text() == "X":
                return "-1"
            if self.push_list[1][3].text() == "O":
                return "1"

        if self.push_list[0][5].text() == self.push_list[1][4].text() \
                and self.push_list[0][5].text() == self.push_list[2][3].text() \
                and self.push_list[0][5].text() == self.push_list[3][2].text() \
                and self.push_list[0][5].text() != "":
            if self.push_list[0][5].text() == "X":
                return "-1"
            if self.push_list[0][5].text() == "O":
                return "1"

        if self.push_list[1][4].text() == self.push_list[2][3].text() \
                and self.push_list[1][4].text() == self.push_list[3][2].text() \
                and self.push_list[1][4].text() == self.push_list[4][1].text() \
                and self.push_list[1][4].text() != "":
            if self.push_list[1][4].text() == "X":
                return "-1"
            if self.push_list[1][4].text() == "O":
                return "1"

        if self.push_list[2][3].text() == self.push_list[3][2].text() \
                and self.push_list[2][3].text() == self.push_list[4][1].text() \
                and self.push_list[2][3].text() == self.push_list[5][0].text() \
                and self.push_list[2][3].text() != "":
            if self.push_list[2][3].text() == "X":
                return "-1"
            if self.push_list[2][3].text() == "O":
                return "1"

        if self.push_list[0][6].text() == self.push_list[1][5].text() \
                and self.push_list[0][6].text() == self.push_list[2][4].text() \
                and self.push_list[0][6].text() == self.push_list[3][3].text() \
                and self.push_list[0][6].text() != "":
            if self.push_list[0][6].text() == "X":
                return "-1"
            if self.push_list[0][6].text() == "O":
                return "1"

        if self.push_list[1][5].text() == self.push_list[2][4].text() \
                and self.push_list[1][5].text() == self.push_list[3][3].text() \
                and self.push_list[1][5].text() == self.push_list[4][2].text() \
                and self.push_list[1][5].text() != "":
            if self.push_list[1][5].text() == "X":
                return "-1"
            if self.push_list[1][5].text() == "O":
                return "1"

        if self.push_list[2][4].text() == self.push_list[3][3].text() \
                and self.push_list[2][4].text() == self.push_list[4][2].text() \
                and self.push_list[2][4].text() == self.push_list[5][1].text() \
                and self.push_list[2][4].text() != "":
            if self.push_list[2][4].text() == "X":
                return "-1"
            if self.push_list[2][4].text() == "O":
                return "1"

        if self.push_list[3][3].text() == self.push_list[4][2].text() \
                and self.push_list[3][3].text() == self.push_list[5][1].text() \
                and self.push_list[3][3].text() == self.push_list[6][0].text() \
                and self.push_list[3][3].text() != "":
            if self.push_list[3][3].text() == "X":
                return "-1"
            if self.push_list[3][3].text() == "O":
                return "1"

        if self.push_list[1][0].text() == self.push_list[2][1].text() \
                and self.push_list[1][0].text() == self.push_list[3][2].text() \
                and self.push_list[1][0].text() == self.push_list[4][3].text() \
                and self.push_list[1][0].text() != "":
            if self.push_list[1][0].text() == "X":
                return "-1"
            if self.push_list[1][0].text() == "O":
                return "1"

        if self.push_list[2][1].text() == self.push_list[3][2].text() \
                and self.push_list[2][1].text() == self.push_list[4][3].text() \
                and self.push_list[2][1].text() == self.push_list[5][4].text() \
                and self.push_list[2][1].text() != "":
            if self.push_list[2][1].text() == "X":
                return "-1"
            if self.push_list[2][1].text() == "O":
                return "1"

        if self.push_list[3][2].text() == self.push_list[4][3].text() \
                and self.push_list[3][2].text() == self.push_list[5][4].text() \
                and self.push_list[3][2].text() == self.push_list[6][5].text() \
                and self.push_list[3][2].text() != "":
            if self.push_list[3][2].text() == "X":
                return "-1"
            if self.push_list[3][2].text() == "O":
                return "1"

        if self.push_list[1][1].text() == self.push_list[2][2].text() \
                and self.push_list[1][1].text() == self.push_list[3][3].text() \
                and self.push_list[1][1].text() == self.push_list[4][4].text() \
                and self.push_list[1][1].text() != "":
            if self.push_list[1][1].text() == "X":
                return "-1"
            if self.push_list[1][1].text() == "O":
                return "1"

        if self.push_list[2][2].text() == self.push_list[3][3].text() \
                and self.push_list[2][2].text() == self.push_list[4][4].text() \
                and self.push_list[2][2].text() == self.push_list[5][5].text() \
                and self.push_list[2][2].text() != "":
            if self.push_list[2][2].text() == "X":
                return "-1"
            if self.push_list[2][2].text() == "O":
                return "1"

        if self.push_list[3][3].text() == self.push_list[4][4].text() \
                and self.push_list[3][3].text() == self.push_list[5][5].text() \
                and self.push_list[3][3].text() == self.push_list[6][6].text() \
                and self.push_list[3][3].text() != "":
            if self.push_list[3][3].text() == "X":
                return "-1"
            if self.push_list[3][3].text() == "O":
                return "1"

        if self.push_list[1][2].text() == self.push_list[2][3].text() \
                and self.push_list[1][2].text() == self.push_list[3][4].text() \
                and self.push_list[1][2].text() == self.push_list[4][5].text() \
                and self.push_list[1][2].text() != "":
            if self.push_list[1][2].text() == "X":
                return "-1"
            if self.push_list[1][2].text() == "O":
                return "1"

        if self.push_list[2][3].text() == self.push_list[3][4].text() \
                and self.push_list[2][3].text() == self.push_list[4][5].text() \
                and self.push_list[2][3].text() == self.push_list[5][6].text() \
                and self.push_list[2][3].text() != "":
            if self.push_list[2][3].text() == "X":
                return "-1"
            if self.push_list[2][3].text() == "O":
                return "1"

        if self.push_list[1][3].text() == self.push_list[2][4].text() \
                and self.push_list[2][3].text() == self.push_list[3][5].text() \
                and self.push_list[2][3].text() == self.push_list[4][6].text() \
                and self.push_list[2][3].text() != "":
            if self.push_list[1][3].text() == "X":
                return "-1"
            if self.push_list[1][3].text() == "O":
                return "1"

        if self.push_list[1][6].text() == self.push_list[2][5].text() \
                and self.push_list[1][6].text() == self.push_list[3][4].text() \
                and self.push_list[1][6].text() == self.push_list[4][3].text() \
                and self.push_list[1][6].text() != "":
            if self.push_list[1][6].text() == "X":
                return "-1"
            if self.push_list[1][6].text() == "O":
                return "1"

        if self.push_list[2][5].text() == self.push_list[3][4].text() \
                and self.push_list[2][5].text() == self.push_list[4][3].text() \
                and self.push_list[2][5].text() == self.push_list[5][2].text() \
                and self.push_list[2][5].text() != "":
            if self.push_list[2][5].text() == "X":
                return "-1"
            if self.push_list[2][5].text() == "O":
                return "1"

        if self.push_list[3][4].text() == self.push_list[4][3].text() \
                and self.push_list[3][4].text() == self.push_list[5][2].text() \
                and self.push_list[3][4].text() == self.push_list[6][1].text() \
                and self.push_list[3][4].text() != "":
            if self.push_list[3][4].text() == "X":
                return "-1"
            if self.push_list[3][4].text() == "O":
                return "1"

        if self.push_list[2][0].text() == self.push_list[3][1].text() \
                and self.push_list[2][0].text() == self.push_list[4][2].text() \
                and self.push_list[2][0].text() == self.push_list[5][3].text() \
                and self.push_list[2][0].text() != "":
            if self.push_list[2][0].text() == "X":
                return "-1"
            if self.push_list[2][0].text() == "O":
                return "1"
        if self.push_list[3][1].text() == self.push_list[4][2].text() \
                and self.push_list[3][1].text() == self.push_list[5][3].text() \
                and self.push_list[3][1].text() == self.push_list[6][4].text() \
                and self.push_list[3][1].text() != "":
            if self.push_list[3][1].text() == "X":
                return "-1"
            if self.push_list[3][1].text() == "O":
                return "1"

        if self.push_list[3][0].text() == self.push_list[4][1].text() \
                and self.push_list[3][0].text() == self.push_list[5][2].text() \
                and self.push_list[3][0].text() == self.push_list[6][3].text() \
                and self.push_list[3][0].text() != "":
            if self.push_list[3][0].text() == "X":
                return "-1"
            if self.push_list[3][0].text() == "O":
                return "1"

        if self.push_list[2][6].text() == self.push_list[3][5].text() \
                and self.push_list[2][6].text() == self.push_list[4][4].text() \
                and self.push_list[2][6].text() == self.push_list[5][3].text() \
                and self.push_list[2][6].text() != "":
            if self.push_list[2][6].text() == "X":
                return "-1"
            if self.push_list[2][6].text() == "O":
                return "1"

        if self.push_list[3][5].text() == self.push_list[4][4].text() \
                and self.push_list[3][5].text() == self.push_list[5][3].text() \
                and self.push_list[3][5].text() == self.push_list[6][2].text() \
                and self.push_list[3][5].text() != "":
            if self.push_list[3][5].text() == "X":
                return "-1"
            if self.push_list[3][5].text() == "O":
                return "1"

        if self.push_list[3][6].text() == self.push_list[4][5].text() \
                and self.push_list[3][6].text() == self.push_list[5][4].text() \
                and self.push_list[3][6].text() == self.push_list[6][3].text() \
                and self.push_list[3][6].text() != "":
            if self.push_list[3][6].text() == "X":
                return "-1"
            if self.push_list[3][6].text() == "O":
                return "1"

        berabere_list = []
        for i in range(7):
            for j in range(7):
                if self.push_list[i][j].text() != "":
                    berabere_list.append(self.push_list[i][j])
        if len(berabere_list) == 49:
            return "0"

        # # if nothing is crossed
        # return False

    def who_wins(self):

        # checking if any row crossed
        for i in range(7):
            if self.push_list[0][i].text() == self.push_list[1][i].text() \
                    and self.push_list[0][i].text() == self.push_list[2][i].text() \
                    and self.push_list[0][i].text() == self.push_list[3][i].text() \
                    and self.push_list[0][i].text() != "":
                self.push_list[0][i].setStyleSheet("background-color: red")
                self.push_list[1][i].setStyleSheet("background-color: red")
                self.push_list[2][i].setStyleSheet("background-color: red")
                self.push_list[3][i].setStyleSheet("background-color: red")
                return True

            if self.push_list[1][i].text() == self.push_list[2][i].text() \
                    and self.push_list[1][i].text() == self.push_list[3][i].text() \
                    and self.push_list[1][i].text() == self.push_list[4][i].text() \
                    and self.push_list[1][i].text() != "":
                self.push_list[1][i].setStyleSheet("background-color: red")
                self.push_list[2][i].setStyleSheet("background-color: red")
                self.push_list[3][i].setStyleSheet("background-color: red")
                self.push_list[4][i].setStyleSheet("background-color: red")
                return True

            if self.push_list[2][i].text() == self.push_list[3][i].text() \
                    and self.push_list[2][i].text() == self.push_list[4][i].text() \
                    and self.push_list[2][i].text() == self.push_list[5][i].text() \
                    and self.push_list[2][i].text() != "":
                self.push_list[2][i].setStyleSheet("background-color: red")
                self.push_list[3][i].setStyleSheet("background-color: red")
                self.push_list[4][i].setStyleSheet("background-color: red")
                self.push_list[5][i].setStyleSheet("background-color: red")
                return True

            if self.push_list[3][i].text() == self.push_list[4][i].text() \
                    and self.push_list[3][i].text() == self.push_list[5][i].text() \
                    and self.push_list[3][i].text() == self.push_list[6][i].text() \
                    and self.push_list[3][i].text() != "":
                self.push_list[3][i].setStyleSheet("background-color: red")
                self.push_list[4][i].setStyleSheet("background-color: red")
                self.push_list[5][i].setStyleSheet("background-color: red")
                self.push_list[6][i].setStyleSheet("background-color: red")
                return True


        # checking if any column crossed
        for i in range(7):
            if self.push_list[i][0].text() == self.push_list[i][1].text() \
                    and self.push_list[i][0].text() == self.push_list[i][2].text() \
                    and self.push_list[i][0].text() == self.push_list[i][3].text() \
                    and self.push_list[i][0].text() != "":
                self.push_list[i][0].setStyleSheet("background-color: red")
                self.push_list[i][1].setStyleSheet("background-color: red")
                self.push_list[i][2].setStyleSheet("background-color: red")
                self.push_list[i][3].setStyleSheet("background-color: red")
                return True

            if self.push_list[i][1].text() == self.push_list[i][2].text() \
                    and self.push_list[i][1].text() == self.push_list[i][3].text() \
                    and self.push_list[i][1].text() == self.push_list[i][4].text() \
                    and self.push_list[i][1].text() != "":
                self.push_list[i][1].setStyleSheet("background-color: red")
                self.push_list[i][2].setStyleSheet("background-color: red")
                self.push_list[i][3].setStyleSheet("background-color: red")
                self.push_list[i][4].setStyleSheet("background-color: red")
                return True

            if self.push_list[i][2].text() == self.push_list[i][3].text() \
                    and self.push_list[i][2].text() == self.push_list[i][4].text() \
                    and self.push_list[i][2].text() == self.push_list[i][5].text() \
                    and self.push_list[i][2].text() != "":
                self.push_list[i][2].setStyleSheet("background-color: red")
                self.push_list[i][3].setStyleSheet("background-color: red")
                self.push_list[i][4].setStyleSheet("background-color: red")
                self.push_list[i][5].setStyleSheet("background-color: red")
                return True

            if self.push_list[i][3].text() == self.push_list[i][4].text() \
                    and self.push_list[i][3].text() == self.push_list[i][5].text() \
                    and self.push_list[i][3].text() == self.push_list[i][6].text() \
                    and self.push_list[i][3].text() != "":
                self.push_list[i][3].setStyleSheet("background-color: red")
                self.push_list[i][4].setStyleSheet("background-color: red")
                self.push_list[i][5].setStyleSheet("background-color: red")
                self.push_list[i][6].setStyleSheet("background-color: red")
                return True

        # checking if diagonal crossed
        if self.push_list[0][0].text() == self.push_list[1][1].text() \
                and self.push_list[0][0].text() == self.push_list[2][2].text() \
                and self.push_list[0][0].text() == self.push_list[3][3].text() \
                and self.push_list[0][0].text() != "":
            self.push_list[0][0].setStyleSheet("background-color: red")
            self.push_list[1][1].setStyleSheet("background-color: red")
            self.push_list[2][2].setStyleSheet("background-color: red")
            self.push_list[3][3].setStyleSheet("background-color: red")
            return True

        # checking if diagonal crossed
        if self.push_list[1][1].text() == self.push_list[2][2].text() \
                and self.push_list[1][1].text() == self.push_list[3][3].text() \
                and self.push_list[1][1].text() == self.push_list[4][4].text() \
                and self.push_list[1][1].text() != "":
            self.push_list[1][1].setStyleSheet("background-color: red")
            self.push_list[2][2].setStyleSheet("background-color: red")
            self.push_list[3][3].setStyleSheet("background-color: red")
            self.push_list[4][4].setStyleSheet("background-color: red")
            return True

        # checking if diagonal crossed
        if self.push_list[2][2].text() == self.push_list[3][3].text() \
                and self.push_list[2][2].text() == self.push_list[4][4].text() \
                and self.push_list[2][2].text() == self.push_list[5][5].text() \
                and self.push_list[2][2].text() != "":
            self.push_list[2][2].setStyleSheet("background-color: red")
            self.push_list[3][3].setStyleSheet("background-color: red")
            self.push_list[4][4].setStyleSheet("background-color: red")
            self.push_list[5][5].setStyleSheet("background-color: red")
            return True

        # checking if diagonal crossed
        if self.push_list[3][3].text() == self.push_list[4][4].text() \
                and self.push_list[3][3].text() == self.push_list[5][5].text() \
                and self.push_list[3][3].text() == self.push_list[6][6].text() \
                and self.push_list[3][3].text() != "":
            self.push_list[3][3].setStyleSheet("background-color: red")
            self.push_list[4][4].setStyleSheet("background-color: red")
            self.push_list[5][5].setStyleSheet("background-color: red")
            self.push_list[6][6].setStyleSheet("background-color: red")
            return True

        if self.push_list[0][1].text() == self.push_list[1][2].text() \
                and self.push_list[0][1].text() == self.push_list[2][3].text() \
                and self.push_list[0][1].text() == self.push_list[3][4].text() \
                and self.push_list[0][1].text() != "":
            self.push_list[0][1].setStyleSheet("background-color: red")
            self.push_list[1][2].setStyleSheet("background-color: red")
            self.push_list[2][3].setStyleSheet("background-color: red")
            self.push_list[3][4].setStyleSheet("background-color: red")
            return True

        if self.push_list[1][2].text() == self.push_list[2][3].text() \
                and self.push_list[1][2].text() == self.push_list[3][4].text() \
                and self.push_list[1][2].text() == self.push_list[4][5].text() \
                and self.push_list[1][2].text() != "":
            self.push_list[1][2].setStyleSheet("background-color: red")
            self.push_list[2][3].setStyleSheet("background-color: red")
            self.push_list[3][4].setStyleSheet("background-color: red")
            self.push_list[4][5].setStyleSheet("background-color: red")
            return True

        if self.push_list[2][3].text() == self.push_list[3][4].text() \
                and self.push_list[2][3].text() == self.push_list[4][5].text() \
                and self.push_list[2][3].text() == self.push_list[5][6].text() \
                and self.push_list[2][3].text() != "":
            self.push_list[2][3].setStyleSheet("background-color: red")
            self.push_list[3][4].setStyleSheet("background-color: red")
            self.push_list[4][5].setStyleSheet("background-color: red")
            self.push_list[5][6].setStyleSheet("background-color: red")
            return True

        if self.push_list[0][2].text() == self.push_list[1][3].text() \
                and self.push_list[0][2].text() == self.push_list[2][4].text() \
                and self.push_list[0][2].text() == self.push_list[3][5].text() \
                and self.push_list[0][2].text() != "":
            self.push_list[0][2].setStyleSheet("background-color: red")
            self.push_list[1][3].setStyleSheet("background-color: red")
            self.push_list[2][4].setStyleSheet("background-color: red")
            self.push_list[3][5].setStyleSheet("background-color: red")
            return True

        if self.push_list[1][3].text() == self.push_list[2][4].text() \
                and self.push_list[1][3].text() == self.push_list[3][5].text() \
                and self.push_list[1][3].text() == self.push_list[4][6].text() \
                and self.push_list[1][3].text() != "":
            self.push_list[1][3].setStyleSheet("background-color: red")
            self.push_list[2][4].setStyleSheet("background-color: red")
            self.push_list[3][5].setStyleSheet("background-color: red")
            self.push_list[4][6].setStyleSheet("background-color: red")
            return True

        if self.push_list[0][3].text() == self.push_list[1][4].text() \
                and self.push_list[0][3].text() == self.push_list[2][5].text() \
                and self.push_list[0][3].text() == self.push_list[3][6].text() \
                and self.push_list[0][3].text() != "":
            self.push_list[0][3].setStyleSheet("background-color: red")
            self.push_list[1][4].setStyleSheet("background-color: red")
            self.push_list[2][5].setStyleSheet("background-color: red")
            self.push_list[3][6].setStyleSheet("background-color: red")
            return True

        if self.push_list[0][3].text() == self.push_list[1][2].text() \
                and self.push_list[0][3].text() == self.push_list[2][1].text() \
                and self.push_list[0][3].text() == self.push_list[3][0].text() \
                and self.push_list[0][3].text() != "":
            self.push_list[0][3].setStyleSheet("background-color: red")
            self.push_list[1][2].setStyleSheet("background-color: red")
            self.push_list[2][1].setStyleSheet("background-color: red")
            self.push_list[3][0].setStyleSheet("background-color: red")
            return True

        if self.push_list[0][4].text() == self.push_list[1][3].text() \
                and self.push_list[0][4].text() == self.push_list[2][2].text() \
                and self.push_list[0][4].text() == self.push_list[3][1].text() \
                and self.push_list[0][4].text() != "":
            self.push_list[0][4].setStyleSheet("background-color: red")
            self.push_list[1][3].setStyleSheet("background-color: red")
            self.push_list[2][2].setStyleSheet("background-color: red")
            self.push_list[3][1].setStyleSheet("background-color: red")
            return True

        if self.push_list[1][3].text() == self.push_list[2][2].text() \
                and self.push_list[1][3].text() == self.push_list[3][1].text() \
                and self.push_list[1][3].text() == self.push_list[4][0].text() \
                and self.push_list[1][3].text() != "":
            self.push_list[1][3].setStyleSheet("background-color: red")
            self.push_list[2][2].setStyleSheet("background-color: red")
            self.push_list[3][1].setStyleSheet("background-color: red")
            self.push_list[4][0].setStyleSheet("background-color: red")
            return True

        if self.push_list[0][5].text() == self.push_list[1][4].text() \
                and self.push_list[0][5].text() == self.push_list[2][3].text() \
                and self.push_list[0][5].text() == self.push_list[3][2].text() \
                and self.push_list[0][5].text() != "":
            self.push_list[0][5].setStyleSheet("background-color: red")
            self.push_list[1][4].setStyleSheet("background-color: red")
            self.push_list[2][3].setStyleSheet("background-color: red")
            self.push_list[3][2].setStyleSheet("background-color: red")
            return True

        if self.push_list[1][4].text() == self.push_list[2][3].text() \
                and self.push_list[1][4].text() == self.push_list[3][2].text() \
                and self.push_list[1][4].text() == self.push_list[4][1].text() \
                and self.push_list[1][4].text() != "":
            self.push_list[1][4].setStyleSheet("background-color: red")
            self.push_list[2][3].setStyleSheet("background-color: red")
            self.push_list[3][2].setStyleSheet("background-color: red")
            self.push_list[4][1].setStyleSheet("background-color: red")
            return True

        if self.push_list[2][3].text() == self.push_list[3][2].text() \
                and self.push_list[2][3].text() == self.push_list[4][1].text() \
                and self.push_list[2][3].text() == self.push_list[5][0].text() \
                and self.push_list[2][3].text() != "":
            self.push_list[2][3].setStyleSheet("background-color: red")
            self.push_list[3][2].setStyleSheet("background-color: red")
            self.push_list[4][1].setStyleSheet("background-color: red")
            self.push_list[5][0].setStyleSheet("background-color: red")
            return True

        if self.push_list[0][6].text() == self.push_list[1][5].text() \
                and self.push_list[0][6].text() == self.push_list[2][4].text() \
                and self.push_list[0][6].text() == self.push_list[3][3].text() \
                and self.push_list[0][6].text() != "":
            self.push_list[0][6].setStyleSheet("background-color: red")
            self.push_list[1][5].setStyleSheet("background-color: red")
            self.push_list[2][4].setStyleSheet("background-color: red")
            self.push_list[3][3].setStyleSheet("background-color: red")
            return True

        if self.push_list[1][5].text() == self.push_list[2][4].text() \
                and self.push_list[1][5].text() == self.push_list[3][3].text() \
                and self.push_list[1][5].text() == self.push_list[4][2].text() \
                and self.push_list[1][5].text() != "":
            self.push_list[1][5].setStyleSheet("background-color: red")
            self.push_list[2][4].setStyleSheet("background-color: red")
            self.push_list[3][3].setStyleSheet("background-color: red")
            self.push_list[4][2].setStyleSheet("background-color: red")
            return True

        if self.push_list[2][4].text() == self.push_list[3][3].text() \
                and self.push_list[2][4].text() == self.push_list[4][2].text() \
                and self.push_list[2][4].text() == self.push_list[5][1].text() \
                and self.push_list[2][4].text() != "":
            self.push_list[2][4].setStyleSheet("background-color: red")
            self.push_list[3][3].setStyleSheet("background-color: red")
            self.push_list[4][2].setStyleSheet("background-color: red")
            self.push_list[5][1].setStyleSheet("background-color: red")
            return True

        if self.push_list[3][3].text() == self.push_list[4][2].text() \
                and self.push_list[3][3].text() == self.push_list[5][1].text() \
                and self.push_list[3][3].text() == self.push_list[6][0].text() \
                and self.push_list[3][3].text() != "":
            self.push_list[3][3].setStyleSheet("background-color: red")
            self.push_list[4][2].setStyleSheet("background-color: red")
            self.push_list[5][1].setStyleSheet("background-color: red")
            self.push_list[6][0].setStyleSheet("background-color: red")
            return True

        if self.push_list[1][0].text() == self.push_list[2][1].text() \
                and self.push_list[1][0].text() == self.push_list[3][2].text() \
                and self.push_list[1][0].text() == self.push_list[4][3].text() \
                and self.push_list[1][0].text() != "":
            self.push_list[1][0].setStyleSheet("background-color: red")
            self.push_list[2][1].setStyleSheet("background-color: red")
            self.push_list[3][2].setStyleSheet("background-color: red")
            self.push_list[4][3].setStyleSheet("background-color: red")
            return True

        if self.push_list[2][1].text() == self.push_list[3][2].text() \
                and self.push_list[2][1].text() == self.push_list[4][3].text() \
                and self.push_list[2][1].text() == self.push_list[5][4].text() \
                and self.push_list[2][1].text() != "":
            self.push_list[2][1].setStyleSheet("background-color: red")
            self.push_list[3][2].setStyleSheet("background-color: red")
            self.push_list[4][3].setStyleSheet("background-color: red")
            self.push_list[5][4].setStyleSheet("background-color: red")
            return True

        if self.push_list[3][2].text() == self.push_list[4][3].text() \
                and self.push_list[3][2].text() == self.push_list[5][4].text() \
                and self.push_list[3][2].text() == self.push_list[6][5].text() \
                and self.push_list[3][2].text() != "":
            self.push_list[3][2].setStyleSheet("background-color: red")
            self.push_list[4][3].setStyleSheet("background-color: red")
            self.push_list[5][4].setStyleSheet("background-color: red")
            self.push_list[6][5].setStyleSheet("background-color: red")
            return True

        if self.push_list[1][1].text() == self.push_list[2][2].text() \
                and self.push_list[1][1].text() == self.push_list[3][3].text() \
                and self.push_list[1][1].text() == self.push_list[4][4].text() \
                and self.push_list[1][1].text() != "":
            self.push_list[1][1].setStyleSheet("background-color: red")
            self.push_list[2][2].setStyleSheet("background-color: red")
            self.push_list[3][3].setStyleSheet("background-color: red")
            self.push_list[4][4].setStyleSheet("background-color: red")
            return True

        if self.push_list[2][2].text() == self.push_list[3][3].text() \
                and self.push_list[2][2].text() == self.push_list[4][4].text() \
                and self.push_list[2][2].text() == self.push_list[5][5].text() \
                and self.push_list[2][2].text() != "":
            self.push_list[2][2].setStyleSheet("background-color: red")
            self.push_list[3][3].setStyleSheet("background-color: red")
            self.push_list[4][4].setStyleSheet("background-color: red")
            self.push_list[5][5].setStyleSheet("background-color: red")
            return True

        if self.push_list[3][3].text() == self.push_list[4][4].text() \
                and self.push_list[3][3].text() == self.push_list[5][5].text() \
                and self.push_list[3][3].text() == self.push_list[6][6].text() \
                and self.push_list[3][3].text() != "":
            self.push_list[3][3].setStyleSheet("background-color: red")
            self.push_list[4][4].setStyleSheet("background-color: red")
            self.push_list[5][5].setStyleSheet("background-color: red")
            self.push_list[6][6].setStyleSheet("background-color: red")
            return True

        if self.push_list[1][2].text() == self.push_list[2][3].text() \
                and self.push_list[1][2].text() == self.push_list[3][4].text() \
                and self.push_list[1][2].text() == self.push_list[4][5].text() \
                and self.push_list[1][2].text() != "":
            self.push_list[1][2].setStyleSheet("background-color: red")
            self.push_list[2][3].setStyleSheet("background-color: red")
            self.push_list[3][4].setStyleSheet("background-color: red")
            self.push_list[4][5].setStyleSheet("background-color: red")
            return True

        if self.push_list[2][3].text() == self.push_list[3][4].text() \
                and self.push_list[2][3].text() == self.push_list[4][5].text() \
                and self.push_list[2][3].text() == self.push_list[5][6].text() \
                and self.push_list[2][3].text() != "":
            self.push_list[2][3].setStyleSheet("background-color: red")
            self.push_list[3][4].setStyleSheet("background-color: red")
            self.push_list[4][5].setStyleSheet("background-color: red")
            self.push_list[5][6].setStyleSheet("background-color: red")
            return True
        if self.push_list[1][3].text() == self.push_list[2][4].text() \
                and self.push_list[2][3].text() == self.push_list[3][5].text() \
                and self.push_list[2][3].text() == self.push_list[4][6].text() \
                and self.push_list[2][3].text() != "":
            self.push_list[1][3].setStyleSheet("background-color: red")
            self.push_list[2][4].setStyleSheet("background-color: red")
            self.push_list[3][5].setStyleSheet("background-color: red")
            self.push_list[4][6].setStyleSheet("background-color: red")
            return True

        if self.push_list[1][6].text() == self.push_list[2][5].text() \
                and self.push_list[1][6].text() == self.push_list[3][4].text() \
                and self.push_list[1][6].text() == self.push_list[4][3].text() \
                and self.push_list[1][6].text() != "":
            self.push_list[1][6].setStyleSheet("background-color: red")
            self.push_list[2][5].setStyleSheet("background-color: red")
            self.push_list[3][4].setStyleSheet("background-color: red")
            self.push_list[4][3].setStyleSheet("background-color: red")
            return True

        if self.push_list[2][5].text() == self.push_list[3][4].text() \
                and self.push_list[2][5].text() == self.push_list[4][3].text() \
                and self.push_list[2][5].text() == self.push_list[5][2].text() \
                and self.push_list[2][5].text() != "":
            self.push_list[2][5].setStyleSheet("background-color: red")
            self.push_list[3][4].setStyleSheet("background-color: red")
            self.push_list[4][3].setStyleSheet("background-color: red")
            self.push_list[5][2].setStyleSheet("background-color: red")
            return True

        if self.push_list[3][4].text() == self.push_list[4][3].text() \
                and self.push_list[3][4].text() == self.push_list[5][2].text() \
                and self.push_list[3][4].text() == self.push_list[6][1].text() \
                and self.push_list[3][4].text() != "":
            self.push_list[3][4].setStyleSheet("background-color: red")
            self.push_list[4][3].setStyleSheet("background-color: red")
            self.push_list[5][2].setStyleSheet("background-color: red")
            self.push_list[6][1].setStyleSheet("background-color: red")
            return True

        if self.push_list[2][0].text() == self.push_list[3][1].text() \
                and self.push_list[2][0].text() == self.push_list[4][2].text() \
                and self.push_list[2][0].text() == self.push_list[5][3].text() \
                and self.push_list[2][0].text() != "":
            self.push_list[2][0].setStyleSheet("background-color: red")
            self.push_list[3][1].setStyleSheet("background-color: red")
            self.push_list[4][2].setStyleSheet("background-color: red")
            self.push_list[5][3].setStyleSheet("background-color: red")
            return True

        if self.push_list[3][1].text() == self.push_list[4][2].text() \
                and self.push_list[3][1].text() == self.push_list[5][3].text() \
                and self.push_list[3][1].text() == self.push_list[6][4].text() \
                and self.push_list[3][1].text() != "":
            self.push_list[3][1].setStyleSheet("background-color: red")
            self.push_list[4][2].setStyleSheet("background-color: red")
            self.push_list[5][3].setStyleSheet("background-color: red")
            self.push_list[6][4].setStyleSheet("background-color: red")
            return True

        if self.push_list[3][0].text() == self.push_list[4][1].text() \
                and self.push_list[3][0].text() == self.push_list[5][2].text() \
                and self.push_list[3][0].text() == self.push_list[6][3].text() \
                and self.push_list[3][0].text() != "":
            self.push_list[3][0].setStyleSheet("background-color: red")
            self.push_list[4][1].setStyleSheet("background-color: red")
            self.push_list[5][2].setStyleSheet("background-color: red")
            self.push_list[6][3].setStyleSheet("background-color: red")
            return True

        if self.push_list[2][6].text() == self.push_list[3][5].text() \
                and self.push_list[2][6].text() == self.push_list[4][4].text() \
                and self.push_list[2][6].text() == self.push_list[5][3].text() \
                and self.push_list[2][6].text() != "":
            self.push_list[2][6].setStyleSheet("background-color: red")
            self.push_list[3][5].setStyleSheet("background-color: red")
            self.push_list[4][4].setStyleSheet("background-color: red")
            self.push_list[5][3].setStyleSheet("background-color: red")
            return True

        if self.push_list[3][5].text() == self.push_list[4][4].text() \
                and self.push_list[3][5].text() == self.push_list[5][3].text() \
                and self.push_list[3][5].text() == self.push_list[6][2].text() \
                and self.push_list[3][5].text() != "":
            self.push_list[3][5].setStyleSheet("background-color: red")
            self.push_list[4][4].setStyleSheet("background-color: red")
            self.push_list[5][3].setStyleSheet("background-color: red")
            self.push_list[6][2].setStyleSheet("background-color: red")
            return True

        if self.push_list[3][6].text() == self.push_list[4][5].text() \
                and self.push_list[3][6].text() == self.push_list[5][4].text() \
                and self.push_list[3][6].text() == self.push_list[6][3].text() \
                and self.push_list[3][6].text() != "":
            self.push_list[3][6].setStyleSheet("background-color: red")
            self.push_list[4][5].setStyleSheet("background-color: red")
            self.push_list[5][4].setStyleSheet("background-color: red")
            self.push_list[6][3].setStyleSheet("background-color: red")
            return True

        berabere_list = []
        for i in range(7):
            for j in range(7):
                if self.push_list[i][j].text() != "":
                    berabere_list.append(self.push_list[i][j])
        if len(berabere_list) == 49:
            return "0"

        # # if nothing is crossed
        # return False

def run():
    ap = QtWidgets.QApplication(sys.argv)
    win = TICTACTOE()
    win.show()
    sys.exit(ap.exec_())

if __name__ == "__main__":
    run()