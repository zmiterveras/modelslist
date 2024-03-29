#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from PyQt5 import QtWidgets, QtCore
from utils.handleSql import HandleSql
from utils.searcher import SearcherController
from views.locapphandler import LocAppHandler
from views.mymodels import MyModels
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
        menuBar = self.menuBar()
        myNotes = menuBar.addMenu('&Notes')
        mySearch = menuBar.addMenu("Поиск")
        # action = myNotes.addAction('Add Model')
        self.view = CentralWidget(self.app_dir, mySearch)
        self.setCentralWidget(self.view)
        action = myNotes.addAction('Models', self.view.viewModels)
        action = myNotes.addAction('Photos', self.view.viewPhotos)
        action = myNotes.addAction('Sessions', self.view.viewSessions)
        action = myNotes.addAction('Change Application', self.view.addLocApp)
        action = myNotes.addAction('Change Location', lambda x="Location": self.view.addLocApp(x))
        # action = myNotes.addAction('Add Photo')
        #action = myMenu.addAction('Test',  self.test)
        # myEdit = menuBar.addMenu('&Edit notes')
        # action = myEdit.addAction('Delete application')
        # action = myEdit.addAction('Delete Location')
        # action = myEdit.addAction('Change Application')
        # action = myEdit.addAction('Change Location')
        myAbout = menuBar.addMenu('О...')
        action = myAbout.addAction('О программе', self.aboutProgramm)
        action = myAbout.addAction('Обо мне', self.aboutMe)

        self.statusBar = self.statusBar()
        self.view.btn_close.clicked.connect(self.close)

    def aboutProgramm(self):
        ab = QtWidgets.QWidget(parent=self, flags=QtCore.Qt.Window)
        ab.setWindowTitle('О программе')
        ab.setWindowModality(QtCore.Qt.WindowModal)
        ab.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        abbox = QtWidgets.QVBoxLayout()
        text = '''
                Эта программа поможет фотографу\n
                ситематизировать данные о моделях,\n
                фотосессиях, фотографиях и местах\n
                и времени их публикации.\n
                Версия: ''' + self.version + '\n'

        abl = QtWidgets.QLabel(text)
        abl.setAlignment(QtCore.Qt.AlignCenter)
        abb = QtWidgets.QPushButton('Close')
        abb.clicked.connect(ab.close)
        abbox.addWidget(abl)
        abbox.addWidget(abb)
        ab.setLayout(abbox)
        ab.show()

    def aboutMe(self):
        text = '''Автор: @zmv\nОбратная связь: zmvph79@gmail.com'''
        QtWidgets.QMessageBox.information(None, 'Об авторе', text)

    def closeEvent(self, e):
        e.accept()
        QtWidgets.QWidget.closeEvent(self, e)


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, root_path, menu, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.root_path = root_path
        self.menu = menu
        self.database = os.path.join(self.root_path, 'bases/models.sqlite')
        self.handlersql = HandleSql()
        self.models = []
        if not os.path.exists("bases/models.sqlite"):
            print("Not database")
            self.createDataBase()
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
            name text, model_id integer, application_id integer, location_id integer, publish_data text, notes text)"""
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
        """
        default make MyModels
        """
        self.main_box = QtWidgets.QVBoxLayout()
        self.vbox = QtWidgets.QVBoxLayout() # не нужен?
        self.bottom_box = QtWidgets.QHBoxLayout()
        self.viewWidget = MyModels(self.database, self.handlersql) #MyView(self.database, self.handlersql)
        self.setControlButtons()
        self.main_box.addWidget(self.viewWidget)
        self.main_box.addLayout(self.bottom_box)
        self.setLayout(self.main_box)
        self.setSearchModelMenu()

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
        self.searchFlag = False

    def setSearchModelMenu(self):
        self.menu.clear()
        self.menu.addAction('Model', lambda p="m.name", w="Models name": self.mySearch(p, w))
        self.menu.addAction('From', lambda p="m.origin", w="From": self.mySearch(p, w))

    def setSearchPhotoMenu(self):
        self.menu.clear()
        self.menu.addAction('Photo', lambda p="p.name", w="Photos name": self.mySearch(p, w))
        self.menu.addAction('Model',
                            lambda p="m.name",
                                   w="Models name": self.mySearch(p, w,[i[1] for i in self.models],
                                                                  extend=["", "Application", "Location", "Date"],
                                                                  date_col='p.publish_data'))
        self.menu.addAction('Application', lambda p="a.name", w="Applications name": self.mySearch(p, w,
                                                                [i[1] for i in self.viewWidget.app_list],
                                                                extend=["", "Location", "Date"],
                                                                date_col='p.publish_data'))
        self.menu.addAction('Location', lambda p="l.name", w="Locations name": self.mySearch(p, w,
                                                                [i[1] for i in self.viewWidget.loc_list],
                                                                extend=["", "Application", "Date"],
                                                                date_col='p.publish_data'))
        self.menu.addAction('Date', lambda p="p.publish_data", w="Date": self.mySearch(p, w,
                                                                    extend=["", "Application", "Location"],
                                                                    date=True))

    def setSearchSessionMenu(self):
        self.menu.clear()
        self.menu.addAction('Model', lambda p="m.name", w="Models name": self.mySearch(p, w,
                                                                [i[1] for i in self.models],
                                                                extend=["", "Date"],
                                                                date_col='s.session_date'))
        self.menu.addAction('Date', lambda p="s.session_date", w="Date": self.mySearch(p, w, date=True))

    def viewModels(self):
        print("viewModels")
        if self.viewWidget.__class__.__name__ == "MyModels" and not self.viewWidget.search_flag:
            print("In MyModels")
        else:
            self.clearVBox()
            self.viewWidget = MyModels(self.database, self.handlersql)
            self.main_box.insertWidget(0, self.viewWidget)
            self.setSearchModelMenu()

    def viewPhotos(self):
        print("viewPhotos")
        if self.viewWidget.__class__.__name__ == "MyPhotos" and not self.viewWidget.search_flag:
            print("In MyPhotos")
        else:
            if self.viewWidget.__class__.__name__ == "MyModels":
                self.models = sorted(self.viewWidget.modelslist, key=lambda x: x[1])
            self.clearVBox()
            self.viewWidget = MyPhotos(self.database, self.handlersql, self.models)
            self.main_box.insertWidget(0, self.viewWidget)
            self.setSearchPhotoMenu()

    def viewSessions(self):
        print("viewSessions")
        if self.viewWidget.__class__.__name__ == "MySessions" and not self.viewWidget.search_flag:
            print("In MySessions")
        else:
            if self.viewWidget.__class__.__name__ == "MyModels":
                self.models = sorted(self.viewWidget.modelslist, key=lambda x: x[1])
            self.clearVBox()
            self.viewWidget = MySessions(self.database, self.handlersql, self.models)
            self.main_box.insertWidget(0, self.viewWidget)
            self.setSearchSessionMenu()

    def addLocApp(self, alias="Application"):
        print("addLocApp")
        if self.viewWidget.__class__.__name__ == "LocAppHandler" and self.viewWidget.alias == alias:
                print("from widget", self.viewWidget.alias)
                print("here", alias)
                print("In LocAppHandler")
        else:
            if self.viewWidget.__class__.__name__ == "MyModels":
                self.models = self.viewWidget.modelslist
            self.clearVBox()
            self.viewWidget = LocAppHandler(self.database, self.handlersql, alias)
            self.main_box.insertWidget(0, self.viewWidget)

    def mySearch(self, param, what, names=[], date=False, extend=[], date_col=''):
        '''
        :param param: таблица и столбец для поиска tablename.columnname
        :param what: строка с описанием искомого Models name
        :param names: список строк имен моделей, приложений или локаций
        :param date: буллевскаая переменная о наличии поиска по дате?
        :param extend: список полей для расширеного поиска
        :param date_col: имя поля даты для расширеного поиска
        :return: создает TopLevel с виджетами для организации поиска
        '''
        self.viewWidget.search_flag = True
        searcher = SearcherController(self.viewWidget, param, what, names, date, extend, date_col)
        searcher.searcherWindow()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Modelslist')
    window.resize(1150, 400)
    desktop = QtWidgets.QApplication.desktop()
    x = (desktop.width() // 2) - window.width()
    window.move(x, 250)
    window.show()
    sys.exit(app.exec_())
