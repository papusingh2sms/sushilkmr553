from PyQt5 import QtCore, QtGui, QtWidgets
from error import Ui_Dialog1
import sqlite3
lib=sqlite3.connect('cricket.db')
cur=lib.cursor()
class Ui_Dialog2(object):
    def error(self,x,y):
            Dialog1 = QtWidgets.QDialog()
            ui = Ui_Dialog1()
            ui.setupUi(Dialog1)
            Dialog1.setWindowTitle(x)
            Dialog1.show()
            ui.label.setText(y)
            Dialog1.exec_()
    def Players(self):
        self.listWidget.clear()
        team=self.comboBox.currentText ()
        cur.execute("select * from teams where Team_name='"+team+"';")
        player=list()
        for all in cur.fetchall():
            player.append(all[2])
        self.listWidget.addItems(player)
        return player
    def button_clicked(self):
        match=self.comboBox_2.currentText ()
        self.listWidget_2.clear()
        player=self.Players()
        player_score=list()
        for all in player:
            if match=='':
                break
            cur.execute("select * from "+match+" where Player='"+all+"';")
            pts1=list(cur.fetchone())
            try:
                score=((pts1[2])/2)+pts1[4]+2*pts1[5]
                if pts1[2]>=50:
                    score=score+5
                if pts1[2]>=100:
                    score=score+10
                if pts1[3]>0:
                    strike_rate=(pts1[2]/pts1[3])*100
                    if 80<=strike_rate<=100:
                        score=score+2
                    if strike_rate>=100:
                        score=score+4
                if pts1[9]>0:
                    score=score+10*pts1[9]
                if pts1[9]>=3:
                    score=score+5
                    if pts1[9]>=5:
                        score=score+5
                if pts1[10]>0:
                    score=score+10*pts1[10]
                if pts1[11]>0:
                    score=score+10*pts1[11]
                if pts1[12]>0:
                    score=score+10*pts1[12]
                if pts1[6]>0:
                    economy_rate=pts1[8]/(pts1[6]/6)
                    if 3.5<=economy_rate<=4.5:
                        score=score+4
                    if 2<=economy_rate<=3.5:
                        score=score+7
                    if economy_rate<=2:
                        score=score+10
                player_score.append(score)
                self.listWidget_2.addItem(str(score))
            except:
                self.listWidget_2.addItem('error')
        self.label_4.setText(str(sum(player_score)))
        self.ranking()
    def ranking(self):
        if self.comboBox.currentText ()=='' or self.comboBox_2.currentText ()=='':
            self.error('error','error')
        else:
            try:
                cur.execute("insert into Rank(Team_name,Matches,Points) VALUES(?,?,?);",(self.comboBox.currentText (),self.comboBox_2.currentText (),self.label_4.text()))
                lib.commit()
                cur.execute("select * from Rank order by Points DESC")
                sorting=list()
                for all in cur.fetchall():
                    sorting.append(all[2])
                Rank=sorting.index(float(self.label_4.text()))+1
                congo='You Have Secured Rank '+str(Rank)+' In This Match'
                self.error('CONGRATS',congo)
            except:
                print("")
    def setupUi(self, Dialog2):
        Dialog2.setObjectName("Dialog2")
        Dialog2.resize(1000, 800)
        self.centralwidget = QtWidgets.QWidget(Dialog2)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(Dialog2)
        self.label.setGeometry(QtCore.QRect(0, 0, 1000, 50))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(Dialog2)
        self.comboBox.setGeometry(QtCore.QRect(200, 70, 200, 30))
        self.comboBox.setIconSize(QtCore.QSize(20, 20))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(Dialog2)
        self.comboBox_2.setGeometry(QtCore.QRect(600, 70, 200, 30))
        self.comboBox_2.setIconSize(QtCore.QSize(20, 20))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.line = QtWidgets.QFrame(Dialog2)
        self.line.setGeometry(QtCore.QRect(100, 150, 800, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(200,240,250,400))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setItalic(True)
        self.listWidget.setFont(font)
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.listWidget.setObjectName("listWidget")
        self.label_2 = QtWidgets.QLabel(Dialog2)
        self.label_2.setGeometry(QtCore.QRect(200, 200, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog2)
        self.label_3.setGeometry(QtCore.QRect(550, 200, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog2)
        self.label_4.setGeometry(QtCore.QRect(650, 200, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("QLabel { color: rgb(0, 85, 255)}")
        self.label_4.setObjectName("label_4")
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(550, 240, 250,400))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.listWidget_2.setFont(font)
        self.listWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidget_2.setObjectName("listWidget_2")
        self.pushButton = QtWidgets.QPushButton(Dialog2)
        self.pushButton.setGeometry(QtCore.QRect(450, 700, 100, 40))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.button_clicked)

        self.retranslateUi(Dialog2)
        self.comboBox.activated['QString'].connect(self.Players)
        QtCore.QMetaObject.connectSlotsByName(Dialog2)

    def retranslateUi(self, Dialog2):
        _translate = QtCore.QCoreApplication.translate
        Dialog2.setWindowTitle(_translate("Dialog2", "Dialog"))
        self.label.setText(_translate("Dialog2", "Evaluate the performance of you fantasy game"))
        self.label_2.setText(_translate("Dialog2", "Players"))
        self.label_3.setText(_translate("Dialog2", "Points    :"))
        self.label_4.setText(_translate("Dialog2", "0"))
        self.pushButton.setText(_translate("Dialog2", "Evaluate"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog2 = QtWidgets.QDialog()
    ui = Ui_Dialog2()
    ui.setupUi(Dialog2)
    Dialog2.show()
    sys.exit(app.exec_())
