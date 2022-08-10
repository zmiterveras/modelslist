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
        self.view = MyView(self.app_dir)
        self.setCentralWidget(self.view)
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


def connectBase(basename):
    conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    conn.setDatabaseName(basename)
    conn.open()
    return conn


class MyView(QtWidgets.QWidget):
    def __init__(self, root_path, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.root_path = root_path
        self.database = os.path.join(self.root_path, 'bases/models.sqlite')
        self.modelslist = []
        self.modelnames = []
        self.newmodel = []
        if not os.path.exists("bases/models.sqlite"):
            print("Not database")
            self.createDataBase()
        else:

            print("There is database")
        self.makeWidget()

    def createDataBase(self):
        # conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        # conn.setDatabaseName(self.database)
        # conn.open()
        conn = connectBase(self.database)
        query = QtSql.QSqlQuery()
        if 'Models' not in conn.tables():
            querystr1 = '''create table Models (id integer primary key autoincrement,
            name text, origin text, ed_work text)'''
            query.exec(querystr1)
            query.clear()
            # for i in range(1):
            #     query.exec("insert into Models (id, name, origin, ed_work) values (null, 'name', 'city', 'job')")
            #     query.clear()
        if 'Application' not in conn.tables():
            querystr2 = """create table Application (id integer primary key autoincrement,
            name text)"""
            query.exec(querystr2)
            query.clear()
            query.exec("insert into Application (id, name) values (null, 'any')")
            query.clear()
        if 'Location' not in conn.tables():
            querystr3 = """create table Location (id integer primary key autoincrement,
            name text)"""
            query.exec(querystr3)
            query.clear()
            query.exec("insert into Location (id, name) values (null, 'any')")
            query.clear()
        if 'Photos' not in conn.tables():
            querystr4 = """create table Photos (id integer primary key autoincrement,
            name text, model_id integer, application_id integer, location_id integer, publish_data text)"""
            query.exec(querystr4)
            query.clear()
        if 'Sessions' not in conn.tables():
            querystr4 = """create table Sessions (id integer primary key autoincrement,
            model_id integer, location_desc text, equipment text, session_date text)"""
            query.exec(querystr4)
            query.clear()
        if 'Contacts' not in conn.tables():
            querystr5 = """create table Contacts (id integer primary key autoincrement,
            model_id integer, phone text, email text, references text)"""
            query.exec(querystr5)
        conn.close()

    def makeWidget(self):
        self.main_box = QtWidgets.QVBoxLayout()
        self.top_box = QtWidgets.QVBoxLayout()
        self.bottom_box = QtWidgets.QHBoxLayout()
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.top_box.addLayout(self.vbox)
        self.top_box.addLayout(self.hbox)
        self.main_box.addLayout(self.top_box)
        self.main_box.addLayout(self.bottom_box)
        self.setLayout(self.main_box)
        if self.checkModelsList():
            self.setModelListView()
        else:
            label = QtWidgets.QLabel('Models List is empty')
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.vbox.addWidget(label)
            self.setModelsEditButton()

    def clear(self):
        for i in reversed(range(self.vbox.count())):
            wt = self.vbox.itemAt(i).widget()
            wt.setParent(None)
            wt.deleteLater()
        for i in reversed(range(self.hbox.count())):
            wb = self.hbox.itemAt(i).widget()
            wb.setParent(None)
            wb.deleteLater()

    def checkModelsList(self):
        models_count = False
        querystr = "select id, name from Models"
        # conn = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        # conn.setDatabaseName(self.database)
        # conn.open()
        conn = connectBase(self.database)
        query = QtSql.QSqlQuery()
        query.exec(querystr)
        # print(query.isSelect())
        if query.isActive():
            query.first()
            # if query.isValid():
            while query.isValid():
                self.modelslist.append((query.value('id'), query.value('name')))
                self.modelnames.append(query.value('name'))
                query.next()
        if len(self.modelslist):
            models_count = True
            print("Valid")
        else:
            print("not valid")
        conn.close()
        return models_count

    def setModelListView(self):
        connectBase(self.database)
        stm = QtSql.QSqlTableModel(parent=None)
        stm.setTable('Models')
        stm.setSort(1, QtCore.Qt.AscendingOrder)
        stm.select()
        names = [(1, 'Имя'), (2, 'Откуда'), (3, 'Образование/Работа')]
        for (i, n) in names:
            stm.setHeaderData(i, QtCore.Qt.Horizontal, n)
        tv = QtWidgets.QTableView()
        tv.setModel(stm)
        tv.hideColumn(0)
        self.vbox.addWidget(tv)
        self.setModelsEditButton()

    def setModelsEditButton(self):
        for i, f in (('AddModel', self.addModel), ('ChangeModel', self.test), ('DeleteModel', self.test)):
            btn = QtWidgets.QPushButton(i)
            btn.clicked.connect(f)
            self.hbox.addWidget(btn)

    def addModel(self,  a, new=('', '', '', '', '', ''), flag=None):
        def getName():
            value1 = lE_name.text()
            value2 = lE_origin.text()
            value3 = lE_ed_work.text()
            value4 = lE_phone.text()
            value5 = lE_email.text()
            value6 = lE_references.text()
            if value1 == '':
                QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не введено имя')
            else:
                if value1 in list(self.modelnames) and not flag:
                    result = QtWidgets.QMessageBox.question(None, 'Предупреждение',
                                                            'Модель с похожим именем есть в списке.\n' +
                                                            'Хотите продолжить?',
                                                            buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                            defaultButton=QtWidgets.QMessageBox.No)
                    if result == 16384:
                        pass
                    else:
                        return
                if flag == 1:
                    pass
                    # if value1 != value_k_old:
                    #     val_id = self.dw[value_k_old][0]
                    #     del self.dw[value_k_old]
                    # else:
                    #     val_id = self.dw[value1][0]
                    # self.dw[value1] = [val_id] + dcont[1:5] + [value6_1]
                    # txt = 'Изменено слово: '
                    # for i, name in enumerate([val_id] + dcont):
                    #     self.changenote[i].append(name)
                else:
                    txt = 'Добавлена модель: '
                    if self.modelslist:
                        self.modelslist.append((self.modelslist[-1][0] + 1, value1))
                    else:
                        self.modelslist.append((1, value1))
                    self.modelnames.append(value1)
                    self.newmodel = [value1, value2, value3, value4, value5, value6]
                    # self.dw[value1] = [None] + dcont[1:5] + [value6_1]
                    # for j, n in enumerate(dcont):
                    #     self.newname[j].append(n)
                QtWidgets.QMessageBox.information(None, 'Инфо', txt + value1)
                self.clear()
                self.saveModel()
                self.setModelListView()
                tladd_model.close()
        tladd_model = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        tladd_model.setWindowTitle('Добавить')
        tladd_model.setWindowModality(QtCore.Qt.WindowModal)
        tladd_model.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        lE_name = QtWidgets.QLineEdit()
        lE_origin = QtWidgets.QLineEdit()
        lE_ed_work = QtWidgets.QLineEdit()
        lE_phone = QtWidgets.QLineEdit()
        lE_email = QtWidgets.QLineEdit()
        lE_references = QtWidgets.QLineEdit()
        btn_add = QtWidgets.QPushButton('Добавить')
        btn_close = QtWidgets.QPushButton('Закрыть')
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(btn_add)
        hbox.addWidget(btn_close)
        form = QtWidgets.QFormLayout()
        k = 0
        for i in (lE_name, lE_origin, lE_ed_work, lE_phone, lE_email, lE_references):
            i.setText(new[k])
            k += 1
        # if flag == 1:
        #     tladd_model.setWindowTitle('Изменить')
        #     cb_pn.setCurrentText(new[k])
        #     value_k_old = new[0]
        form.addRow('Имя модели:*', lE_name)
        form.addRow('Откуда:', lE_origin)
        form.addRow('Учеба/Работа:', lE_ed_work)
        form.addRow('Телефон:', lE_phone)
        form.addRow('Email:', lE_email)
        form.addRow('Ссылки:', lE_references)
        form.addRow(hbox)
        btn_add.clicked.connect(getName)
        btn_close.clicked.connect(tladd_model.close)
        tladd_model.setLayout(form)
        tladd_model.show()

    def saveModel(self):
        conn = connectBase(self.database)
        query = QtSql.QSqlQuery()
        query.prepare("insert into Models values(null, :name, :origin, :ed_work)")
        query.bindValue(':name', self.newmodel[0])
        query.bindValue(':origin', self.newmodel[1])
        query.bindValue(':ed_work', self.newmodel[2])
        query.exec_()
        query.clear()
        query.prepare("insert into Contacts values(null, :model_id, :phone, :email, :references)")
        query.bindValue(':model_id', self.modelslist[-1][0])
        query.bindValue(':phone', self.newmodel[3])
        query.bindValue(':email', self.newmodel[4])
        query.bindValue(':references', self.newmodel[5])
        query.exec_()
        conn.close()

    def test(self):
        print('test')




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
