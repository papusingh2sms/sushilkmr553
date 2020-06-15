from PyQt5 import QtCore, QtGui, QtWidgets
from Dialog_box import Ui_Dialog
from error import Ui_Dialog1
from evaluate import Ui_Dialog2
global em
em=list()
import sqlite3
lib=sqlite3.connect('cricket.db')
cur=lib.cursor()
class database:
    def teams(x):
        cur.execute("select * from teams where Team_name='"+x+"';")
        teams=list()
        players=list()
        for all in cur.fetchall():
            teams.append(all[1])
            players.append(all[2]+'('+str(all[3])+')')
        return teams,players
    def insert_teams(team_name):
        for all in em:
            player=all[:all.find('(')]
            value=int(all[all.find('(')+1:all.find(')')])
            cur.execute("insert into teams(Team_name,Players,Value) VALUES(?,?,?);",(team_name,player,value))
            lib.commit()
class Ui_MainWindow(object):
    def error(self,x):
            Dialog1 = QtWidgets.QDialog()
            ui = Ui_Dialog1()
            ui.setupUi(Dialog1)
            Dialog1.show()
            ui.label.setText(x)
            Dialog1.exec_()
    def button(self,x):
        self.listWidget.clear()
        button=x
        cur.execute("select * from stats where Categories='"+button+"';")
        data=list(cur.fetchall())
        players=list()
        for all in data:
            list_item=all[1]+'('+str(all[6])+')'
            if list_item not in em:
                players.append(list_item)
        self.listWidget.addItems(players)
    def rb1(self):
        self.button(self.radioButton.text())
    def rb2(self):
        self.button(self.radioButton_2.text())
    def rb3(self):
        self.button(self.radioButton_3.text())
    def rb4(self):
        self.button(self.radioButton_4.text())
    def remove(self):
        row=self.listWidget_2.currentRow()
        self.listWidget_2.takeItem(row)
        em.pop(row)
        self.group_label()
    def group_label(self):
        val=list()
        for all in em:
            val.append(int(all[all.find('(')+1:all.find(')')]))
        global s
        s=sum(val)
        self.label_13.setText(str(s))
        self.label_12.setText(str(1000-s))
        for role in ['BAT','BWL','AR','WK']:
            cur.execute("select * from stats where Categories='"+role+"';")
            data=list(cur.fetchall())
            players=list()
            for all in data:
                list_item=all[1]+'('+str(all[6])+')'
                if list_item not in em:
                    players.append(list_item)
            spd=str(len(data)-len(players))
            if role=='BAT':
                self.label_4.setText(spd)
            if role=='BWL':
                self.label_6.setText(spd)
            if role=='AR':
                self.label_8.setText(spd)
            if role=='WK':
                self.label_10.setText(spd)
    def insert(self):
        row=self.listWidget.currentRow()
        self.listWidget_2.clear()
        try:
            em.append(self.listWidget.takeItem(row).text())
        except:
            print('')
        self.listWidget_2.addItems(em)
        self.group_label()
    def double_clicked(self,x):
        item=x.text()
        val=int(item[item.find('(')+1:item.find(')')])
        if val+s<=1000:
            if self.label_10.text()=='1' and item in ['UMESH(110)','BUMRAH(60)']:
                self.error('You can\'t select more than one wicket-keeper')
            else:
                self.insert()
        else:
            self.error('You Can\'t Add More Players')
    def save(self):
        if self.label_15.text()=='':
                self.error('Team Name Is Blank')
        else:
            if len(em)<10:
                self.error('Team is not complete')
            else:
                try:
                    database.insert_teams(self.label_15.text())
                    Dialog1 = QtWidgets.QDialog()
                    ui = Ui_Dialog1()
                    ui.setupUi(Dialog1)
                    Dialog1.show()
                    Dialog1.setWindowTitle("saved")
                    ui.label.setText('Team Saved')
                    Dialog1.exec_()
                    em.clear()
                    self.listWidget_2.clear()
                    self.listWidget.clear()
                except:
                    self.error('Team not saved')
    def open(self):
        while True:
            Dialog = QtWidgets.QDialog()
            ui = Ui_Dialog()
            ui.setupUi(Dialog)
            Dialog.setWindowTitle("open")
            y=Dialog.exec()
            if ui.lineEdit.text()=="":
                if y==QtWidgets.QDialog.Rejected:
                    break
                self.error('ERROR !! \nTeam column should not be blank')
            else:
                teams,players=database.teams(ui.lineEdit.text().upper())
                if ui.lineEdit.text().upper() not in teams:
                    self.error('This Team Is Not There \n Create A New Team')
                else:
                    for all in players:
                        em.append(all)
                    self.listWidget_2.addItems(em)
                    self.radioButton.show()
                    self.radioButton_2.show()
                    self.radioButton_3.show()
                    self.radioButton_4.show()
                    self.label_15.setText(ui.lineEdit.text().upper())
                    self.rb4()
                    self.rb2()
                    self.rb3()
                    self.rb1()
                    self.insert()
                    cur.execute("delete from teams where Team_name='"+ui.lineEdit.text().upper()+"';")
                    lib.commit()
                    break
    def new(self):
        while True:
            Dialog = QtWidgets.QDialog()
            ui = Ui_Dialog()
            ui.setupUi(Dialog)
            y=Dialog.exec()
            if ui.lineEdit.text()=="":
                if y==QtWidgets.QDialog.Rejected:
                    break
                self.error('ERROR !! \nTeam column should not be blank')
            else:
                teams,players=database.teams(ui.lineEdit.text().upper())
                if ui.lineEdit.text().upper() in teams:
                    self.error('This Name Is Already Taken')
                else:
                    self.radioButton.show()
                    self.radioButton_2.show()
                    self.radioButton_3.show()
                    self.radioButton_4.show()
                    self.label_15.setText(ui.lineEdit.text().upper())
                    self.insert()
                    break
    def Evaluate(self):
        cur.execute("select * from teams")
        teams=list()
        for all in cur.fetchall():
            teams.append(all[1])
        saved_teams=list(dict.fromkeys(teams))
        cur.execute("SELECT * FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
        tables=list()
        for all in list(cur.fetchall()):
            tables.append(all[1])
        tables.remove('stats')
        tables.remove('teams')
        tables.remove('Rank')
        Dialog2 = QtWidgets.QDialog()
        ui = Ui_Dialog2()
        ui.setupUi(Dialog2)
        Dialog2.show()
        ui.comboBox.addItems(saved_teams)
        ui.comboBox_2.addItems(tables)
        Dialog2.exec()
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 850)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 800))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(25, 30, 950, 80))
        self.groupBox.setStyleSheet("QPushButton { background-color: white }")
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox.setObjectName("groupBox")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 30, 151, 21))
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(170, 30, 41, 21))
        font = QtGui.QFont()
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("QLabel { color: blue }\n"
"rgb(0, 0, 255)")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(230, 30, 151, 21))
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(390, 30, 41, 21))
        font = QtGui.QFont()
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("QLabel { color: blue }\n"
"rgb(0, 0, 255)")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(450, 30, 171, 21))
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(630, 30, 41, 21))
        font = QtGui.QFont()
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("QLabel { color: blue }\n"
"rgb(0, 0, 255)")
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(690, 30, 201, 21))
        self.label_9.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(900, 30, 41, 21))
        font = QtGui.QFont()
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("QLabel { color: blue }\n"
"rgb(0, 0, 255)")
        self.label_10.setObjectName("label_10")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(71, 210, 398, 500))
        self.listWidget.itemDoubleClicked['QListWidgetItem*'].connect(self.double_clicked)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setItalic(True)
        self.listWidget.isSortingEnabled()
        self.listWidget.setFont(font)
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.listWidget.setObjectName("listWidget")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(71, 160, 398, 41))
        self.groupBox_2.setStyleSheet("")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton.setGeometry(QtCore.QRect(50, 5, 91, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.clicked.connect(self.rb1)
        self.radioButton.hide()
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_2.setGeometry(QtCore.QRect(140, 5, 81, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.clicked.connect(self.rb2)
        self.radioButton_2.hide()
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_3.setGeometry(QtCore.QRect(230, 5, 81, 20))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_3.clicked.connect(self.rb3)
        self.radioButton_3.hide()
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_4.setGeometry(QtCore.QRect(320, 5, 81, 20))
        self.radioButton_4.setCheckable(True)
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_4.clicked.connect(self.rb4)
        self.radioButton_4.hide()
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(71, 130, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Kalam")
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(260, 130, 61, 21))
        font = QtGui.QFont()
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("QLabel { color: blue }\n"
"rgb(0, 0, 255)")
        self.label_12.setObjectName("label_12")
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(530, 210, 398, 500))
        self.listWidget_2.itemDoubleClicked['QListWidgetItem*'].connect(self.remove)
        font = QtGui.QFont()
        font.setFamily("Kalam")
        font.setPointSize(12)
        self.listWidget_2.setFont(font)
        self.listWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.addItems(em)
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(670, 130, 61, 21))
        font = QtGui.QFont()
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("QLabel { color: blue }\n"
"rgb(0, 0, 255)")
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(530, 130, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Kalam")
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(670, 180, 111, 21))
        font = QtGui.QFont()
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("QLabel { color: blue }\n"
"rgb(0, 0, 255)")
        self.label_15.setText("")
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(530, 180, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(800, 720, 181, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        font = QtGui.QFont()
        font.setPointSize(20)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 18))
        self.menubar.setObjectName("menubar")
        self.menuManage_Teams = QtWidgets.QMenu(self.menubar)
        self.menuManage_Teams.setObjectName("menuManage_Teams")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_Team = QtWidgets.QAction(MainWindow)
        self.actionNew_Team.setObjectName("actionNew_Team")
        self.actionNew_Team.triggered.connect(self.new)
        self.actionOpen_Team = QtWidgets.QAction(MainWindow)
        self.actionOpen_Team.setObjectName("actionOpen_Team")
        self.actionOpen_Team.triggered.connect(self.open)
        self.actionSAVE_Team = QtWidgets.QAction(MainWindow)
        self.actionSAVE_Team.setObjectName("actionSAVE_Team")
        self.actionSAVE_Team.triggered.connect(self.save)
        self.actionEvaluate_Team = QtWidgets.QAction(MainWindow)
        self.actionEvaluate_Team.setObjectName("actionEvaluate_Team")
        self.actionEvaluate_Team.triggered.connect(self.Evaluate)
        self.menuManage_Teams.addSeparator()
        self.menuManage_Teams.addAction(self.actionNew_Team)
        self.menuManage_Teams.addAction(self.actionOpen_Team)
        self.menuManage_Teams.addAction(self.actionSAVE_Team)
        self.menuManage_Teams.addAction(self.actionEvaluate_Team)
        self.menubar.addAction(self.menuManage_Teams.menuAction())

        self.retranslateUi(MainWindow)
        self.radioButton_2.clicked.connect(self.listWidget.show)
        self.radioButton_3.clicked.connect(self.listWidget.show)
        self.radioButton_4.clicked.connect(self.listWidget.show)
        self.radioButton.clicked.connect(self.listWidget.show)
        self.pushButton.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Cricket"))
        self.groupBox.setTitle(_translate("MainWindow", "Your selections"))
        self.label_3.setText(_translate("MainWindow", "Batsmen (BAT)  :"))
        self.label_4.setText(_translate("MainWindow", "00"))
        self.label_5.setText(_translate("MainWindow", "Bowlers (BWL)  :"))
        self.label_6.setText(_translate("MainWindow", "00"))
        self.label_7.setText(_translate("MainWindow", "Allrounders (AR)  :"))
        self.label_8.setText(_translate("MainWindow", "00"))
        self.label_9.setText(_translate("MainWindow", "Wicket-keepers (WK)  :"))
        self.label_10.setText(_translate("MainWindow", "00"))
        self.radioButton.setText(_translate("MainWindow", "BAT"))
        self.radioButton_2.setText(_translate("MainWindow", "BWL"))
        self.radioButton_3.setText(_translate("MainWindow", "AR"))
        self.radioButton_4.setText(_translate("MainWindow", "WK"))
        self.label_11.setText(_translate("MainWindow", "Points Available"))
        self.label_12.setText(_translate("MainWindow", "1000"))
        self.label_13.setText(_translate("MainWindow", "00"))
        self.label_14.setText(_translate("MainWindow", "Points Used"))
        self.label_16.setText(_translate("MainWindow", "Team Name  :"))
        self.pushButton.setText(_translate("MainWindow", "Quit Game"))
        self.pushButton.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.menuManage_Teams.setTitle(_translate("MainWindow", "Manage Teams"))
        self.actionNew_Team.setText(_translate("MainWindow", "New Team"))
        self.actionNew_Team.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionOpen_Team.setText(_translate("MainWindow", "OPEN Team"))
        self.actionOpen_Team.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSAVE_Team.setText(_translate("MainWindow", "SAVE Team"))
        self.actionSAVE_Team.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionEvaluate_Team.setText(_translate("MainWindow", "Evaluate Team"))
        self.actionEvaluate_Team.setShortcut(_translate("MainWindow", "Ctrl+E"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
