#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# inheriting branch

from PyQt5 import QtWidgets, QtCore, QtGui, QtSql
import sys, sqlite3, random, os, time, datetime
from utils.handleSql import HandleSql
from views.mymodels import MyModels
from views.locapphandler import LocAppHandler
from views.myphotos import MyPhotos
from views.mysessions import MySessions


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.version = '''1'''
        QtWidgets.QMainWindow.__init__(self, parent)
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        # self.wp = os.path.join(self.app_dir, 'images')
        # ico_path = os.path.join(self.wp, 'dic.png')
        # ico = QtGui.QIcon(ico_path)
        # self.setWindowIcon(ico)
        # self.view = MyView(self.app_dir)
        self.view = CentralWidget(self.app_dir)
        self.setCentralWidget(self.view)
        menuBar = self.menuBar()
        myNotes = menuBar.addMenu('&Notes')
        # action = myNotes.addAction('Add Model')
        action = myNotes.addAction('Add Application', self.view.addLocApp)
        action = myNotes.addAction('Add Location', lambda x="Location": self.view.addLocApp(x))
        # action = myNotes.addAction('Add Photo')
        #action = myMenu.addAction('Test',  self.test)
        myEdit = menuBar.addMenu('&Edit notes')
        action = myEdit.addAction('Delete application')
        action = myEdit.addAction('Delete Location')
        action = myEdit.addAction('Change Application')
        action = myEdit.addAction('Change Location')
        myAbout = menuBar.addMenu('О...')
        action = myAbout.addAction('О программе') #, self.aboutProgramm)
        action = myAbout.addAction('Обо мне') #, self.aboutMe)
        self.statusBar = self.statusBar()
        self.view.btn_close.clicked.connect(self.close)

    def closeEvent(self, e):
        e.accept()
        QtWidgets.QWidget.closeEvent(self, e)


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, root_path, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.root_path = root_path
        self.database = os.path.join(self.root_path, 'bases/models.sqlite')
        self.handlersql = HandleSql()
        self.models = []
        self.names = []
        if not os.path.exists("bases/models.sqlite"):
            print("Not database")
            self.createDataBase()
        else:
            print("There is database")
        self.makeWidget()

    def createDataBase(self):
        conn, query = self.handlersql.connectBase(self.database)
        if 'Models' not in conn.tables():
            querystr1 = '''create table Models (id integer primary key autoincrement,
            name text, origin text, ed_work text)'''
            query.exec(querystr1)
            query.clear()
        if 'Application' not in conn.tables():
            querystr2 = """create table Application (id integer primary key autoincrement,
            name text)"""
            query.exec(querystr2)
            query.clear()
            query.prepare("insert into Application values (null, ?)")
            query.addBindValue('any')
            query.exec_()
            query.clear()
        if 'Location' not in conn.tables():
            querystr3 = """create table Location (id integer primary key autoincrement,
            name text)"""
            query.exec(querystr3)
            query.clear()
            query.prepare("insert into Location values (null, ?)")
            query.addBindValue('any')
            query.exec_()
            query.clear()
        if 'Photos' not in conn.tables():
            querystr4 = """create table Photos (id integer primary key autoincrement,
            name text, model_id integer, application_id integer, location_id integer, publish_data text)"""
            query.exec(querystr4)
            query.clear()
        if 'Sessions' not in conn.tables():
            querystr5 = """create table Sessions (id integer primary key autoincrement,
            model_id integer, location_desc text, equipment text, session_date text)"""
            query.exec(querystr5)
            query.clear()
        if 'Contacts' not in conn.tables():
            querystr6 = '''create table Contacts (id integer primary key autoincrement,
            model_id integer, phone text, email text, ref_s text)'''
            query.exec(querystr6)
            query.clear()
        conn.close()

    def makeWidget(self):
        self.main_box = QtWidgets.QVBoxLayout()
        self.vbox = QtWidgets.QVBoxLayout()
        self.bottom_box = QtWidgets.QHBoxLayout()
        self.viewWidget = MyModels(self.database, self.handlersql) #MyView(self.database, self.handlersql)
        self.setControlButtons()
        # self.vbox.addWidget(self.viewWidget)
        # self.main_box.addLayout(self.vbox)
        self.main_box.addWidget(self.viewWidget)
        self.main_box.addLayout(self.bottom_box)
        self.setLayout(self.main_box)
        self.models = self.viewWidget.modelslist
        self.names = self.viewWidget.modelnames

    def setControlButtons(self):
        for i, f in (('Models', self.viewModels), ('Photos', self.viewPhotos), ('Sessions', self.viewSessions)):
            btn = QtWidgets.QPushButton(i)
            btn.clicked.connect(f)
            self.bottom_box.addWidget(btn)
        self.btn_close = QtWidgets.QPushButton('Close')
        self.bottom_box.addWidget(self.btn_close)

    def clearVBox(self):
        wt = self.main_box.itemAt(0).widget()
        wt.setParent(None)
        wt.deleteLater()
        # for i in reversed(range(self.vbox.count())):
        #     wt = self.vbox.itemAt(i).widget()
        #     print("wt: ", wt)
        #     wt.setParent(None)
        #     wt.deleteLater()

    def viewModels(self):
        print("viewModels")
        if self.viewWidget.__class__.__name__ == "MyView":
            print("In MyView")
        else:
            self.clearVBox()
            self.viewWidget = MyModels(self.database, self.handlersql) #MyView(self.database, self.handlersql)
            self.main_box.insertWidget(0, self.viewWidget)

    def viewPhotos(self):
        print("viewPhotos")
        if self.viewWidget.__class__.__name__ == "MyPhotos":
            print("In MyPhotos")
        else:
            self.clearVBox()
            self.viewWidget = MyPhotos(self.database, self.handlersql, self.models, self.names)
            self.main_box.insertWidget(0, self.viewWidget)

    def viewSessions(self):
        print("viewSessions")
        if self.viewWidget.__class__.__name__ == "MySessions":
            print("In MySessions")
        else:
            self.clearVBox()
            self.viewWidget = MySessions(self.database, self.handlersql, self.models, self.names)
            self.main_box.insertWidget(0, self.viewWidget)

    def addLocApp(self, alias="Application"):
        print("addLocApp")
        if self.viewWidget.__class__.__name__ == "LocAppHandler" and self.viewWidget.alias == alias:
                print("from widget", self.viewWidget.alias)
                print("here", alias)
                print("In LocAppHandler")
        else:
            self.clearVBox()
            self.viewWidget = LocAppHandler(self.database, self.handlersql, alias)
            self.main_box.insertWidget(0, self.viewWidget)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Modelslist')
    window.resize(1100, 400)
    desktop = QtWidgets.QApplication.desktop()
    x = (desktop.width() // 2) - window.width()
    window.move(x, 250)
    window.show()
    sys.exit(app.exec_())
