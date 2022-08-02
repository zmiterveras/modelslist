#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui, QtSql
import sys, sqlite3, random, os, time


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.version = '''1'''
        QtWidgets.QMainWindow.__init__(self, parent)
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        # self.wp = os.path.join(self.app_dir, 'images')
        # ico_path = os.path.join(self.wp, 'dic.png')
        # ico = QtGui.QIcon(ico_path)
        # self.setWindowIcon(ico)
        ss = QtWidgets.QWidget()
        self.setCentralWidget(ss)
        menuBar = self.menuBar()
        myNotes = menuBar.addMenu('&Notes')
        action = myNotes.addAction('Add Model')
        action = myNotes.addAction('Add Application')
        action = myNotes.addAction('Add Location')
        action = myNotes.addAction('Add Photo')
        #action = myMenu.addAction('Test',  self.test)
        myEdit = menuBar.addMenu('&Edit notes')
        action = myEdit.addAction('Delete model')
        action = myEdit.addAction('Delete photo')
        action = myEdit.addAction('Change photo')
        action = myEdit.addAction('Change model')
        myAbout = menuBar.addMenu('О...')
        action = myAbout.addAction('О программе') #, self.aboutProgramm)
        action = myAbout.addAction('Обо мне') #, self.aboutMe)
        self.statusBar = self.statusBar()

    def createDataBase(self):
        conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        newdic = os.path.join(self.app_dir, 'models.sqlite')
        conn.setDatabaseName(newdic)
        conn.open()
        query = QtSql.QSqlQuery()
        if 'Models' not in conn.tables():
            querystr1 = '''create table Models (id integer primary key autoincrement,
            name text, from text, ed_work text)'''
            query.exec(querystr1)
            query.clear()
        if 'Application' not in conn.tables():
            querystr2 = """create table Application (id integer primary key autoincrement,
            name text)"""
            query.exec(querystr2)
            query.clear()
        if 'Location' not in conn.tables():
            querystr3 = """create table Location (id integer primary key autoincrement,
            name text)"""
            query.exec(querystr3)
            query.clear()
        if 'Location' not in conn.tables():
            querystr3 = """create table Location (id integer primary key autoincrement,
            name text)"""
            query.exec(querystr3)
            query.clear()
        if 'Photos' not in conn.tables():
            querystr4 = """create table Photos (id integer primary key autoincrement,
            name text, model_id integer, application_id integer, location_id integer, publish_data text)"""
            query.exec(querystr4)
            query.clear()
        if 'Sessions' not in conn.tables():
            querystr4 = """create table Sessions (id integer primary key autoincrement,
            model_id integer, location text, equipment text, session_date text)"""
            query.exec(querystr4)
            query.clear()

        conn.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Modelslist')
    window.resize(550, 200)
    desktop = QtWidgets.QApplication.desktop()
    x = (desktop.width() // 2) - window.width()
    window.move(x, 250)
    window.show()
    sys.exit(app.exec_())
