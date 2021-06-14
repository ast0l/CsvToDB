# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_csv_to_db.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from csvtodb.Mysql import Mysql
from csvtodb.Laravel import Laravel
from csvtodb.Csv import Csv
import re


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # set main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(637, 479)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        MainWindow.setFont(font)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # title dbsm
        self.title_dbsm = QtWidgets.QLabel(self.centralwidget)
        self.title_dbsm.setGeometry(QtCore.QRect(10, 50, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Amiri")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.title_dbsm.setFont(font)
        self.title_dbsm.setObjectName("title_dbsm")

        # title framework
        self.title_framework = QtWidgets.QLabel(self.centralwidget)
        self.title_framework.setGeometry(QtCore.QRect(10, 200, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Amiri")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.title_framework.setFont(font)
        self.title_framework.setObjectName("title_framework")

        # radio mysql
        self.btn_mysql = QtWidgets.QRadioButton(self.centralwidget)
        self.btn_mysql.setGeometry(QtCore.QRect(10, 90, 82, 17))
        self.btn_mysql.setObjectName("btn_mysql")
        self.btn_mysql.toggled.connect(lambda: self.display_opt(dbsm=True))

        # radio laravel
        self.btn_laravel = QtWidgets.QRadioButton(self.centralwidget)
        self.btn_laravel.setGeometry(QtCore.QRect(10, 250, 82, 17))
        self.btn_laravel.setObjectName("btn_laravel")
        self.btn_laravel.toggled.connect(lambda: self.display_opt(dbsm=False))

        # send btn
        self.send = QtWidgets.QPushButton(self.centralwidget)
        self.send.setGeometry(QtCore.QRect(0, 400, 631, 71))
        self.send.setObjectName("send")
        self.send.clicked.connect(self.generate)

        # select csv btn
        self.btn_select_csv = QtWidgets.QPushButton(self.centralwidget)
        self.btn_select_csv.setGeometry(QtCore.QRect(290, 60, 75, 23))
        self.btn_select_csv.setObjectName("btn_select_csv")
        self.btn_select_csv.clicked.connect(self.browse_file)

        # display csv filepath
        self.csv_filepath_display = QtWidgets.QLineEdit(self.centralwidget)
        self.csv_filepath_display.setEnabled(True)
        self.csv_filepath_display.setGeometry(QtCore.QRect(370, 60, 231, 20))
        self.csv_filepath_display.setText("")
        self.csv_filepath_display.setReadOnly(False)
        self.csv_filepath_display.setObjectName("csv_filepath_display")

        # btn migration file for framework
        self.btn_migration_file = QtWidgets.QPushButton(self.centralwidget)
        self.btn_migration_file.setGeometry(QtCore.QRect(290, 110, 111, 23))
        self.btn_migration_file.setObjectName("btn_migration_file")
        self.btn_migration_file.setVisible(False)
        self.btn_migration_file.clicked.connect(lambda: self.mig_seed_file(type='migration'))

        # btn seeder file for framework
        self.btn_seeder_file = QtWidgets.QPushButton(self.centralwidget)
        self.btn_seeder_file.setGeometry(QtCore.QRect(290, 150, 111, 23))
        self.btn_seeder_file.setObjectName("btn_seeder_file")
        self.btn_seeder_file.setVisible(False)
        self.btn_seeder_file.clicked.connect(lambda: self.mig_seed_file(type='seeder'))

        # select migration seeder for dbsm
        self.select_migration_seeder = QtWidgets.QComboBox(self.centralwidget)
        self.select_migration_seeder.setGeometry(QtCore.QRect(290, 150, 120, 23))
        self.select_migration_seeder.setObjectName("btn_dbsm_migration_seeder")
        self.select_migration_seeder.addItem("")
        self.select_migration_seeder.addItem("")
        self.select_migration_seeder.addItem("")
        self.select_migration_seeder.setVisible(False)

        # display migration filepath for framework
        self.label_migration_file = QtWidgets.QLineEdit(self.centralwidget)
        self.label_migration_file.setGeometry(QtCore.QRect(410, 110, 221, 16))
        self.label_migration_file.setObjectName("label_migration_file")
        self.label_migration_file.setVisible(False)

        # display seeder filepath for framework
        self.label_seeder_file = QtWidgets.QLineEdit(self.centralwidget)
        self.label_seeder_file.setGeometry(QtCore.QRect(410, 150, 221, 16))
        self.label_seeder_file.setObjectName("label_seeder_file")
        self.label_seeder_file.setVisible(False)

        # save in for dbsm
        self.btn_save_dbsm = QtWidgets.QPushButton(self.centralwidget)
        self.btn_save_dbsm.setGeometry(QtCore.QRect(290, 110, 111, 23))
        self.btn_save_dbsm.setObjectName("btn_save_dbsm")
        self.btn_save_dbsm.setVisible(False)
        self.btn_save_dbsm.clicked.connect(self.save_in)

        # label for save in
        self.label_save_in = QtWidgets.QLineEdit(self.centralwidget)
        self.label_save_in.setGeometry(QtCore.QRect(410, 110, 221, 16))
        self.label_save_in.setObjectName("label_migration_file")
        self.label_save_in.setVisible(False)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Csv To DB"))
        self.title_dbsm.setText(_translate("MainWindow", "DBSM"))
        self.title_framework.setText(_translate("MainWindow", "Framework"))
        self.btn_mysql.setText(_translate("MainWindow", "Mysql"))
        self.btn_laravel.setText(_translate("MainWindow", "Laravel"))
        self.send.setText(_translate("MainWindow", "Generate"))
        self.btn_select_csv.setText(_translate("MainWindow", "Select CSV"))
        self.btn_migration_file.setText(_translate("MainWindow", "migration file"))
        self.btn_seeder_file.setText(_translate("MainWindow", "seeder file"))
        self.select_migration_seeder.setItemText(0, _translate("MainWindow", "migration"))
        self.select_migration_seeder.setItemText(1, _translate("MainWindow", "seeder"))
        self.select_migration_seeder.setItemText(2, _translate("MainWindow", "migration + seeder"))
        self.label_migration_file.setText(_translate("MainWindow", ""))
        self.label_seeder_file.setText(_translate("MainWindow", ""))
        self.btn_save_dbsm.setText(_translate("MainWindow", "save in"))
        self.label_save_in.setText(_translate("MainWindow", ""))

    # -------------------------------
    # method for btn
    # -------------------------------

    def browse_file(self):
        """
        open folder dialog menu

        :return:
        """
        file = QtWidgets.QFileDialog.getOpenFileName(caption='Select CSV file', directory='D:\\', filter='*.csv')
        self.csv_filepath_display.setText(file[0])

    def save_in(self):
        """
        save in for dbsm

        :return:
        """
        file = QtWidgets.QFileDialog.getExistingDirectory(caption='Select where to save the file', directory='./')
        self.label_save_in.setVisible(True)
        self.label_save_in.setText(file)

    def display_opt(self, dbsm: bool):
        """
        display info for mysql\n

        mode:
        - dbsm
        - framework

        :return:
        """
        if dbsm:
            self.select_migration_seeder.setVisible(True if self.btn_mysql.isChecked() else False)
            self.btn_save_dbsm.setVisible(True if self.btn_mysql.isChecked() else False)
        else:
            self.btn_seeder_file.setVisible(True if self.btn_laravel.isChecked() else False)
            self.btn_migration_file.setVisible(True if self.btn_laravel.isChecked() else False)

    def mig_seed_file(self, type: str):
        """
        migration or seeder file

        :return:
        """
        file = QtWidgets.QFileDialog.getOpenFileName(caption=f'Select {type} file', directory='D:\\', filter='*.php')
        if type == 'migration':
            self.label_migration_file.setVisible(True)
            self.label_migration_file.setText(file[0])
        else:
            self.label_seeder_file.setVisible(True)
            self.label_seeder_file.setText(file[0])

    def generate(self):
        """
        generate file from the csv

        :return:
        """
        print('yes')
        filename = re.findall(r'[\w-]+\.csv', self.csv_filepath_display.text())
        print('yes2')
        filepath = re.sub(r'[\/\\][\w-]+\.csv', '', self.csv_filepath_display.text(), 0)
        print('yes3')
        for name in filename:
            filename = re.sub(r'\.csv', '', name)
        csv = Csv(filename=filename, filepath=filepath)

        # mysql
        if self.btn_mysql.isChecked():
            if self.label_save_in.text():
                save_in = self.label_save_in.text()
                if self.select_migration_seeder.currentText() == 'migration':
                    Mysql.new_table(csv=csv, filename=filename, filepath=save_in)

                elif self.select_migration_seeder.currentText() == 'seeder':
                    Mysql.new_seeder(csv=csv, filename=filename, filepath=save_in)

                elif self.select_migration_seeder.currentText() == 'migration + seeder':
                    Mysql.new_table(csv=csv, filename=filename, filepath=save_in)
                    Mysql.new_seeder(csv=csv, filename=filename, filepath=save_in)

        # laravel
        elif self.btn_laravel.isChecked():
            filename = re.findall(r'[\w-]+\.php', self.label_migration_file.text())
            filepath = re.sub(r'[\/\\][\w-]+\.php', '', self.label_migration_file.text(), 0)
            for name in filename:
                filename = re.sub(r'\.php', '', name)

            if self.label_migration_file.text():
                print(filename, filepath)
                Laravel.new_migration(csv=csv, filename=filename, filepath=filepath)
            if self.label_seeder_file.text():
                Laravel.new_seeder(csv=csv, filename=filename, filepath=filepath)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
